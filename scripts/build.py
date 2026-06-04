#!/usr/bin/env python3
from __future__ import annotations

import shutil
from typing import Any

from cataloglib import (
    CATEGORIES,
    DIST_DIR,
    CatalogError,
    content_sha,
    json_dump,
    load_validated_providers,
    now_iso,
)


def snake_provider(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    endpoints = payload["endpoints"]
    prices = [endpoint["minPriceUsd"] for endpoint in endpoints] + [
        endpoint["maxPriceUsd"] for endpoint in endpoints
    ]
    return {
        "fqn": payload["fqn"],
        "title": payload["title"],
        "subtitle": payload["subtitle"],
        "description": payload["description"],
        "use_case": payload["useCase"],
        "i18n": payload["i18n"],
        "logo": payload["logo"],
        "category": payload["category"],
        "chains": payload["chains"],
        "is_first_party": payload["isFirstParty"],
        "is_featured": payload["isFeatured"],
        "featured_tags": payload["featuredTags"],
        "service_url": payload["serviceUrl"],
        "endpoint_count": len(endpoints),
        "has_metering": any(endpoint["metered"] for endpoint in endpoints),
        "has_free_tier": any(endpoint["minPriceUsd"] == 0 for endpoint in endpoints),
        "min_price_usd": min(prices),
        "max_price_usd": max(prices),
        "sha": sha,
    }


def detail_provider(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    detail = snake_provider(payload, sha)
    detail["endpoints"] = [
        {
            "method": endpoint["method"],
            "path": endpoint["path"],
            "url": endpoint["url"],
            "title": endpoint["title"],
            "subtitle": endpoint["subtitle"],
            "description": endpoint["description"],
            "use_case": endpoint["useCase"],
            "i18n": endpoint["i18n"],
            "metered": endpoint["metered"],
            "min_price_usd": endpoint["minPriceUsd"],
            "max_price_usd": endpoint["maxPriceUsd"],
        }
        for endpoint in payload["endpoints"]
    ]
    detail["status"] = payload.get(
        "status",
        {
            "catalog": "listed",
            "gateway": "unknown",
            "payment": "unknown",
            "upstream": "unknown",
        },
    )
    return detail


def pay_json(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    return {
        "version": 1,
        "fqn": payload["fqn"],
        "title": payload["title"],
        "subtitle": payload["subtitle"],
        "description": payload["description"],
        "use_case": payload["useCase"],
        "i18n": payload["i18n"],
        "service_url": payload["serviceUrl"],
        "chains": payload["chains"],
        "sha": sha,
        "endpoints": [
            {
                "method": endpoint["method"],
                "path": endpoint["path"],
                "url": endpoint["url"],
                "description": endpoint["description"],
                "metered": endpoint["metered"],
                "min_price_usd": endpoint["minPriceUsd"],
                "max_price_usd": endpoint["maxPriceUsd"],
            }
            for endpoint in payload["endpoints"]
        ],
    }


def search_doc(summary: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "fqn": summary["fqn"],
        "title": summary["title"],
        "subtitle": summary["subtitle"],
        "description": summary["description"],
        "use_case": summary["use_case"],
        "category": summary["category"],
        "chains": summary["chains"],
        "featured_tags": summary["featured_tags"],
        "service_url": summary["service_url"],
        "endpoints": [
            {
                "method": endpoint["method"],
                "path": endpoint["path"],
                "title": endpoint["title"],
                "description": endpoint["description"],
            }
            for endpoint in detail["endpoints"]
        ],
    }


def main() -> int:
    try:
        providers = load_validated_providers()
    except CatalogError as exc:
        print(str(exc))
        return 1

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    generated_at = now_iso()
    summaries: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    search_docs: list[dict[str, Any]] = []
    used_categories: dict[str, int] = {}
    used_chains: dict[str, int] = {}

    for provider_dir, payload, pay_md in providers:
        sha = content_sha(payload, pay_md)
        summary = snake_provider(payload, sha)
        detail = detail_provider(payload, sha)
        summaries.append(summary)
        details.append(detail)
        search_docs.append(search_doc(summary, detail))
        used_categories[summary["category"]] = used_categories.get(summary["category"], 0) + 1
        for chain in summary["chains"]:
            used_chains[chain] = used_chains.get(chain, 0) + 1

        fqn = summary["fqn"]
        json_dump(DIST_DIR / "providers" / f"{fqn}.json", detail)
        json_dump(DIST_DIR / "pay" / f"{fqn}.json", pay_json(payload, sha))
        (DIST_DIR / "pay").mkdir(parents=True, exist_ok=True)
        (DIST_DIR / "pay" / f"{fqn}.md").write_text(pay_md, encoding="utf-8")

    summaries.sort(key=lambda item: (not item["is_featured"], item["category"], item["fqn"]))
    base_url = "https://catalog.bankofai.io/api"
    catalog = {
        "version": 1,
        "generated_at": generated_at,
        "provider_count": len(summaries),
        "first_party_count": sum(1 for provider in summaries if provider["is_first_party"]),
        "chain_count": len(used_chains),
        "base_url": base_url,
        "frontend": {
            "featured_fqns": [provider["fqn"] for provider in summaries if provider["is_featured"]],
            "categories": [
                {"id": category, "count": used_categories.get(category, 0)}
                for category in sorted(CATEGORIES)
                if used_categories.get(category, 0)
            ],
            "chains": [
                {"id": chain, "count": count}
                for chain, count in sorted(used_chains.items())
            ],
        },
        "providers": summaries,
    }
    json_dump(DIST_DIR / "catalog.json", catalog)
    json_dump(DIST_DIR / "categories.json", catalog["frontend"]["categories"])
    json_dump(DIST_DIR / "search-index.json", {"version": 1, "generated_at": generated_at, "documents": search_docs})
    json_dump(
        DIST_DIR / "status.json",
        {
            "version": 1,
            "generated_at": generated_at,
            "provider_count": len(summaries),
            "status": "ok",
        },
    )
    print(f"built {len(summaries)} provider(s) into {DIST_DIR.relative_to(DIST_DIR.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
