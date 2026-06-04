#!/usr/bin/env python3
from __future__ import annotations

from cataloglib import CatalogError, load_validated_providers


def main() -> int:
    try:
        providers = load_validated_providers()
    except CatalogError as exc:
        print(str(exc))
        return 1
    print(f"validated {len(providers)} provider(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
