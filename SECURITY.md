# Security Policy

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| Latest  | ✅ Supported       |

## Security Best Practices

This repository uses automated GitHub Actions to update your profile README. Here are the security considerations:

### GitHub Token Permissions

The `update-readme.yml` workflow requires minimal permissions:

```yaml
permissions:
  contents: write
```

- **contents: write** - Required to commit and push README changes

### Personal Access Tokens (PAT)

The workflow uses a Personal Access Token (`GH_PAT`) for GitHub API access. To secure your PAT:

1. **Create a scoped PAT** with only necessary permissions:
   - `public_repo` (for public repositories)
   - `read:org` (if you need organization data)

2. **Store securely in repository secrets:**
   - Go to Repository Settings → Secrets and variables → Actions
   - Create a new secret named `GH_PAT`
   - Paste your PAT token

3. **Rotate tokens regularly:**
   - GitHub PATs can be set to expire
   - Update your secret when tokens expire

4. **Never commit tokens to the repository**
   - Keep tokens out of `.env` files
   - Don't include tokens in code or documentation

### Token Usage in Code

The script (`update_readme.py`) handles tokens securely:

```python
# Tokens are read from environment variables only
token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')

# Tokens are never logged or printed
# Token usage follows principle of least privilege
```

### External Dependencies

This project primarily uses Python's standard library. Current dependencies:

- **Standard Library**: `json`, `os`, `subprocess`, `urllib`, `datetime`, `pathlib`, `typing`
- **No external runtime dependencies** (security minimalism)

### API Rate Limits

The GitHub API has rate limits:
- Unauthenticated requests: 60/hour
- Authenticated requests: 5,000/hour

This workflow runs every 6 hours, staying well within limits when authenticated.

### Reporting Vulnerabilities

If you discover a security vulnerability:

1. **Do not open a public issue**
2. **Email the maintainer privately** (if contact info is available)
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

4. **Allow time for response** before disclosing publicly

### Common Security Concerns

#### Token Exposure in Logs

The workflow configuration ensures tokens are not exposed:
- Workflow logs are not set to print environment variables
- Secrets are masked in GitHub Actions logs

#### Man-in-the-Middle Attacks

The script uses:
- HTTPS for all API requests
- Built-in urllib.request with SSL verification

#### Code Injection

- User input is minimal (only GitHub username)
- No dynamic code execution
- All API responses are validated before use

## Best Practices for Forkers

If you fork this repository:

1. **Create your own PAT** - Don't share tokens
2. **Update secret name** if you change variable names
3. **Review workflow permissions** regularly
4. **Monitor repository access** in GitHub settings
5. **Enable branch protection rules** for main branch
6. **Require status checks** before merging

## Dependency Management

While this project has minimal dependencies, always:

1. **Keep dependencies updated**
2. **Review security advisories** for any new dependencies
3. **Use pinned versions** in requirements files
4. **Audit dependencies** regularly

## Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/security)
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Creating a Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Questions?

If you have security-related questions not covered here, please:
- Check the [Troubleshooting section](GUIDE.md#troubleshooting)
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development practices
- Open an issue with the "security" label
