import argparse
from pathlib import Path

from .radar import collect, write_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect and rank listings from public RSS feeds.")
    parser.add_argument("--feed", action="append", required=True, help="public RSS or Atom URL; repeat for multiple")
    parser.add_argument("--skills", required=True, help="comma-separated skill keywords")
    parser.add_argument("--output", type=Path, default=Path("jobs.csv"))
    args = parser.parse_args(argv)
    skills = [value.strip() for value in args.skills.split(",") if value.strip()]
    try:
        listings = collect(args.feed, skills)
        write_csv(listings, args.output)
    except Exception as error:
        parser.error(str(error))
    print(f"Saved {len(listings)} listing(s) to {args.output}")
    for item in listings[:5]:
        print(f"{item.score:2}  {item.title} — {item.company} [{', '.join(item.matched_skills)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
