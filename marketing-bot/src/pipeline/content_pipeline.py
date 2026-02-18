"""End-to-end content pipeline: generate → queue → approve → publish."""

from typing import Optional

from src.db.knowledge_base import KnowledgeBase
from src.db.models import ContentTask, ContentDraft
from src.agents.orchestrator import Orchestrator
from src.integrations.claude_client import ClaudeClient


class ContentPipeline:
    """Manages the full content lifecycle from generation to publishing."""

    def __init__(self, claude_client: ClaudeClient, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.orchestrator = Orchestrator(claude_client, knowledge_base)

    def generate_and_queue(self, task: ContentTask) -> int:
        """Generate content and add it to the review queue."""
        # Generate the draft
        draft = self.orchestrator.generate_content(task)

        # Validate brand compliance
        validation = self.orchestrator.validate_content(draft)

        # Save to database with appropriate status
        status = "queued" if validation["is_compliant"] else "draft"

        content_id = self.kb.add_content(
            content_type=draft.content_type,
            platform=draft.platform,
            body=draft.body,
            principal=draft.principal,
            title=draft.title,
            topic=draft.topic,
            status=status,
        )

        # If there's a linked calendar entry, update it
        if task.calendar_entry_id:
            self.kb.update_calendar_entry_status(
                task.calendar_entry_id, "generated", content_id=content_id
            )

        return content_id

    def approve(self, content_id: int) -> bool:
        """Approve content for publishing."""
        content = self.kb.get_content(content_id)
        if content is None:
            raise ValueError(f"Content {content_id} not found")
        if content.status not in ("draft", "queued"):
            raise ValueError(
                f"Cannot approve content with status '{content.status}'"
            )
        return self.kb.update_content_status(content_id, "approved")

    def reject(self, content_id: int, reason: Optional[str] = None) -> bool:
        """Reject content."""
        content = self.kb.get_content(content_id)
        if content is None:
            raise ValueError(f"Content {content_id} not found")
        return self.kb.update_content_status(content_id, "rejected")

    def publish(self, content_id: int, publisher=None,
                dry_run: bool = False) -> dict:
        """Publish approved content to the target platform."""
        content = self.kb.get_content(content_id)
        if content is None:
            raise ValueError(f"Content {content_id} not found")
        if content.status != "approved":
            raise ValueError(
                f"Cannot publish content with status '{content.status}'. "
                "Content must be approved first."
            )

        if dry_run:
            return {
                "status": "dry_run",
                "content_id": content_id,
                "platform": content.platform,
                "body_preview": content.body[:200],
            }

        if publisher is None:
            raise ValueError("Publisher required for actual publishing")

        # Publish via the appropriate platform client
        result = publisher.publish(content)

        if result.get("success"):
            self.kb.update_content_status(content_id, "published")
            if result.get("post_id"):
                self.kb.set_platform_post_id(content_id, result["post_id"])

        return result

    def edit_and_requeue(self, content_id: int, new_body: str,
                         new_title: Optional[str] = None) -> bool:
        """Edit rejected/draft content and requeue it."""
        content = self.kb.get_content(content_id)
        if content is None:
            raise ValueError(f"Content {content_id} not found")

        self.kb.update_content_body(content_id, new_body, title=new_title)
        return self.kb.update_content_status(content_id, "queued")

    def get_review_queue(self) -> list[dict]:
        """Get all content awaiting review."""
        queued = self.kb.get_content_by_status("queued")
        drafts = self.kb.get_content_by_status("draft")

        items = []
        for content in queued + drafts:
            validation = self.orchestrator.validate_content(
                ContentDraft(
                    content_type=content.content_type,
                    platform=content.platform,
                    body=content.body,
                    topic=content.topic or "",
                )
            )
            items.append({
                "id": content.id,
                "type": content.content_type,
                "platform": content.platform,
                "principal": content.principal,
                "status": content.status,
                "preview": content.body[:150],
                "is_compliant": validation["is_compliant"],
                "issues": validation["issues"],
                "created_at": content.created_at,
            })

        return items

    def plan_and_generate(self, days_ahead: int = 7,
                          instructions: str = "") -> list[int]:
        """Let the orchestrator plan content and generate all pieces."""
        tasks = self.orchestrator.plan_content(
            days_ahead=days_ahead,
            instructions=instructions,
        )
        content_ids = []
        for task in tasks:
            content_id = self.generate_and_queue(task)
            content_ids.append(content_id)
        return content_ids
