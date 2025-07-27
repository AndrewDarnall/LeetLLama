""" History Windowed Parsing and Summarization """
from typing import List, Dict


def summarize_message_history(
    history: List[Dict], 
    max_chars: int = 95000  # ≈ 80% of 32K tokens × 4
) -> str:
    """
    Summarizes conversation history, fitting roughly within a token budget
    using character-based approximation (no tokenizer).
    """
    conversation = [msg for msg in history if msg["role"] in {"user", "assistant"}]

    summary_lines = []
    total_chars = 0

    # Start from the end and collect backwards until we hit char budget
    for i in range(len(conversation) - 2, -1, -2):  # Step back 2 at a time
        user_msg = conversation[i].get("content", "").strip()
        assistant_msg = (
            conversation[i + 1].get("content", "").strip()
            if i + 1 < len(conversation)
            else ""
        )

        entry = f"**User**: {user_msg}\n**Assistant**: {assistant_msg}\n"
        if total_chars + len(entry) > max_chars:
            break

        summary_lines.insert(0, entry)  # Insert at beginning to reverse order
        total_chars += len(entry)

    return "\n".join(summary_lines)
