#!/usr/bin/env python3

import json
import subprocess
from datetime import datetime
from pathlib import Path

ALLOWLIST = Path.home() / ".hermes" / "github_allowed_repos.txt"

def run(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "command failed")
    return result.stdout.strip()

def main():
    today = datetime.now().astimezone().strftime("%Y-%m-%d")

    if not ALLOWLIST.exists():
        print(json.dumps({
            "error": "GitHub allowlist does not exist",
            "path": str(ALLOWLIST)
        }))
        return

    repos = [
        line.strip()
        for line in ALLOWLIST.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]

    output = {
        "date": today,
        "repositories": []
    }

    for repo in repos:
        try:
            raw = run([
                "gh", "api", "-X", "GET",
                f"repos/{repo}/commits",
                "-f", f"since={today}T00:00:00+05:30",
                "-f", f"until={today}T23:59:59+05:30",
                "--paginate"
            ])

            commits = json.loads(raw) if raw else []

            repo_data = {
                "repository": repo,
                "commits": []
            }

            for commit in commits:
                sha = commit["sha"]

                detail_raw = run([
                    "gh", "api", "-X", "GET",
                    f"repos/{repo}/commits/{sha}"
                ])

                detail = json.loads(detail_raw)

                repo_data["commits"].append({
                    "sha": sha,
                    "message": detail["commit"]["message"].split("\n")[0],
                    "author": detail["commit"]["author"]["name"],
                    "files": [
                        {
                            "filename": f["filename"],
                            "status": f["status"],
                            "additions": f["additions"],
                            "deletions": f["deletions"]
                        }
                        for f in detail.get("files", [])
                    ],
                    "stats": detail.get("stats", {})
                })

            output["repositories"].append(repo_data)

        except Exception as e:
            output["repositories"].append({
                "repository": repo,
                "error": str(e)
            })

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
