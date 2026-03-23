import json
import os
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

# Get username from environment variable or default to Ian-bug
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', 'Ian-bug')


def run_command(cmd: str) -> str:
    """Run a command and return output with proper encoding"""
    env = os.environ.copy()
    # Ensure GH_TOKEN is available to subprocess
    if 'GH_TOKEN' not in env:
        env['GH_TOKEN'] = os.environ.get('GH_TOKEN', '')
    if 'GITHUB_TOKEN' not in env:
        env['GITHUB_TOKEN'] = os.environ.get('GITHUB_TOKEN', '')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', env=env)
    return result.stdout


def fetch_pinned_repos() -> List[Dict[str, Any]]:
    """Fetch pinned repositories using GitHub GraphQL API directly"""
    query = '''query($login: String!) {
      user(login: $login) {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              description
              url
              stargazerCount
              forkCount
              primaryLanguage { name }
            }
          }
        }
      }
    }'''
    
    # Get token
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Warning: No GitHub token found, falling back to gh CLI")
        return []
    
    # Make GraphQL request
    url = 'https://api.github.com/graphql'
    data = json.dumps({'query': query, 'variables': {'login': GITHUB_USERNAME}}).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Ian-bug-profile-updater'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('data', {}).get('user', {}).get('pinnedItems', {}).get('nodes', [])
    except Exception as e:
        print(f"Warning: Failed to fetch pinned repos via GraphQL: {e}")
        return []


def fetch_github_data() -> Dict[str, Any]:
    print(f"[DEBUG] Starting to fetch GitHub data for {GITHUB_USERNAME}...")

    # 1. Fetch User Stats
    user_stats_cmd = f'gh api user --jq "{{login, public_repos, followers, following}}"'
    try:
        user_stats = json.loads(run_command(user_stats_cmd))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Warning: Failed to fetch user stats: {e}")
        user_stats = {'login': GITHUB_USERNAME, 'public_repos': 0, 'followers': 0, 'following': 0}

    # 2. Fetch Pinned Repositories using GraphQL API
    repos = fetch_pinned_repos()
    if not repos:
        print("Warning: No pinned repositories found via GraphQL")
    else:
        print(f"[OK] Fetched {len(repos)} pinned repositories")

    # 3. Fetch Recent Activity
    activity_cmd = f'gh api users/{GITHUB_USERNAME}/events/public --jq ".[:5] | map({{name: .repo.name, url: .repo.url, created_at: .created_at}})"'
    activity = []
    try:
        activity = json.loads(run_command(activity_cmd))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Warning: Failed to parse activity: {e}")

    return {
        'repos': repos,
        'stats': user_stats,
        'activity': activity
    }


def generate_repos_section(repos: Any) -> str:
    """Generate repositories section markdown"""
    # Type checking and handling
    if not repos:
        return "No repositories found."

    if isinstance(repos, str):
        print(f"Warning: repos is a string: {repos}")
        return "No repositories found."

    if not isinstance(repos, list):
        print(f"Warning: repos is not a list: {type(repos)}")
        return "No repositories found."

    markdown = ""
    for repo in repos:
        # Add defensive type checking for each repo
        if not isinstance(repo, dict):
            print(f"Warning: Skipping non-dict repo item: {type(repo)}")
            continue

        name: str = repo.get('name', 'Unknown')
        url: str = repo.get('url', '#')
        # Ensure URL uses HTTPS (GitHub GraphQL sometimes returns http://)
        if url and url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        desc: str = repo.get('description') or 'No description'
        stars: int = repo.get('stargazerCount', 0)
        forks: int = repo.get('forkCount', 0)
        primary_lang: Optional[Dict[str, str]] = repo.get('primaryLanguage')
        lang: str = primary_lang.get('name', 'Unknown') if primary_lang else 'Unknown'

        markdown += f"- [{name}]({url}) - {desc}\n"
        markdown += f"  - ⭐ {stars} stars | 🍴 {forks} forks | 🔷 {lang}\n"

    return markdown


def generate_activity_section(activity: List[Dict[str, Any]]) -> str:
    """Generate recent activity section markdown"""
    if not activity:
        return "No recent activity."

    markdown = ""
    # Sort by created_at in descending order (most recent first)
    for item in sorted(activity[:5], key=lambda x: x.get('created_at', ''), reverse=True):
        name: str = item.get('name', 'Unknown')
        url: str = item.get('url', '#')
        created_at: str = item.get('created_at', '')

        # Convert API URL to web URL
        if url and 'api.github.com/repos' in url:
            url = url.replace('api.github.com/repos', 'github.com')
        # Ensure URL uses HTTPS
        if url and url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)

        # Format date nicely
        date_str = 'recently'
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError) as e:
                print(f"Warning: Failed to parse date '{created_at}': {e}")
                date_str = 'recently'

        markdown += f"- [{name}]({url}) - last activity: {date_str}\n"

    return markdown


def generate_readme(data: Dict[str, Any]) -> str:
    """Generate complete README content"""
    # Safely get repos with type checking
    repos: Any = data.get('repos', [])
    if not isinstance(repos, list):
        print(f"Warning: repos is not a list, got {type(repos)}")
        repos = []

    repos_section: str = generate_repos_section(repos)
    activity_section: str = generate_activity_section(data.get('activity', []))
    updated_time: str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    readme = f"""## Hi there 👋 I'm Ian (also named as o6md, bk5x)

<img src="https://count.getloli.com/get/@{GITHUB_USERNAME}?theme=rule34" alt="Profile Views" />

### 📊 Stats
<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&show_icons=true&theme=radical&hide_border=true" alt="GitHub Stats" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&layout=compact&theme=radical&hide_border=true" alt="Top Languages" />
<img src="https://github-readme-streak-stats.herokuapp.com?user={GITHUB_USERNAME}&theme=radical&hide_border=true" alt="GitHub Streak" />

---

# I Use Windows BTW

![I Use Windows BTW](screenshot.png)

### 🔥 Recent Activity

{activity_section}

### 🚀 Pinned Repositories

{repos_section}

### 🤝 Connect with Me

- 💼 GitHub: [{GITHUB_USERNAME}](https://github.com/{GITHUB_USERNAME})

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y01WG0DL)

### 📈 GitHub Overview
- 📦 Total Repositories: {data['stats'].get('public_repos', 0)}
- 👥 Followers: {data['stats'].get('followers', 0)}
- 🤝 Following: {data['stats'].get('following', 0)}

---
✨ Last updated: {updated_time}

<!--
**{GITHUB_USERNAME}/{GITHUB_USERNAME}** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I'm currently working on ...
- 🌱 I'm currently learning ...
- 👯 I'm looking to collaborate on ...
- 🤔 I'm looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
"""
    return readme


if __name__ == '__main__':
    print("Fetching GitHub data...")
    data = fetch_github_data()

    print("Generating README...")
    readme_content: str = generate_readme(data)

    readme_path: Path = Path('README.md')
    readme_path.write_text(readme_content, encoding='utf-8')

    print("README updated successfully!")
    print(f"Updated {len(data['repos'])} repositories")
    print(f"Updated {len(data['activity'])} activity items")
