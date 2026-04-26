#!/usr/bin/env python3
"""
Restaurant & Food Business Data Collector
==========================================
Collects independent/local food business data for a given city
using Google Places API and Yelp Fusion API, then exports to Excel.

Usage:
    python restaurant_scraper.py --city Guelph
    python restaurant_scraper.py -c "Cambridge" --log-level DEBUG
    python restaurant_scraper.py              # prompts for city
"""

import argparse
import logging
import os
import re
import sys
import time
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
YELP_API_KEY: str = os.getenv("YELP_API_KEY", "")

SEARCH_KEYWORDS: list[str] = [
    "restaurant",
    "sweet shop",
    "mithai",
    "bakery",
    "cloud kitchen",
    "takeout kitchen",
    "Indian restaurant",
    "sweets manufacturer",
]

# Known large chains / franchise brand keywords (lowercase)
FRANCHISE_KEYWORDS: list[str] = [
    "mcdonald",
    "tim horton",
    "subway",
    "starbucks",
    "burger king",
    "wendy",
    "pizza hut",
    "domino",
    "kfc",
    "popeyes",
    "chick-fil-a",
    "dairy queen",
    "harvey",
    "a&w",
    "swiss chalet",
    "boston pizza",
    "kelsey",
    "east side mario",
    "the keg",
    "mr sub",
    "quiznos",
    "panera",
    "chipotle",
    "taco bell",
    "five guys",
    "shake shack",
    "panda express",
    "nando",
    "new york fries",
    "mary brown",
    "greco pizza",
    "pizza pizza",
    "241 pizza",
    "freshii",
    "mucho burrito",
    "qdoba",
    "jimmy john",
    "jersey mike",
    "little caesar",
    "papa john",
    "arby",
    "sonic drive",
    "popeyes",
    "carl's jr",
    "hardee",
    "long john silver",
]

# Chains hints that lower confidence but don't auto-exclude
CHAIN_HINT_WORDS: list[str] = [
    "chain",
    "group",
    "holdings",
    "international",
    "worldwide",
    "global",
    "corp",
    "franchise",
    "network",
]

EXCEL_COLUMNS: list[str] = [
    "Business Name",
    "Address",
    "City",
    "Phone Number",
    "Website",
    "Category / Cuisine",
    "Source",
    "Confidence Score (Independent)",
]

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logger = logging.getLogger("restaurant_scraper")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


# ---------------------------------------------------------------------------
# Helpers: franchise detection, phone normalization, confidence scoring
# ---------------------------------------------------------------------------


def is_franchise(name: str) -> bool:
    """Return True if the business name matches a known franchise indicator."""
    name_lower = name.lower()
    return any(kw in name_lower for kw in FRANCHISE_KEYWORDS)


def normalize_phone(phone: str) -> str:
    """Standardize phone to (XXX) XXX-XXXX format where possible."""
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone  # Return original if format is unexpected


def compute_confidence_score(name: str) -> float:
    """
    Estimate how likely this is an independent business.
    Returns a score from 0.0 (likely chain) to 1.0 (likely independent).
    """
    if is_franchise(name):
        return 0.0

    score = 1.0
    name_lower = name.lower()

    # Penalize multi-location number patterns like "#2" or "Location 3"
    if re.search(r"\b(#\d+|location\s*\d+|\d{3,})\b", name_lower):
        score -= 0.2

    for hint in CHAIN_HINT_WORDS:
        if hint in name_lower:
            score -= 0.15

    return max(0.0, round(score, 2))


# ---------------------------------------------------------------------------
# HTTP helper with retry / rate-limit handling
# ---------------------------------------------------------------------------


def safe_request(
    url: str,
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    retries: int = 3,
    backoff: float = 2.0,
) -> Optional[requests.Response]:
    """GET with automatic retry and rate-limit back-off."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if resp.status_code == 429:
                wait = backoff * (attempt + 1)
                logger.warning("Rate limited. Waiting %.1fs before retry…", wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            logger.warning(
                "Request failed (attempt %d/%d): %s", attempt + 1, retries, exc
            )
            if attempt < retries - 1:
                time.sleep(backoff)

    logger.error("All retries exhausted for: %s", url)
    return None


# ---------------------------------------------------------------------------
# Google Places API
# ---------------------------------------------------------------------------


def _google_place_details(place_id: str) -> dict:
    """Fetch phone number and website from Google Place Details endpoint."""
    if not place_id or not GOOGLE_API_KEY:
        return {}
    resp = safe_request(
        "https://maps.googleapis.com/maps/api/place/details/json",
        params={
            "place_id": place_id,
            "fields": "formatted_phone_number,website",
            "key": GOOGLE_API_KEY,
        },
    )
    if resp:
        return resp.json().get("result", {})
    return {}


def fetch_google_places(city: str) -> list[dict]:
    """Query Google Places Text Search API for food businesses in the city."""
    if not GOOGLE_API_KEY:
        logger.warning("GOOGLE_API_KEY not set — skipping Google Places.")
        return []

    results: list[dict] = []
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    for keyword in SEARCH_KEYWORDS:
        query = f"{keyword} in {city}, Ontario, Canada"
        params: dict = {"query": query, "key": GOOGLE_API_KEY, "type": "food"}
        logger.info("[Google] Searching: %s", query)

        while True:
            resp = safe_request(base_url, params=params)
            if not resp:
                break

            data = resp.json()
            places = data.get("results", [])
            logger.info("[Google] %d results for '%s'", len(places), keyword)

            for place in places:
                name = place.get("name", "")
                if not name or is_franchise(name):
                    continue

                details = _google_place_details(place.get("place_id", ""))
                cuisine = ", ".join(
                    t
                    for t in place.get("types", [])
                    if t not in {"point_of_interest", "establishment"}
                )

                results.append(
                    {
                        "Business Name": name,
                        "Address": place.get("formatted_address", ""),
                        "City": city,
                        "Phone Number": normalize_phone(
                            details.get("formatted_phone_number", "")
                        ),
                        "Website": details.get("website", ""),
                        "Category / Cuisine": cuisine,
                        "Source": "Google Places",
                        "Confidence Score (Independent)": compute_confidence_score(
                            name
                        ),
                    }
                )

            next_token = data.get("next_page_token")
            if next_token:
                # Google requires a short pause before the next-page token is valid
                time.sleep(2)
                params = {"pagetoken": next_token, "key": GOOGLE_API_KEY}
            else:
                break

    logger.info("[Google] Total collected: %d", len(results))
    return results


# ---------------------------------------------------------------------------
# Yelp Fusion API
# ---------------------------------------------------------------------------


def fetch_yelp(city: str) -> list[dict]:
    """Query Yelp Fusion Business Search API for food businesses in the city."""
    if not YELP_API_KEY:
        logger.warning("YELP_API_KEY not set — skipping Yelp.")
        return []

    results: list[dict] = []
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    base_url = "https://api.yelp.com/v3/businesses/search"

    yelp_categories = "restaurants,food,bakeries,desserts,candy,indpak,sweets"
    limit = 50
    offset = 0
    max_results = 1000  # Yelp hard cap

    while offset < max_results:
        params = {
            "location": f"{city}, Ontario, Canada",
            "categories": yelp_categories,
            "limit": limit,
            "offset": offset,
        }
        logger.info("[Yelp] Fetching records at offset %d…", offset)
        resp = safe_request(base_url, headers=headers, params=params)
        if not resp:
            break

        data = resp.json()

        # Yelp may return an error dict instead of businesses
        if "error" in data:
            logger.error(
                "[Yelp] API error: %s", data["error"].get("description", data["error"])
            )
            break

        businesses = data.get("businesses", [])
        if not businesses:
            break

        logger.info("[Yelp] %d businesses at offset %d", len(businesses), offset)

        for biz in businesses:
            name = biz.get("name", "")
            if not name or is_franchise(name):
                continue

            location = biz.get("location", {})
            address = ", ".join(location.get("display_address", []))
            cuisine = ", ".join(c.get("title", "") for c in biz.get("categories", []))
            phone = biz.get("display_phone", "") or biz.get("phone", "")

            results.append(
                {
                    "Business Name": name,
                    "Address": address,
                    "City": city,
                    "Phone Number": normalize_phone(phone),
                    # Yelp Fusion does not expose business websites; using Yelp listing URL
                    "Website": biz.get("url", ""),
                    "Category / Cuisine": cuisine,
                    "Source": "Yelp",
                    "Confidence Score (Independent)": compute_confidence_score(name),
                }
            )

        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break
        time.sleep(0.5)  # Polite pacing

    logger.info("[Yelp] Total collected: %d", len(results))
    return results


# ---------------------------------------------------------------------------
# OpenStreetMap Overpass API  (no API key required)
# ---------------------------------------------------------------------------

# OSM amenity/shop tags that correspond to food businesses
_OSM_FOOD_TAGS: list[tuple[str, str]] = [
    ("amenity", "restaurant"),
    ("amenity", "cafe"),
    ("amenity", "fast_food"),
    ("amenity", "bakery"),
    ("amenity", "ice_cream"),
    ("shop", "bakery"),
    ("shop", "confectionery"),
    ("shop", "pastry"),
    ("shop", "deli"),
    ("shop", "sweets"),
]

_OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _build_overpass_query(city: str) -> str:
    """Build an Overpass QL query for all food-related OSM nodes/ways in a city."""
    area_selector = f'area["name"="{city}"]["place"~"city|town|village"]->.searchArea;'
    parts: list[str] = []
    for tag_k, tag_v in _OSM_FOOD_TAGS:
        parts.append(f'node["{tag_k}"="{tag_v}"](area.searchArea);')
        parts.append(f'way["{tag_k}"="{tag_v}"](area.searchArea);')
    union = "\n  ".join(parts)
    return f"""[out:json][timeout:60];
{area_selector}
(
  {union}
);
out center tags;"""


def fetch_overpass(city: str) -> list[dict]:
    """Fetch food business data from OpenStreetMap via Overpass API (no key needed)."""
    query = _build_overpass_query(city)
    logger.info("[OSM] Querying Overpass API for %s…", city)

    resp = safe_request(_OVERPASS_URL, params={"data": query}, retries=3, backoff=5.0)
    if not resp:
        logger.error("[OSM] Overpass query failed.")
        return []

    elements = resp.json().get("elements", [])
    logger.info("[OSM] %d raw elements returned.", len(elements))

    results: list[dict] = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        if not name or is_franchise(name):
            continue

        # Reconstruct address from OSM addr:* tags
        addr_parts = [
            tags.get("addr:housenumber", ""),
            tags.get("addr:street", ""),
        ]
        address = " ".join(p for p in addr_parts if p)
        if tags.get("addr:city"):
            address = (
                f"{address}, {tags['addr:city']}" if address else tags["addr:city"]
            )

        cuisine = (
            tags.get("cuisine", "") or tags.get("shop", "") or tags.get("amenity", "")
        )
        cuisine = cuisine.replace("_", " ").replace(";", ", ")

        results.append(
            {
                "Business Name": name,
                "Address": address,
                "City": city,
                "Phone Number": normalize_phone(
                    tags.get("phone", "") or tags.get("contact:phone", "")
                ),
                "Website": tags.get("website", "") or tags.get("contact:website", ""),
                "Category / Cuisine": cuisine,
                "Source": "OpenStreetMap",
                "Confidence Score (Independent)": compute_confidence_score(name),
            }
        )

    logger.info("[OSM] %d businesses after filtering.", len(results))
    return results


# ---------------------------------------------------------------------------
# YellowPages.ca  (HTML scraping — robots.txt permits crawling)
# ---------------------------------------------------------------------------

_YP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-CA,en;q=0.9",
}

_YP_SEARCH_TERMS: list[str] = [
    "restaurants",
    "sweet-shops",
    "bakeries",
    "indian-restaurants",
    "takeout-restaurants",
]


def _parse_yp_page(html: str, city: str) -> list[dict]:
    """Extract business cards from a YellowPages.ca search result page."""
    from urllib.parse import unquote

    soup = BeautifulSoup(html, "lxml")
    records: list[dict] = []

    for card in soup.select("div.listing__content__wrapper"):
        name_tag = card.select_one("a.listing__name--link")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name or is_franchise(name):
            continue

        # Address from schema.org microdata spans
        parts = [
            card.select_one("[itemprop=streetAddress]"),
            card.select_one("[itemprop=addressLocality]"),
            card.select_one("[itemprop=addressRegion]"),
            card.select_one("[itemprop=postalCode]"),
        ]
        address = " ".join(p.get_text(strip=True) for p in parts if p)

        # Phone stored in data-phone attribute
        phone_tag = card.select_one("[data-phone]")
        phone = phone_tag["data-phone"] if phone_tag else ""

        # Website extracted from YP redirect URL
        ws_tag = card.select_one("a[href*='gourl']")
        website = ""
        if ws_tag:
            m = re.search(r"redirect=([^&]+)", ws_tag.get("href", ""))
            if m:
                website = unquote(m.group(1))

        records.append(
            {
                "Business Name": name,
                "Address": address,
                "City": city,
                "Phone Number": normalize_phone(phone),
                "Website": website,
                "Category / Cuisine": "",
                "Source": "YellowPages.ca",
                "Confidence Score (Independent)": compute_confidence_score(name),
            }
        )
    return records


def fetch_yellowpages(city: str) -> list[dict]:
    """Scrape YellowPages.ca for food businesses in the city."""
    results: list[dict] = []
    city_slug = city.lower().replace(" ", "-")

    for term in _YP_SEARCH_TERMS:
        page = 1
        while True:
            url = f"https://www.yellowpages.ca/search/si/{page}/{term}/{city_slug}+ON"
            logger.info("[YellowPages] %s page %d…", term, page)
            resp = safe_request(url, headers=_YP_HEADERS, retries=3, backoff=3.0)
            if not resp:
                break

            if resp.status_code == 404 or "no results" in resp.text.lower():
                logger.info("[YellowPages] No more results for '%s'.", term)
                break

            page_records = _parse_yp_page(resp.text, city)
            if not page_records:
                break

            results.extend(page_records)
            logger.info("[YellowPages] %d records on page %d.", len(page_records), page)

            # Stop after 10 pages per term to stay polite
            if page >= 10:
                break
            page += 1
            time.sleep(1.5)  # polite delay between pages

    logger.info("[YellowPages] Total collected: %d", len(results))
    return results


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def deduplicate(records: list[dict]) -> list[dict]:
    """Remove duplicates keyed on normalised (Business Name, Address)."""
    seen: set[tuple] = set()
    unique: list[dict] = []
    for record in records:
        key = (
            re.sub(r"\s+", " ", record["Business Name"].strip().lower()),
            re.sub(r"\s+", " ", record["Address"].strip().lower()),
        )
        if key not in seen:
            seen.add(key)
            unique.append(record)

    logger.info("Deduplication: %d → %d records", len(records), len(unique))
    return unique


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_to_excel(records: list[dict], city: str) -> str:
    """Save records to <city>_restaurants.xlsx, sorted by confidence score."""
    filename = f"{city.replace(' ', '_').lower()}_restaurants.xlsx"
    df = pd.DataFrame(records, columns=EXCEL_COLUMNS)
    df.sort_values("Confidence Score (Independent)", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_excel(filename, index=False, engine="openpyxl")
    logger.info("Exported %d records to: %s", len(df), filename)
    return filename


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect independent restaurant/food business data for a city.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--city",
        "-c",
        type=str,
        help="City name to search (e.g., Guelph, Cambridge, Waterloo)",
    )
    parser.add_argument(
        "--log-level",
        "-l",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )
    return parser.parse_args()


def prompt_city() -> str:
    """Interactively prompt the user for a city name with basic validation."""
    city = input("Enter city name: ").strip()
    if not city:
        print("Error: City name cannot be empty.")
        sys.exit(1)
    if any(ch.isdigit() for ch in city):
        print("Error: City name should not contain numbers.")
        sys.exit(1)
    if len(city.split()) > 4:
        print(
            "Error: Please enter a single city name only (e.g., 'Cambridge', 'Niagara Falls')."
        )
        sys.exit(1)
    return city.title()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    city = args.city.title() if args.city else prompt_city()
    logger.info("Starting data collection for: %s", city)

    all_records: list[dict] = []

    # No-key sources (always run)
    osm_records = fetch_overpass(city)
    all_records.extend(osm_records)

    yp_records = fetch_yellowpages(city)
    all_records.extend(yp_records)

    # API-key sources (run only if keys are configured)
    google_records = fetch_google_places(city)
    all_records.extend(google_records)

    yelp_records = fetch_yelp(city)
    all_records.extend(yelp_records)

    if not all_records:
        logger.warning(
            "No records collected. Check network connectivity or try a different city name."
        )
        sys.exit(0)

    unique_records = deduplicate(all_records)
    output_file = export_to_excel(unique_records, city)

    print(
        f"\nCollection complete. {len(unique_records)} unique businesses saved to: {output_file}"
    )


if __name__ == "__main__":
    main()
