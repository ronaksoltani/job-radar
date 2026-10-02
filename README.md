# Job Radar

Collect public job listings from RSS feeds you choose, rank them against a short skills list, and export a CSV report. The tool does not scrape logged-in job platforms or bypass access controls.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
job-radar --feed https://example.com/jobs.rss --skills python,sql,git --output jobs.csv
```

Feeds differ in the fields they provide; missing company, location, or description values are left blank. Check the source site's terms before polling it and set a reasonable schedule. The skill score is a transparent keyword count, not a hiring recommendation.

## Learning notes

This project practices RSS/XML parsing, text normalization, stable IDs, keyword scoring, CSV output, and keeping network access behind an explicit command-line option.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
