# Ian-bug

Auto-updating GitHub profile with dynamic data fetched via GitHub Actions.

## What This Does

This repository automatically updates your GitHub profile README (`README.md`) with:
- 📊 Your GitHub statistics (followers, following, repository count)
- 🚀 Your pinned repositories from GitHub
- ⭐ Repository details (description, stars, forks, language)
- 🔥 Recent activity
- 📈 Visual statistics cards
- 👤 Profile view counter

## How It Works

1. **GitHub Actions** runs every 6 hours (or manually triggered)
2. Uses **GitHub CLI** to fetch your latest data
3. A **Python script** generates a new README with up-to-date information
4. Changes are automatically committed and pushed

## Quick Start

1. This workflow is already set up in `.github/workflows/update-readme.yml`
2. Enable GitHub Actions in your repository settings
3. Trigger the workflow manually from the Actions tab
4. Your profile README will auto-update every 6 hours

## Customization

### Change Your Username
Edit `.github/scripts/update_readme.py` and replace `Ian-bug` with your GitHub username in:
- GraphQL query login parameter
- Profile view counter URL
- Stats cards URLs

### Change Update Frequency
Edit `.github/workflows/update-readme.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Change this line
```

### Modify Displayed Repositories
The script displays your **pinned repositories** from GitHub. To change which repos appear:
1. Go to your GitHub profile
2. Customize your profile pins
3. Pin/unpin up to 6 repositories
4. Changes appear after the next auto-update

### Customize the README Template
Edit the `generate_readme()` function in `.github/scripts/update_readme.py` to change:
- Section titles
- Layout
- Add/remove sections
- Change formatting

## Files

- `.github/workflows/update-readme.yml` - GitHub Actions workflow
- `.github/scripts/update_readme.py` - Python script that fetches data
- `SETUP.md` - Detailed setup instructions

## Manual Update

To update your README immediately:
1. Go to Actions tab in GitHub
2. Select "Update GitHub Profile README"
3. Click "Run workflow"

Or push any change to the main branch.

## Troubleshooting

**Workflow not running?**
- Check Actions are enabled in repository settings
- Verify the workflow file is in `.github/workflows/`

**Data not updating?**
- Check the workflow logs for errors
- Ensure GitHub CLI has proper permissions
- Try manually triggering the workflow

## Note

⚠️ **Do not manually edit the README.md file** - it will be overwritten by the automation. Make changes to the Python script instead.

---

**Last auto-update:** See the timestamp at the bottom of your README
