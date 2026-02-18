"""Anthropic Claude API wrapper for RC Marketing Bot."""

import time
from typing import Optional

import anthropic

from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL


class ClaudeClient:
    """Wrapper around the Anthropic SDK with retry logic and usage tracking."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._api_key = api_key or ANTHROPIC_API_KEY
        self._model = model or CLAUDE_MODEL
        self._client: Optional[anthropic.Anthropic] = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_calls = 0

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        max_retries: int = 3,
    ) -> str:
        """Generate content using Claude API with retry logic."""
        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self._model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )

                self.total_input_tokens += response.usage.input_tokens
                self.total_output_tokens += response.usage.output_tokens
                self.total_calls += 1

                return response.content[0].text

            except anthropic.RateLimitError as e:
                last_error = e
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            except anthropic.APIError as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)

        raise last_error

    def get_usage_stats(self) -> dict:
        """Return cumulative usage statistics."""
        return {
            "total_calls": self.total_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
        }
