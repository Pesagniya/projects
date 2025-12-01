import argparse
import json
from urllib import request, error


def fetch_json(url):
    try:
        with request.urlopen(url) as response:
            if response.status == 200:
                return json.loads(response.read())
            else:
                return None
    except:
        return None


def fetch_github_events(username):
    """Fetch public events for a GitHub user."""
    url = f"https://api.github.com/users/{username}/events"
    return fetch_json(url) or []


def get_commit_count_for_push(repo_name, before_sha, head_sha):
    """
    Uses the GitHub compare API:
    /repos/:owner/:repo/compare/:before...:head
    """
    try:
        owner, repo = repo_name.split("/")
    except ValueError:
        return None

    compare_url = (
        f"https://api.github.com/repos/{owner}/{repo}/compare/{before_sha}...{head_sha}"
    )

    data = fetch_json(compare_url)
    if not data or "commits" not in data:
        return None

    return len(data["commits"])


def format_event(event):
    """Convert event JSON into readable text."""
    event_type = event.get("type")
    repo = event.get("repo", {}).get("name", "unknown/repo")

    match event_type:

        case "PushEvent":
            payload = event.get("payload", {})
            before = payload.get("before")
            head = payload.get("head")

            commit_count = get_commit_count_for_push(repo, before, head)

            if commit_count is not None:
                return f"Pushed {commit_count} commits to {repo}"
            else:
                return f"Pushed to {repo}"

        case "IssuesEvent":
            action = event["payload"].get("action", "updated")
            return f"{action.capitalize()} an issue in {repo}"

        case "WatchEvent":
            return f"Starred {repo}"

        case "ForkEvent":
            return f"Forked {repo}"

        case "CreateEvent":
            ref_type = event["payload"].get("ref_type", "item")
            return f"Created a new {ref_type} in {repo}"

        case "PullRequestEvent":
            action = event["payload"].get("action", "updated")
            return f"{action.capitalize()} a pull request in {repo}"
        
        case "IssueCommentEvent":
            action = event["payload"].get("action", "commented on")
            issue = event["payload"].get("issue", {})
            number = issue.get("number", "?")
            return f"{action.capitalize()} a comment on issue #{number} in {repo}"


def main():
    parser = argparse.ArgumentParser(
        prog="github-activity",
        description="GitHub Activity Tracker CLI"
    )
    parser.add_argument("username", help="GitHub username to track")
    args = parser.parse_args()

    events = fetch_github_events(args.username)

    if not events:
        print("No events found.")
        return

    for event in events:
        print("- " + format_event(event))


if __name__ == "__main__":
    main()
