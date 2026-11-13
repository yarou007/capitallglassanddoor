#!/usr/bin/env python3
"""Check the deployable static site without a build step or dependencies.

Run ``python3 scripts/verify_site.py``. To verify retained URLs and outgoing
HTML destinations against a pre-edit capture, add ``--baseline PATH``.
This is static verification; it does not measure browser layout or Lighthouse.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qsl, quote, quote_plus, unquote, urlsplit
import xml.etree.ElementTree as ET


DOMAIN = "https://www.capitalglassanddoor.com/"
HOST = "www.capitalglassanddoor.com"
BRAND = "Capital Glass and Door"
PHONE = "tel:+12026434062"
PENDING = {
    "locations/rockville-md.html",
    "locations/towson-md.html",
    "locations/fells-point-baltimore.html",
}
EXCLUDE = {".git", ".codex", ".agents", "node_modules", ".venv", "venv"}
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


def normalize(value: str) -> str:
    return " ".join(unescape(value).split())


class TextOnly(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_html(value: str) -> str:
    parser = TextOnly()
    parser.feed(value)
    return normalize(" ".join(parser.parts))


class Page(HTMLParser):
    def __init__(self, path: Path, root: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.name = path.relative_to(root).as_posix()
        self.source = path.read_text(encoding="utf-8")
        self.elements: list[tuple[str, dict[str, str], int]] = []
        self.refs: list[tuple[str, str, int]] = []
        self.anchors: list[str] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.titles: list[list[str]] = []
        self.meta: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.faqs: list[tuple[str, str]] = []
        self.jsonld: list[str] = []
        self.public_parts: list[str] = []
        self.h1_count = 0
        self._in_title = False
        self._nonpublic_depth = 0
        self._script: list[str] | None = None
        self._details: list[dict[str, object]] = []
        self.feed(self.source)
        self.close()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        line = self.getpos()[0]
        self.elements.append((tag, data, line))
        if tag in {"script", "style", "template"}:
            self._nonpublic_depth += 1
        for attribute in ("alt", "title", "aria-label"):
            if data.get(attribute):
                self.public_parts.append(data[attribute])
        if "id" in data:
            if data["id"] in self.ids:
                self.duplicate_ids.add(data["id"])
            self.ids.add(data["id"])
        if tag == "a" and data.get("name"):
            self.ids.add(data["name"])
        if tag == "a" and "href" in data:
            self.anchors.append(data["href"])
        for attribute in ("href", "src", "poster"):
            if data.get(attribute):
                self.refs.append((attribute, data[attribute], line))
        if data.get("srcset"):
            for candidate in data["srcset"].split(","):
                if candidate.strip():
                    self.refs.append(("srcset", candidate.strip().split()[0], line))
        if tag == "title":
            self.titles.append([])
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.meta.append(data)
        elif tag == "link" and "canonical" in data.get("rel", "").lower().split():
            self.canonicals.append(data.get("href", ""))
        elif tag == "script":
            self._script = [] if data.get("type", "").lower() == "application/ld+json" else None
        if tag == "details":
            self._details.append({"question": [], "answer": [], "summary": False})
        elif tag == "summary" and self._details:
            self._details[-1]["summary"] = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"}:
            self._nonpublic_depth = max(0, self._nonpublic_depth - 1)
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._script is not None:
            self.jsonld.append("".join(self._script))
            self._script = None
        if tag == "summary" and self._details:
            self._details[-1]["summary"] = False
        elif tag == "details" and self._details:
            detail = self._details.pop()
            self.faqs.append((normalize(" ".join(detail["question"])), normalize(" ".join(detail["answer"]))))

    def handle_data(self, data: str) -> None:
        if not self._nonpublic_depth:
            self.public_parts.append(data)
        if self._in_title and self.titles:
            self.titles[-1].append(data)
        if self._script is not None:
            self._script.append(data)
        if self._details:
            detail = self._details[-1]
            detail["question" if detail["summary"] else "answer"].append(data)

    def metavalues(self, name: str) -> list[str]:
        return [item.get("content", "") for item in self.meta if item.get("name", "").lower() == name]

    @property
    def noindex(self) -> bool:
        return any("noindex" in value.lower().split(",") or "noindex" in value.lower().split()
                   for value in self.metavalues("robots"))

    @property
    def expected_url(self) -> str:
        return DOMAIN if self.name == "index.html" else DOMAIN + self.name


def walk_nodes(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_nodes(child)


def types(node: dict) -> set[str]:
    value = node.get("@type", [])
    return {value} if isinstance(value, str) else set(value)


def site_files(root: Path, pattern: str) -> list[Path]:
    return sorted(path for path in root.rglob(pattern)
                  if not any(part in EXCLUDE or part.startswith(".") for part in path.relative_to(root).parts))


def local_target(page: Page, href: str, root: Path) -> tuple[Path, str] | None:
    url = urlsplit(href)
    if url.scheme or url.netloc:
        if url.scheme not in {"http", "https", ""} or url.hostname not in {HOST, HOST.removeprefix("www.")}:
            return None
        base = root
    else:
        base = root if url.path.startswith("/") else page.path.parent
    decoded = unquote(url.path)
    target = (base / decoded.lstrip("/")).resolve() if decoded else page.path
    if target.is_dir() or decoded.endswith("/"):
        target = target / "index.html"
    return target, unquote(url.fragment)


def verify(root: Path, baseline: Path | None) -> int:
    errors: list[str] = []
    pages: dict[Path, Page] = {}
    title_owners: dict[str, list[str]] = defaultdict(list)
    description_owners: dict[str, list[str]] = defaultdict(list)
    message_owners: dict[str, list[str]] = defaultdict(list)
    noindex_names: set[str] = set()
    refs_checked = 0
    faq_count = 0

    def fail(name: str, reason: str) -> None:
        errors.append(f"{name}: {reason}")

    for path in site_files(root, "*.html"):
        try:
            page = Page(path, root)
            pages[path.resolve()] = page
        except (UnicodeError, ValueError) as exc:
            fail(path.relative_to(root).as_posix(), f"could not parse HTML: {exc}")

    if not pages:
        fail("site", "no HTML pages found")

    for page in pages.values():
        if page.h1_count != 1:
            fail(page.name, f"expected one H1, found {page.h1_count}")
        titles = [normalize(" ".join(parts)) for parts in page.titles]
        if len(titles) != 1 or not titles[0]:
            fail(page.name, "expected one nonempty title")
        else:
            title_owners[titles[0].casefold()].append(page.name)
            if BRAND not in titles[0]:
                fail(page.name, "title must use the exact full business name")
        descriptions = page.metavalues("description")
        if len(descriptions) != 1 or not normalize(descriptions[0]):
            fail(page.name, "expected one nonempty meta description")
        else:
            description_owners[normalize(descriptions[0]).casefold()].append(page.name)
        if page.canonicals != [page.expected_url]:
            fail(page.name, f"canonical must be exactly {page.expected_url}")
        if not page.metavalues("viewport"):
            fail(page.name, "missing mobile viewport")
        if page.duplicate_ids:
            fail(page.name, "duplicate IDs: " + ", ".join(sorted(page.duplicate_ids)))
        if page.noindex:
            noindex_names.add(page.name)
        if page.name in PENDING and not page.noindex:
            fail(page.name, "pending service coverage page must remain noindex")

        # Missing business facts belong in project documentation, not customer
        # pages. Also catch escaped markers or markers left in HTML comments.
        if re.search(r"\[\s*ADD\s*:", unescape(page.source), re.I):
            fail(page.name, "owner ADD placeholder remains in public HTML")
        public_text = normalize(" ".join(page.public_parts + [
            item.get("content", "") for item in page.meta
        ]))
        for pattern in (
            r"\bawaiting\s+(?:owner|business)\s+confirmation\b",
            r"\bowner[-\s]+(?:approved|confirmation)\b",
            r"\bproject\s+placeholders\b",
            r"\binformation\s+to\s+confirm\b",
            r"\bcoverage\s+confirmation\s+(?:is\s+)?pending\b",
            r"\bawaiting\s+coverage\s+confirmation\b",
            r"\bbusiness\s+verification\s+details\b",
            r"\bretaining\s+this\s+existing\s+location\s+URL\b",
            r"\bexcluded\s+from\s+search\s+indexing\b",
            r"\bsupplied\s+service\s+markets\b",
        ):
            if match := re.search(pattern, public_text, re.I):
                fail(page.name, "owner-facing copy remains: " + match.group())

        calls = 0
        messages: set[str] = set()
        for href in page.anchors:
            url = urlsplit(href)
            if url.scheme.lower() == "tel":
                calls += 1
                if href != PHONE:
                    fail(page.name, f"incorrect telephone action: {href}")
            if url.hostname and (url.hostname == "wa.me" or "whatsapp" in url.hostname):
                if url.scheme != "https" or url.netloc != "wa.me" or url.path != "/12026434062":
                    fail(page.name, f"incorrect WhatsApp destination: {href}")
                    continue
                try:
                    query = parse_qsl(url.query, keep_blank_values=True, errors="strict")
                except (UnicodeError, ValueError) as exc:
                    fail(page.name, f"invalid WhatsApp encoding: {exc}")
                    continue
                if len(query) != 1 or query[0][0] != "text" or not query[0][1].strip():
                    fail(page.name, "WhatsApp needs one nonempty text parameter")
                    continue
                message = query[0][1]
                encoded = url.query.removeprefix("text=")
                if encoded not in {quote(message, safe=""), quote_plus(message, safe="")}:
                    fail(page.name, "WhatsApp message must be URL-encoded")
                messages.add(message)
        if not calls:
            fail(page.name, "missing direct telephone action")
        if len(messages) != 1:
            fail(page.name, f"expected one consistent page-specific WhatsApp message, found {len(messages)}")
        else:
            message_owners[next(iter(messages))].append(page.name)

        for tag, attrs, line in page.elements:
            if tag in {"form", "input", "select", "textarea"} or "formaction" in attrs or "form" in attrs:
                fail(page.name, f"form markup remains at line {line}")
            if tag == "button" and attrs.get("type") == "submit":
                fail(page.name, f"submit button remains at line {line}")
            if tag == "img" and (not attrs.get("width") or not attrs.get("height")):
                fail(page.name, f"image dimensions missing at line {line}")
            if tag == "img" and "alt" not in attrs:
                fail(page.name, f"image alt attribute missing at line {line}")

        parsed_documents = []
        for index, source in enumerate(page.jsonld, 1):
            try:
                document = json.loads(source)
                parsed_documents.append(document)
                if not isinstance(document, (dict, list)):
                    fail(page.name, f"JSON-LD block {index} must be an object or array")
            except json.JSONDecodeError as exc:
                fail(page.name, f"JSON-LD block {index}: {exc}")
        if not parsed_documents:
            fail(page.name, "missing parseable JSON-LD")
        structured_faqs = []
        for document in parsed_documents:
            if "[ADD:" in json.dumps(document, ensure_ascii=False):
                fail(page.name, "owner placeholders must stay outside active JSON-LD")
            for node in walk_nodes(document):
                if "FAQPage" in types(node):
                    for question in node.get("mainEntity", []):
                        answer = question.get("acceptedAnswer", {})
                        structured_faqs.append((plain_html(str(question.get("name", ""))), plain_html(str(answer.get("text", "")))))
                if "LocalBusiness" in types(node) or "Locksmith" in types(node):
                    if node.get("name") != BRAND or node.get("telephone") != "+12026434062":
                        fail(page.name, "business JSON-LD name/telephone is inconsistent")
                    if any(key in node for key in ("aggregateRating", "review", "openingHours", "openingHoursSpecification")):
                        fail(page.name, "unconfirmed reviews or service hours must stay out of business JSON-LD")
        if structured_faqs != page.faqs:
            fail(page.name, "visible FAQ accordions and FAQPage JSON-LD do not match")
        faq_count += len(structured_faqs)

        for attribute, href, line in page.refs:
            if href.startswith(("data:", "javascript:")):
                if href.startswith("javascript:"):
                    fail(page.name, f"JavaScript URL at line {line}")
                continue
            local = local_target(page, href, root)
            if local is None:
                continue
            target, fragment = local
            refs_checked += 1
            try:
                target.relative_to(root)
            except ValueError:
                fail(page.name, f"reference leaves site root at line {line}: {href}")
                continue
            if not target.is_file():
                fail(page.name, f"missing {attribute} target at line {line}: {href}")
            elif fragment and target.suffix.lower() == ".html":
                destination = pages.get(target.resolve())
                if destination is None or fragment not in destination.ids:
                    fail(page.name, f"missing fragment at line {line}: {href}")

    for label, owners in (("title", title_owners), ("meta description", description_owners), ("WhatsApp prefill", message_owners)):
        for names in owners.values():
            if len(names) > 1:
                fail("site", f"duplicate {label}: " + ", ".join(names))

    for path in site_files(root, "*.html") + site_files(root, "*.js"):
        source = path.read_text(encoding="utf-8")
        name = path.relative_to(root).as_posix()
        for pattern, label in (
            (r"sms\s*:", "SMS action"),
            (r"mailto\s*:", "email action"),
            (r"formsubmit|formspree|contact-form", "form endpoint or form logic"),
            (r"<\s*(?:form|input|textarea|select)\b", "form field markup"),
            (r"addEventListener\s*\(\s*['\"]submit['\"]", "form submit listener"),
            (r"querySelector(?:All)?\s*\(\s*['\"]form(?:['\"\s.#\[])", "form selector"),
        ):
            if re.search(pattern, source, re.I):
                fail(name, f"forbidden {label} remains")

    for path in site_files(root, "*.css"):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", source):
            href = match.group(1).strip()
            if href.startswith(("data:", "http:", "https:", "//", "#")):
                continue
            target = (root / href.lstrip("/")) if href.startswith("/") else path.parent / href
            if not target.is_file():
                fail(path.relative_to(root).as_posix(), f"missing CSS asset: {href}")

    sitemap_urls: list[str] = []
    try:
        sitemap = ET.parse(root / "sitemap.xml")
        sitemap_urls = [element.text.strip() for element in sitemap.iter() if element.tag.split("}")[-1] == "loc" and element.text]
        if len(sitemap_urls) != len(set(sitemap_urls)):
            fail("sitemap.xml", "duplicate URLs")
        expected = {page.expected_url for page in pages.values() if not page.noindex}
        missing = expected - set(sitemap_urls)
        extra = set(sitemap_urls) - expected
        for url in sorted(missing):
            fail("sitemap.xml", f"indexable page missing: {url}")
        for url in sorted(extra):
            fail("sitemap.xml", f"URL is missing, noncanonical or noindex: {url}")
    except (OSError, ET.ParseError) as exc:
        fail("sitemap.xml", str(exc))

    if baseline:
        try:
            captured = json.loads(baseline.read_text(encoding="utf-8"))
            for name, snapshot in captured.items():
                page = pages.get((root / name).resolve())
                if page is None:
                    fail("baseline", f"existing URL removed: {name}")
                    continue
                current_destinations = {local[0] for href in page.anchors
                                        if (local := local_target(page, href, root)) is not None
                                        and local[0].suffix == ".html"}
                for href in set(snapshot.get("links", [])):
                    local = local_target(page, href, root)
                    if local and local[0].suffix == ".html" and not href.startswith("#") and local[0] != page.path:
                        if local[0] not in current_destinations:
                            fail(name, f"existing internal HTML destination removed: {href}")
        except (OSError, ValueError, TypeError) as exc:
            fail("baseline", f"could not load baseline: {exc}")

    print(f"Checked {len(pages)} HTML pages, {refs_checked} local references, {faq_count} FAQ answers and {len(sitemap_urls)} sitemap URLs.")
    print(f"Pending/noindex pages: {len(noindex_names)}. Frameworks, network access and a build step are not required.")
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: metadata, structured data, links, assets, fragments, contact actions and sitemap checks passed.")
    if baseline:
        print("PASS: original HTML URLs and outgoing internal HTML destinations were preserved.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="site root (defaults to repository root)")
    parser.add_argument("--baseline", type=Path, help="optional pre-edit JSON capture keyed by HTML path, with a links array")
    args = parser.parse_args()
    return verify(args.root.resolve(), args.baseline)


if __name__ == "__main__":
    sys.exit(main())
