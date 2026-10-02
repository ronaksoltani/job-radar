import csv

from job_radar.radar import Listing, rank_listing, write_csv


def test_skill_matching_is_case_insensitive_and_counted_once():
    matched, score = rank_listing("Python engineer", "Build with SQL and Python", ["python", "SQL", "Docker"])
    assert matched == ("python", "SQL")
    assert score == 2


def test_csv_report_keeps_listing_fields(tmp_path):
    path = tmp_path / "reports" / "jobs.csv"
    write_csv([Listing("Python role", "Example Co", "Remote", "https://example.org/job", "today", ("python",), 1)], path)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        row = next(csv.DictReader(stream))
    assert row["company"] == "Example Co"
    assert row["matched_skills"] == "python"
