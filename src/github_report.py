import json
import argparse
import sys
from pathlib import Path
import requests

BASE_URL = "https://api.github.com"


def fetch_repos(user):
    url = f"{BASE_URL}/users/{user}/repos"
    
    try:
        response = requests.get(url, timeout=10)
        # raise_for_status() will raise an HTTPError if the status code is 4xx or 5xx
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # sys.stderr.write writes to the standard error stream, separating errors from normal logs
        sys.stderr.write(f"Error fetching data for {user}: {e}\n")
        # sys.exit(1) tells the OS (or Jenkins/GitHub Actions) that this script failed
        sys.exit(1)
    
    return response.json()


def build_report(repos):
    report = {
        "total_repos": len(repos),
        "repo_names": [repo["name"] for repo in repos],
        "top_repo_by_stars": None
    }

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

    return report


def write_report(report, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def main():
    # Set up argparse to handle command-line arguments properly
    parser = argparse.ArgumentParser(description="Fetch GitHub user repos.")
    parser.add_argument("username", help="GitHub username to query")
    args = parser.parse_args()
    
    # Use the username passed from the command line
    user = args.username
    
    print(f"Fetching repositories for user: {user}...")
    repos = fetch_repos(user)
    
    # If the API returns an empty list, let the user know
    if not repos:
        print(f"Warning: No repositories found for user {user}.")
    
    report = build_report(repos)
    
    output_filename = f"reports/{user}_github_report.json"
    write_report(report, output_filename)
    print(f"Success! Report saved to {output_filename}")


if __name__ == "__main__":
    main()

