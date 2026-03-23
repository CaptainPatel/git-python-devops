import json
from pathlib import Path
import requests

BASE_URL = "https://api.github.com"


def fetch_repos(user):
    url = f"{BASE_URL}/users/{user}/repos"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def build_report(repos):
    report = {
        "total_repos": len(repos),
        "repo_names": [],
        "top_repo_by_stars": None
    }

    # TODO 1: fill repo_names with repository names

    report["repo_names"] = [repo["name"] for repo in repos]

    # TODO 2: find the repo with the highest stargazers_count

    if repos:
        max_count = -1
        top_repo = None
        for repo in repos:
            if repo["stargazers_count"] > max_count:
                max_count = repo["stargazers_count"]
                top_repo = repo

        report["top_repo_by_stars"] = {
            "name": top_repo["name"],
            "url": top_repo["html_url"],
            "stars": top_repo["stargazers_count"]
        }

    # TODO 3: store only a small summary for top_repo_by_stars

    return report


def write_report(report, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def main():
    user = "torvalds"
    repos = fetch_repos(user)
    report = build_report(repos)
    write_report(report, "reports/github_report.json")


if __name__ == "__main__":
    main()
