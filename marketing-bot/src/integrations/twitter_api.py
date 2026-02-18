"""Twitter/X API client for posting tweets and threads."""

from typing import Optional

import requests

from src.config import TWITTER_BEARER_TOKEN, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET


class TwitterAPI:
    """Client for the Twitter API v2."""

    BASE_URL = "https://api.twitter.com/2"

    def __init__(self, bearer_token: Optional[str] = None,
                 mock_mode: bool = False):
        self._bearer_token = bearer_token or TWITTER_BEARER_TOKEN
        self._mock_mode = mock_mode

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json",
        }

    def create_tweet(self, text: str) -> dict:
        """Create a single tweet."""
        if self._mock_mode:
            return {
                "success": True,
                "post_id": "mock_tweet_123",
                "platform": "twitter",
            }

        payload = {"text": text}
        response = requests.post(
            f"{self.BASE_URL}/tweets", headers=self.headers, json=payload
        )
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "post_id": data.get("data", {}).get("id", ""),
            "platform": "twitter",
        }

    def create_thread(self, thread_text: str) -> dict:
        """Create a tweet thread from numbered text."""
        tweets = self._parse_thread_text(thread_text)

        if self._mock_mode:
            return {
                "success": True,
                "post_id": "mock_thread_123",
                "platform": "twitter",
                "tweet_count": len(tweets),
            }

        if not tweets:
            return {"success": False, "error": "No tweets to post"}

        tweet_ids = []
        reply_to = None

        for tweet_text in tweets:
            payload = {"text": tweet_text}
            if reply_to:
                payload["reply"] = {"in_reply_to_tweet_id": reply_to}

            response = requests.post(
                f"{self.BASE_URL}/tweets", headers=self.headers, json=payload
            )
            response.raise_for_status()
            data = response.json()
            tweet_id = data.get("data", {}).get("id", "")
            tweet_ids.append(tweet_id)
            reply_to = tweet_id

        return {
            "success": True,
            "post_id": tweet_ids[0] if tweet_ids else "",
            "platform": "twitter",
            "tweet_count": len(tweet_ids),
            "tweet_ids": tweet_ids,
        }

    def get_tweet_metrics(self, tweet_id: str) -> dict:
        """Get engagement metrics for a tweet."""
        if self._mock_mode:
            return {
                "impressions": 2500,
                "likes": 30,
                "comments": 5,
                "shares": 15,
                "clicks": 120,
            }

        response = requests.get(
            f"{self.BASE_URL}/tweets/{tweet_id}",
            headers=self.headers,
            params={
                "tweet.fields": "public_metrics",
            },
        )
        response.raise_for_status()
        data = response.json()
        metrics = data.get("data", {}).get("public_metrics", {})

        return {
            "impressions": metrics.get("impression_count", 0),
            "likes": metrics.get("like_count", 0),
            "comments": metrics.get("reply_count", 0),
            "shares": metrics.get("retweet_count", 0) + metrics.get("quote_count", 0),
            "clicks": 0,  # Not available via basic API
        }

    def search_recent(self, query: str, max_results: int = 20) -> list[dict]:
        """Twitter API v2 search/recent endpoint."""
        if self._mock_mode:
            return [
                {
                    "id": f"mock_search_{i}",
                    "text": f"Sample tweet about {query} — multifamily market update #{i}",
                    "author_id": f"user_{i}",
                    "author_username": f"analyst_{i}",
                    "created_at": "2026-02-16T12:00:00Z",
                    "public_metrics": {
                        "like_count": 50 + i * 10,
                        "retweet_count": 15 + i * 3,
                        "reply_count": 5 + i,
                        "quote_count": 2 + i,
                        "impression_count": 2000 + i * 500,
                    },
                }
                for i in range(min(max_results, 5))
            ]

        params = {
            "query": query,
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "username",
        }
        response = requests.get(
            f"{self.BASE_URL}/tweets/search/recent",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        # Build author lookup from includes
        users = {}
        for user in data.get("includes", {}).get("users", []):
            users[user["id"]] = user.get("username", "")

        results = []
        for tweet in data.get("data", []):
            results.append({
                "id": tweet["id"],
                "text": tweet["text"],
                "author_id": tweet.get("author_id", ""),
                "author_username": users.get(tweet.get("author_id", ""), ""),
                "created_at": tweet.get("created_at", ""),
                "public_metrics": tweet.get("public_metrics", {}),
            })
        return results

    def get_user_tweets(self, username: str, max_results: int = 10) -> list[dict]:
        """Get recent tweets from a specific user."""
        if self._mock_mode:
            return [
                {
                    "id": f"mock_user_tweet_{i}",
                    "text": f"Latest insight from @{username} on CRE trends #{i}",
                    "author_id": "mock_user_id",
                    "author_username": username,
                    "created_at": "2026-02-16T10:00:00Z",
                    "public_metrics": {
                        "like_count": 100 + i * 20,
                        "retweet_count": 30 + i * 5,
                        "reply_count": 10 + i * 2,
                        "quote_count": 5 + i,
                        "impression_count": 5000 + i * 1000,
                    },
                }
                for i in range(min(max_results, 5))
            ]

        # First look up user ID
        user_response = requests.get(
            f"{self.BASE_URL}/users/by/username/{username}",
            headers=self.headers,
        )
        user_response.raise_for_status()
        user_data = user_response.json()
        user_id = user_data.get("data", {}).get("id")
        if not user_id:
            return []

        # Then get their tweets
        params = {
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,public_metrics",
        }
        response = requests.get(
            f"{self.BASE_URL}/users/{user_id}/tweets",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for tweet in data.get("data", []):
            results.append({
                "id": tweet["id"],
                "text": tweet["text"],
                "author_id": user_id,
                "author_username": username,
                "created_at": tweet.get("created_at", ""),
                "public_metrics": tweet.get("public_metrics", {}),
            })
        return results

    def _parse_thread_text(self, thread_text: str) -> list[str]:
        """Parse numbered thread text into individual tweets."""
        tweets = []
        current = []

        for line in thread_text.strip().split("\n"):
            stripped = line.strip()
            if stripped and stripped[0].isdigit() and "/" in stripped[:4]:
                if current:
                    tweets.append("\n".join(current).strip())
                current = [stripped]
            elif stripped:
                current.append(stripped)

        if current:
            tweets.append("\n".join(current).strip())

        return tweets if tweets else [thread_text.strip()]
