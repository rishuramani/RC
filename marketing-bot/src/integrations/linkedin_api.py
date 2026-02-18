"""LinkedIn API client for posting content."""

from typing import Optional

import requests

from src.config import LINKEDIN_ACCESS_TOKEN


class LinkedInAPI:
    """Client for the LinkedIn API v2."""

    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self, access_token: Optional[str] = None,
                 mock_mode: bool = False):
        self._access_token = access_token or LINKEDIN_ACCESS_TOKEN
        self._mock_mode = mock_mode
        self._person_id: Optional[str] = None

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def get_profile(self) -> dict:
        """Get the authenticated user's profile."""
        if self._mock_mode:
            return {"id": "mock_user_id", "name": "Michael Rosen"}

        response = requests.get(f"{self.BASE_URL}/me", headers=self.headers)
        response.raise_for_status()
        data = response.json()
        self._person_id = data.get("id")
        return data

    def create_post(self, text: str) -> dict:
        """Create a text post on LinkedIn."""
        if self._mock_mode:
            return {
                "success": True,
                "post_id": "mock_linkedin_post_123",
                "platform": "linkedin",
            }

        if not self._person_id:
            self.get_profile()

        payload = {
            "author": f"urn:li:person:{self._person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }

        response = requests.post(
            f"{self.BASE_URL}/ugcPosts", headers=self.headers, json=payload
        )
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "post_id": data.get("id", ""),
            "platform": "linkedin",
        }

    def get_post_metrics(self, post_id: str) -> dict:
        """Get engagement metrics for a post."""
        if self._mock_mode:
            return {
                "impressions": 1500,
                "likes": 45,
                "comments": 8,
                "shares": 12,
                "clicks": 230,
            }

        response = requests.get(
            f"{self.BASE_URL}/socialActions/{post_id}",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()
