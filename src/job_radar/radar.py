from __future__ import annotations

import csv
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path

import feedparser
import requests


@dataclass(frozen=True)
class Listing:
    title: str
    company: str
    location: str
    url: str
    published: str
    matched_skills: tuple[str, ...]
    score: int


def rank_listing(title: str, summary: str, skills: list[str]) -> tuple[tuple[str, ...], int]:
    text = f"{title} {summary}".casefold()
    matched = tuple(skill for skill in skills if skill.strip() and skill.casefold() in text)
    return matched, len(matched)


def fetch_feed(url: str, timeout: float = 12) -> list[Listing]:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "JobRadar/1.0 (personal feed reader)"})
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    listings = []
    for item in feed.entries:
        title = str(item.get("title", "Untitled role")).strip()
        summary = str(item.get("summary", item.get("description", "")))
        company = str(item.get("author", item.get("company", ""))).strip()
        location = str(item.get("location", "")).strip()
        url_value = str(item.get("link", "")).strip()
        published = str(item.get("published", item.get("updated", ""))).strip()
        listings.append((title, company, location, url_value, published, summary))
    return listings


def collect(feeds: list[str], skills: list[str], timeout: float = 12) -> list[Listing]:
    seen: set[str] = set()
    results = []
    for feed_url in feeds:
        for title, company, location, url, published, summary in fetch_feed(feed_url, timeout):
            key = url or hashlib.sha256(f"{title}|{company}|{published}".encode()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            matched, score = rank_listing(title, summary, skills)
            results.append(Listing(title, company, location, url, published, matched, score))
    return sorted(results, key=lambda listing: (-listing.score, listing.published, listing.title.casefold()))


def write_csv(listings: list[Listing], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(asdict(listings[0]).keys()) if listings else
                                ["title", "company", "location", "url", "published", "matched_skills", "score"])
        writer.writeheader()
        for listing in listings:
            row = asdict(listing)
            row["matched_skills"] = ", ".join(listing.matched_skills)
            writer.writerow(row)
