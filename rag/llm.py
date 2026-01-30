from typing import List, Dict, Any, Optional
from openai import OpenAI

from .config import settings
from .tools import create_github_issue, CREATE_TICKET_TOOL

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

def run_chat_with_tools(
    system_prompt: str,
    messages: List[Dict[str, str]],
    tools: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Calls OpenAI chat completion with function calling (tools).
    messages: list of {role: user|assistant, content: "..."}
    Returns a dict with:
      - "final_text"
      - "tool_result" (optional)
    """
    if client is None:
        return {"final_text": "OPENAI_API_KEY is not set. Add it in HF Spaces secrets or a local .env file."}

    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        tools=tools or [],
        tool_choice="auto" if tools else "none",
        temperature=0.2,
    )

    msg = resp.choices[0].message

    # If tool called:
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        if tool_call.function.name == "create_support_ticket":
            args = tool_call.function.arguments
            # arguments is JSON string in OpenAI SDK
            import json
            payload = json.loads(args)
            result = create_github_issue(**payload)

            # Follow up to model with tool result for a nice user-facing confirmation
            follow = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages,
                    {"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls},
                    {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)},
                ],
                temperature=0.2,
            )
            final_text = follow.choices[0].message.content or ""
            return {"final_text": final_text, "tool_result": result}

    return {"final_text": msg.content or ""}
