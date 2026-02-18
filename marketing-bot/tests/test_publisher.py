"""Tests for the publisher module and platform API clients."""

import pytest
from unittest.mock import MagicMock, patch

from src.pipeline.publisher import Publisher
from src.integrations.linkedin_api import LinkedInAPI
from src.integrations.twitter_api import TwitterAPI
from src.db.models import Content


class TestPublisher:

    @pytest.fixture
    def publisher(self):
        linkedin = LinkedInAPI(mock_mode=True)
        twitter = TwitterAPI(mock_mode=True)
        return Publisher(linkedin_api=linkedin, twitter_api=twitter)

    def test_publish_linkedin(self, publisher):
        content = Content(
            id=1, content_type="linkedin_post", platform="linkedin",
            body="Test LinkedIn post", status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is True
        assert result["platform"] == "linkedin"
        assert "post_id" in result

    def test_publish_tweet(self, publisher):
        content = Content(
            id=1, content_type="tweet", platform="twitter",
            body="Test tweet", status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is True
        assert result["platform"] == "twitter"

    def test_publish_thread(self, publisher):
        content = Content(
            id=1, content_type="tweet_thread", platform="twitter",
            body="1/ First tweet\n\n2/ Second tweet\n\n3/ Third tweet",
            status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is True
        assert result["tweet_count"] == 3

    def test_publish_unsupported_platform(self, publisher):
        content = Content(
            id=1, content_type="blog", platform="blog",
            body="Test blog", status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is False
        assert "not supported" in result["error"]

    def test_publish_without_linkedin_api(self):
        publisher = Publisher(twitter_api=TwitterAPI(mock_mode=True))
        content = Content(
            id=1, content_type="linkedin_post", platform="linkedin",
            body="Test", status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is False
        assert "not configured" in result["error"]

    def test_publish_without_twitter_api(self):
        publisher = Publisher(linkedin_api=LinkedInAPI(mock_mode=True))
        content = Content(
            id=1, content_type="tweet", platform="twitter",
            body="Test", status="approved",
        )
        result = publisher.publish(content)
        assert result["success"] is False
        assert "not configured" in result["error"]


class TestLinkedInAPIMock:

    def test_get_profile_mock(self):
        api = LinkedInAPI(mock_mode=True)
        profile = api.get_profile()
        assert "id" in profile
        assert "name" in profile

    def test_create_post_mock(self):
        api = LinkedInAPI(mock_mode=True)
        result = api.create_post("Test LinkedIn post content")
        assert result["success"] is True
        assert result["platform"] == "linkedin"

    def test_get_metrics_mock(self):
        api = LinkedInAPI(mock_mode=True)
        metrics = api.get_post_metrics("mock_id")
        assert "impressions" in metrics
        assert "likes" in metrics


class TestTwitterAPIMock:

    def test_create_tweet_mock(self):
        api = TwitterAPI(mock_mode=True)
        result = api.create_tweet("Test tweet")
        assert result["success"] is True
        assert result["platform"] == "twitter"

    def test_create_thread_mock(self):
        api = TwitterAPI(mock_mode=True)
        thread = "1/ First\n\n2/ Second\n\n3/ Third"
        result = api.create_thread(thread)
        assert result["success"] is True
        assert result["tweet_count"] == 3

    def test_get_metrics_mock(self):
        api = TwitterAPI(mock_mode=True)
        metrics = api.get_tweet_metrics("mock_id")
        assert "impressions" in metrics
        assert "likes" in metrics

    def test_parse_thread_text(self):
        api = TwitterAPI(mock_mode=True)
        text = "1/ First tweet here\n\n2/ Second tweet here\n\n3/ Third tweet"
        tweets = api._parse_thread_text(text)
        assert len(tweets) == 3
        assert tweets[0].startswith("1/")

    def test_parse_thread_single_text(self):
        api = TwitterAPI(mock_mode=True)
        text = "Just a single tweet, no numbering"
        tweets = api._parse_thread_text(text)
        assert len(tweets) == 1
