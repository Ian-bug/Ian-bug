"""Unit tests for update_readme.py"""

import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime, timezone
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / ".github" / "scripts"))

from update_readme import (
    fetch_github_data,
    generate_repos_section,
    generate_activity_section,
    generate_readme,
)


class TestGenerateReposSection:
    """Test repository section generation"""

    def test_empty_repos(self):
        """Test with empty repository list"""
        result = generate_repos_section([])
        assert result == "No repositories found."

    def test_string_repos(self):
        """Test with string instead of list"""
        result = generate_repos_section("not a list")
        assert result == "No repositories found."

    def test_dict_repos(self):
        """Test with dict instead of list"""
        result = generate_repos_section({"repo": "data"})
        assert result == "No repositories found."

    def test_valid_repos(self):
        """Test with valid repository data"""
        repos = [
            {
                "name": "test-repo",
                "url": "https://github.com/test/test-repo",
                "description": "A test repository",
                "stargazerCount": 10,
                "forkCount": 5,
                "primaryLanguage": {"name": "Python"},
            }
        ]
        result = generate_repos_section(repos)
        assert "test-repo" in result
        assert "https://github.com/test/test-repo" in result
        assert "A test repository" in result
        assert "10 stars" in result
        assert "5 forks" in result
        assert "Python" in result

    def test_repo_without_description(self):
        """Test repository without description"""
        repos = [
            {
                "name": "test-repo",
                "url": "https://github.com/test/test-repo",
                "stargazerCount": 0,
                "forkCount": 0,
                "primaryLanguage": None,
            }
        ]
        result = generate_repos_section(repos)
        assert "No description" in result
        assert "Unknown" in result


class TestGenerateActivitySection:
    """Test activity section generation"""

    def test_empty_activity(self):
        """Test with empty activity list"""
        result = generate_activity_section([])
        assert result == "No recent activity."

    def test_valid_activity(self):
        """Test with valid activity data"""
        activity = [
            {
                "name": "test-repo",
                "url": "https://api.github.com/repos/test/test-repo",
                "created_at": "2024-01-15T10:30:00Z",
            }
        ]
        result = generate_activity_section(activity)
        assert "test-repo" in result
        assert "https://github.com/test/test-repo" in result
        assert "2024-01-15" in result

    def test_activity_api_url_conversion(self):
        """Test that API URLs are converted to web URLs"""
        activity = [
            {
                "name": "test-repo",
                "url": "https://api.github.com/repos/test/test-repo",
                "created_at": "2024-01-15T10:30:00Z",
            }
        ]
        result = generate_activity_section(activity)
        assert "api.github.com/repos" not in result
        assert "github.com/test/test-repo" in result

    def test_activity_date_parsing(self):
        """Test date parsing and formatting"""
        activity = [
            {
                "name": "test-repo",
                "url": "https://github.com/test/test-repo",
                "created_at": "2024-03-22T16:10:49Z",
            }
        ]
        result = generate_activity_section(activity)
        assert "2024-03-22" in result

    def test_activity_sorting(self):
        """Test that activities are sorted by date"""
        activity = [
            {
                "name": "repo1",
                "url": "https://github.com/test/repo1",
                "created_at": "2024-01-01T00:00:00Z",
            },
            {
                "name": "repo2",
                "url": "https://github.com/test/repo2",
                "created_at": "2024-01-02T00:00:00Z",
            },
        ]
        result = generate_activity_section(activity)
        # repo2 should come first (more recent)
        repo1_pos = result.index("repo1")
        repo2_pos = result.index("repo2")
        assert repo2_pos < repo1_pos


class TestGenerateReadme:
    """Test README generation"""

    def test_basic_generation(self):
        """Test basic README generation"""
        data = {
            "repos": [],
            "stats": {"public_repos": 10, "followers": 5, "following": 3},
            "activity": [],
        }
        result = generate_readme(data)
        assert "Hi there" in result
        assert "Total Repositories: 10" in result
        assert "Followers: 5" in result
        assert "Following: 3" in result
        assert "Last updated:" in result

    def test_with_repos_and_activity(self):
        """Test README with repos and activity"""
        data = {
            "repos": [
                {
                    "name": "test-repo",
                    "url": "https://github.com/test/test-repo",
                    "description": "Test",
                    "stargazerCount": 1,
                    "forkCount": 0,
                    "primaryLanguage": {"name": "Python"},
                }
            ],
            "stats": {"public_repos": 1, "followers": 0, "following": 0},
            "activity": [
                {
                    "name": "test-repo",
                    "url": "https://github.com/test/test-repo",
                    "created_at": "2024-01-01T00:00:00Z",
                }
            ],
        }
        result = generate_readme(data)
        assert "test-repo" in result
        assert "1 stars" in result
        assert "Pinned Repositories" in result


@patch("update_readme.run_command")
@patch("update_readme.fetch_pinned_repos")
class TestFetchGithubData:
    """Test GitHub data fetching"""

    def test_fetch_all_success(self, mock_fetch_repos, mock_run):
        """Test successful data fetching"""
        # Mock user stats and activity
        mock_run.side_effect = [
            json.dumps({"login": "testuser", "public_repos": 5, "followers": 10, "following": 3}),
            json.dumps(
                [
                    {
                        "name": "test-repo",
                        "url": "https://api.github.com/repos/test/test-repo",
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ]
            ),
        ]

        # Mock repos
        mock_fetch_repos.return_value = [
            {
                "name": "test-repo",
                "url": "https://github.com/test/test-repo",
                "description": "Test",
                "stargazerCount": 1,
                "forkCount": 0,
                "primaryLanguage": {"name": "Python"},
            }
        ]

        data = fetch_github_data()
        assert "repos" in data
        assert "stats" in data
        assert "activity" in data
        assert len(data["repos"]) == 1
        assert data["stats"]["public_repos"] == 5
        assert len(data["activity"]) == 1

    def test_fetch_with_json_error(self, mock_fetch_repos, mock_run):
        """Test handling of JSON parsing errors"""
        # Mock user stats with invalid JSON
        mock_run.side_effect = ["invalid json", "[]"]
        mock_fetch_repos.return_value = []

        data = fetch_github_data()
        assert "stats" in data
        assert data["stats"]["public_repos"] == 0  # Should use default values
        assert data["repos"] == []
        assert data["activity"] == []
