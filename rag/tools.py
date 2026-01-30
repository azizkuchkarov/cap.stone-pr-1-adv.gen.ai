import requests
from typing import Dict, Any
from .config import settings

def create_github_issue(user_name: str, user_email: str, summary: str, description: str) -> Dict[str, Any]:
    """
    Creates a GitHub Issue in the repo settings.GITHUB_REPO using settings.GITHUB_TOKEN.
    """
    if not settings.GITHUB_TOKEN or not settings.GITHUB_REPO:
        return {
            "ok": False,
            "error": "GitHub integration not configured. Set GITHUB_TOKEN and GITHUB_REPO."
        }

    url = f"https://api.github.com/repos/{settings.GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    body = {
        "title": summary,
        "body": f"**User:** {user_name}\n**Email:** {user_email}\n\n{description}"
    }

    r = requests.post(url, headers=headers, json=body, timeout=30)
    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
        return {"ok": True, "issue_url": data.get("html_url", ""), "issue_number": data.get("number")}
    return {"ok": False, "error": f"GitHub API error {r.status_code}: {r.text[:300]}"}

# Tool schema for OpenAI function calling
CREATE_TICKET_TOOL = {
    "type": "function",
    "function": {
        "name": "create_support_ticket",
        "description": "Create a customer support ticket in the issue tracking system.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_name": {"type": "string"},
                "user_email": {"type": "string"},
                "summary": {"type": "string", "description": "Short title of the issue"},
                "description": {"type": "string", "description": "Detailed description, steps, context"}
            },
            "required": ["user_name", "user_email", "summary", "description"]
        }
    }
}
