import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional


def run_command(cmd: str) -> str:
    """Run a command and return output with proper encoding"""
    env = os.environ.copy()
    # Ensure GH_TOKEN is available to subprocess
    if 'GH_TOKEN' not in env:
        env['GH_TOKEN'] = os.environ.get('GH_TOKEN', '')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', env=env)
    return result.stdout


def fetch_github_data() -> Dict[str, Any]:
    """Fetch GitHub data using gh CLI"""
    print("[DEBUG] Starting to fetch GitHub data...")

    # Fetch user stats (simpler query)
    user_stats_cmd = 'gh api user --jq "{login, public_repos, followers, following}"'
    user_stats: Dict[str, Any]
    try:
        user_stats = json.loads(run_command(user_stats_cmd))
        print(f"[DEBUG] User stats: {user_stats}")
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse user stats data: {e}")
        user_stats = {'login': 'Ian-bug', 'public_repos': 0, 'followers': 0, 'following': 0}

    # Fetch pinned repositories using GraphQL with proper formatting
    repos_cmd = r'gh api graphql -F login=Ian-bug -f query="query($login: String!) { user(login: $login) { pinnedItems(first: 6, types: REPOSITORY) { nodes { name description url stargazerCount forkCount primaryLanguage { name } } } } }" --jq ".data.user.pinnedItems.nodes"'
    result = run_command(repos_cmd)

    repos: List[Dict[str, Any]] = []
    try:
        repos = json.loads(result) if result else []
        if isinstance(repos, list) and len(repos) > 0:
            print(f"[OK] Fetched {len(repos)} pinned repositories")
        else:
            print(f"[WARNING] No repos found or invalid format. Type: {type(repos)}")
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse pinned repositories data: {e}")

    # Fetch recent activity (using events API) - simplified query
    activity_cmd = 'gh api users/Ian-bug/events/public --jq ".[:5] | map({name: .repo.name, url: .repo.url, created_at: .created_at}) | group_by(.name) | map({name: .[0].name, url: .[0].url, count: length, latest: .[0].created_at})"'
    activity: List[Dict[str, Any]] = []
    try:
        activity = json.loads(run_command(activity_cmd)) or []
        print(f"[OK] Fetched {len(activity)} activity items")
    except json.JSONDecodeError:
        print("Warning: Failed to parse activity data")
        activity = []

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
    for item in sorted(activity[:5], key=lambda x: str(x.get('latest', '')), reverse=True):
        name: str = item.get('name', 'Unknown')
        url: str = item.get('url', '#')
        count: int = item.get('count', 0)
        latest: str = item.get('latest', '')

        # Convert API URL to web URL
        if url and 'api.github.com/repos' in url:
            url = url.replace('api.github.com/repos', 'github.com')
        elif url and 'api.github.com/repos' not in url and 'github.com/' not in url:
            url = url.replace('github.com/', 'github.com/')

        # Format date nicely
        if latest:
            try:
                dt = datetime.fromisoformat(latest.replace('Z', '+00:00'))
                date_str: str = dt.strftime('%Y-%m-%d')
            except Exception:
                date_str = 'recently'
        else:
            date_str = 'recently'

        markdown += f"- [{name}]({url}) - {count} events (last: {date_str})\n"

    return markdown


def generate_readme(data: Dict[str, Any]) -> str:
    """Generate complete README content"""
    # Safely get repos with type checking
    repos: Any = data.get('repos', [])
    if not isinstance(repos, list):
        print(f"Warning: repos is not a list, got {type(repos)}")
        repos: Any = []

    repos_section: str = generate_repos_section(repos)
    activity_section: str = generate_activity_section(data.get('activity', []))
    updated_time: str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    readme = f"""## Hi there 👋 I'm Ian (also named as o6md, bk5x)

<img src="https://count.getloli.com/get/@Ian-bug?theme=rule34" alt="Profile Views" />

### 📊 Stats
<img src="https://github-readme-stats.vercel.app/api?username=Ian-bug&show_icons=true&theme=radical&hide_border=true" alt="GitHub Stats" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Ian-bug&layout=compact&theme=radical&hide_border=true" alt="Top Languages" />
<img src="https://github-readme-streak-stats.herokuapp.com?user=Ian-bug&theme=radical&hide_border=true" alt="GitHub Streak" />

---

![I Use Windows BTW](screenshot.png)

# I Use Windows BTW

### 🔥 Recent Activity

{activity_section}

### 🚀 Pinned Repositories

{repos_section}

### 🤝 Connect with Me

- 💼 GitHub: [Ian-bug](https://github.com/Ian-bug)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y01WG0DL)

### 📈 GitHub Overview
- 📦 Total Repositories: {data['stats'].get('public_repos', 0)}
- 👥 Followers: {data['stats'].get('followers', 0)}
- 🤝 Following: {data['stats'].get('following', 0)}

---
✨ Last updated: {updated_time}

<!--
**Ian-bug/Ian-bug** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

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
