"""Content templates and user prompt builders for each agent."""


def build_linkedin_prompt(topic: str, principal: str, context: dict,
                          instructions: str = "") -> str:
    """Build the user prompt for LinkedIn post generation."""
    context_text = _format_context(context)

    return f"""Create a LinkedIn post about: {topic}

This post will be published on {_principal_name(principal)}'s LinkedIn profile.

{f"Additional instructions: {instructions}" if instructions else ""}

## KNOWLEDGE BASE CONTEXT
{context_text}

Write the post now. Include hashtags at the end."""


def build_twitter_prompt(topic: str, principal: str, context: dict,
                         thread: bool = False,
                         instructions: str = "") -> str:
    """Build the user prompt for Twitter content generation."""
    context_text = _format_context(context)
    format_type = "a Twitter thread (3-7 tweets)" if thread else "a single tweet (max 280 characters)"

    return f"""Create {format_type} about: {topic}

This will be posted from {_principal_name(principal)}'s account.

{f"Additional instructions: {instructions}" if instructions else ""}

## KNOWLEDGE BASE CONTEXT
{context_text}

Write the {"thread" if thread else "tweet"} now."""


def build_blog_prompt(topic: str, context: dict,
                      instructions: str = "") -> str:
    """Build the user prompt for blog article generation."""
    context_text = _format_context(context)

    return f"""Write a blog article about: {topic}

The article should be 800-1200 words and will be published on the RC Investment Properties website.

{f"Additional instructions: {instructions}" if instructions else ""}

## KNOWLEDGE BASE CONTEXT
{context_text}

Write the article now in HTML format."""


def build_market_report_prompt(market: str, period: str, context: dict,
                               instructions: str = "") -> str:
    """Build the user prompt for market report generation."""
    context_text = _format_context(context)

    return f"""Create a market update report for: {market.title()} - {period}

This report will be distributed to RC Investment Properties' investors and prospects.

{f"Additional instructions: {instructions}" if instructions else ""}

## KNOWLEDGE BASE CONTEXT
{context_text}

Write the report now in Markdown format."""


def build_orchestrator_prompt(calendar_status: str, recent_content: str,
                              market_data: str, instructions: str = "") -> str:
    """Build the user prompt for the orchestrator's planning task."""
    return f"""Plan the upcoming content for RC Investment Properties.

## CURRENT CALENDAR STATUS
{calendar_status}

## RECENTLY PUBLISHED CONTENT
{recent_content}

## LATEST MARKET DATA
{market_data}

{f"Additional instructions: {instructions}" if instructions else ""}

Suggest 3-5 content pieces to create. For each, provide:
- content_type (linkedin_post, tweet, tweet_thread, blog, market_report)
- platform (linkedin, twitter, blog, report)
- topic (specific, data-driven topic)
- principal (michael, bradley, or company)
- instructions (specific guidance for the content creator)

Return as a JSON array."""


def _format_context(context: dict) -> str:
    """Format knowledge base context into a readable string."""
    parts = []

    if context.get("firm_facts"):
        parts.append("### Firm Facts")
        for fact in context["firm_facts"]:
            parts.append(f"- {fact.get('key', '')}: {fact.get('value', '')}")

    if context.get("market_data"):
        parts.append("\n### Market Data")
        for data in context["market_data"]:
            source = f" (Source: {data['source']})" if data.get("source") else ""
            period = f" [{data['period']}]" if data.get("period") else ""
            parts.append(
                f"- {data.get('market', '').title()} {data.get('metric', '')}: "
                f"{data.get('value', '')}{period}{source}"
            )

    if context.get("brand_rules"):
        parts.append("\n### Brand Rules")
        for rule in context["brand_rules"]:
            parts.append(f"- [{rule.get('rule_type', '')}] {rule.get('rule', '')}")

    if context.get("recent_content"):
        parts.append("\n### Recently Created Content (avoid repetition)")
        for content in context["recent_content"]:
            body_preview = content.get("body", "")[:100]
            parts.append(
                f"- [{content.get('content_type', '')}] {body_preview}..."
            )

    if context.get("inspiration"):
        parts.append("\n### Inspiration (content the principals liked recently)")
        parts.append("Use these as style/topic inspiration — don't copy, but draw from the themes and formats:")
        for insp in context["inspiration"]:
            author = insp.get("author", "Unknown")
            body = (insp.get("body") or "")[:150]
            notes = insp.get("notes", "")
            source = insp.get("source_type", "")
            entry = f"- [{source}] {author}: {body}"
            if notes:
                entry += f" (Note: {notes})"
            parts.append(entry)

    return "\n".join(parts) if parts else "No context available."


def _principal_name(principal: str) -> str:
    """Convert principal key to full name."""
    names = {
        "michael": "Michael Rosen",
        "bradley": "Bradley Couch",
        "company": "RC Investment Properties",
    }
    return names.get(principal, principal or "RC Investment Properties")
