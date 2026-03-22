import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional


def run_command(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.stdout


def fetch_github_data() -> Dict[str, Any]:
    repos_cmd = 'gh api graphql --jq ".data.user.pinnedItems.nodes" -f query=' + "'"query($login: String!) { user(login: $login) { pinnedItems(first: 6, types: REPOSITORY) { nodes { ... on Repository { name description url stargazerCount forkCount primaryLanguage { name } } } } }" + "' " + '-F login=Ian-bug'
    result = run_command(repos_cmd)

    repos = []
    try:
        repos = json.loads(result) if result else []
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse: {e}")

    user_stats_cmd = 'gh api user --jq "{login, public_repos, followers, following}"'
    user_stats = {}
    try:
        user_stats = json.loads(run_command(user_stats_cmd))
    except json.JSONDecodeError:
        user_stats = {'login': 'Ian-bug', 'public_repos': 0, 'followers': 0, 'following': 0}

    activity_cmd = 'gh api users/Ian-bug/events/public --jq ".[:10] | map({name: .repo.name, url: .repo.url, type: .type, created_at: .created_at}) | group_by(.name) | map({name: .[0].name, url: .[0].url, count: length, latest: (.[0].created_at})"'
    activity = []
    try:
        activity = json.loads(run_command(activity_cmd)) or []
    except json.JSONDecodeError:
        pass

    return {'repos': repos, 'stats': user_stats, 'activity': activity}


def generate_repos_section(repos):
    if not repos:
        return "No repositories found."
    if not isinstance(repos, list):
        return "No repositories found."

    markdown = ""
    for repo in repos:
        if not isinstance(repo, dict):
            continue
        name = repo.get('name', 'Unknown')
        url = repo.get('url', '#')
        desc = repo.get('description') or 'No description'
        stars = repo.get('stargazerCount', 0)
        forks = repo.get('forkCount', 0)
        primary_lang = repo.get('primaryLanguage')
        lang = primary_lang.get('name', 'Unknown') if primary_lang else 'Unknown'
        markdown += f"- [{name}]({url}) - {desc}\n"
        markdown += f"  - ⭐ {stars} stars | 🍴 {forks} forks | 🔷 {lang}\n"

    return markdown


def generate_activity_section(activity):
    if not activity:
        return "No recent activity."
    markdown = ""
    for item in sorted(activity[:5], key=lambda x: str(x.get('latest', '')), reverse=True):
        name = item.get('name', 'Unknown')
        url = item.get('url', '#')
        count = item.get('count', 0)
        latest = item.get('latest', '')
        if url and 'api.github.com/repos' in url:
            url = url.replace('api.github.com/repos', 'github.com')
        if latest:
            try:
                dt = datetime.fromisoformat(latest.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = 'recently'
        else:
            date_str = 'recently'
        markdown += f"- [{name}]({url}) - {count} events (last: {date_str})\n"

    return markdown


def generate_readme(data):
    repos = data.get('repos', [])
    repos_section = generate_repos_section(repos)
    activity_section = generate_activity_section(data.get('activity', []))
    updated_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

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
"""
    return readme


if __name__ == '__main__':
    print("Fetching GitHub data...")
    data = fetch_github_data()
    print("Generating README...")
    readme_content = generate_readme(data)
    readme_path = Path('README.md')
    readme_path.write_text(readme_content, encoding='utf-8')
    print("README updated successfully!")
    print(f"Updated {len(data['repos'])} repositories")
    print(f"Updated {len(data['activity'])} activity items")
