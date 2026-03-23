# Ian-bug GitHub Profile

This repository automatically updates your GitHub profile README with dynamic data including your repositories, statistics, and recent activity.

## ✨ Features

- 🔄 **Auto-Updates**: Automatically updates every 6 hours via GitHub Actions
- 📊 **GitHub Stats**: Displays follower count, repository count, and following count
- 🚀 **Pinned Repos**: Showcases your pinned repositories from GitHub
- ⭐ **Repository Details**: Shows description, stars, forks, and primary language
- 🔥 **Recent Activity**: Displays recent commit activity across your repositories
- 📈 **Profile Views**: Includes a visitor counter
- 🎨 **Beautiful Stats Cards**: Uses GitHub Readme Stats for visual statistics

## 🛠️ Setup

### 1. Clone this repository to your GitHub account

If this is already your profile repository, skip to step 2.

### 2. Enable GitHub Actions

Make sure GitHub Actions are enabled for this repository:
- Go to Settings > Actions > General
- Under "Actions permissions", select "Allow all actions and reusable workflows"

### 3. Set Up GitHub Personal Access Token (PAT)

The workflow requires a Personal Access Token to fetch data and push changes:

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Profile README Update")
4. Select the following scopes:
   - `repo` (full control of private repositories)
   - `workflow` (update GitHub Action workflows)
5. Generate the token and copy it
6. In your repository, go to Settings > Secrets and variables > Actions
7. Click "New repository secret"
8. Name: `GH_PAT`
9. Value: Paste the token you created
10. Click "Add secret"

⚠️ **Important**: Keep your token secure and never commit it to the repository.

### 4. Verify Permissions

The workflow file already includes the necessary permissions:
```yaml
permissions:
  contents: write
```

### 5. Manually Trigger First Update

You can trigger the workflow manually to generate the initial README:
- Go to Actions tab
- Select "Update GitHub Profile README"
- Click "Run workflow" button

Or push any change to the main branch to trigger it automatically.

## 📝 Customization

### Modify Displayed Repositories

The script displays your **top repositories** (up to 6) fetched via GitHub CLI. To change which repos appear:
1. The script currently fetches your most recently updated repositories
2. To display specific repositories, modify the `fetch_github_data()` function
3. Or star/fork more active repositories to influence the sort order

### Change Username

The username can be configured via the `GITHUB_USERNAME` environment variable:

**Option 1: Environment Variable (Recommended)**
- Set `GITHUB_USERNAME` in the workflow:
```yaml
env:
  GITHUB_USERNAME: your-username
  GH_TOKEN: ${{ secrets.GH_PAT }}
```

**Option 2: Hardcode in Script**
- Replace the default value in `.github/scripts/update_readme.py`:
```python
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', 'your-username')
```

### Update Schedule

Edit `.github/workflows/update-readme.yml`:
```yaml
schedule:
  # Run every 6 hours (change as needed)
  - cron: '0 */6 * * *'
```

Common schedules:
- `0 * * * *` - Every hour
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Once daily at midnight
- `0 0 * * 0` - Once weekly on Sunday

### Customize README Template

Edit the `generate_readme()` function in `.github/scripts/update_readme.py` to modify:
- Section headers
- Layout
- Additional information
- Social links

## 📁 Files

```
.
├── .github/
│   ├── workflows/
│   │   └── update-readme.yml    # GitHub Actions workflow
│   └── scripts/
│       └── update_readme.py     # Python script to fetch data and generate README
├── README.md                     # Your profile README (auto-generated)
└── this file
```

## 🚀 How It Works

1. **GitHub Actions Trigger**: Runs every 6 hours or on manual dispatch
2. **Fetch Data**: Uses GitHub CLI (`gh` command) to fetch:
   - Your top repositories (by recent activity)
   - User statistics (followers, following, repo count)
   - Recent public activity events
3. **Generate README**: Python script creates markdown with:
   - Profile statistics
   - Top repositories with details
   - Recent activity
   - Visual stats cards from GitHub Readme Stats
4. **Commit & Push**: Automatically pulls latest changes, commits, and pushes updates

## 📊 Included Metrics

### GitHub Stats Cards
- Total contributions
- Total stars earned
- Total PRs created
- Code review stats
- Top languages

### Custom Metrics
- Repository count
- Follower count
- Following count
- Recent public activity events
- Top repositories with:
  - Description
  - Star count
  - Fork count
  - Primary language

## 🎨 External Services Used

- **GitHub Readme Stats**: For beautiful stats cards
- **Visitor Counter**: For profile view tracking
- **GitHub API**: For fetching repository and user data

## 🤝 Contributing

Feel free to fork this repository and customize it for your own GitHub profile!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Inspired by various GitHub profile auto-update solutions
- GitHub Readme Stats for the awesome stats cards
- GitHub Actions for automation

---

**Note**: The README.md file in this repository is automatically generated. Do not edit it manually as your changes will be overwritten by the automation script. Instead, edit the `.github/scripts/update_readme.py` file to customize the template.
