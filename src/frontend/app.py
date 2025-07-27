""" Chainlit Front End Facade """
from os import remove as os_remove

import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
import httpx
import json

from src.frontend import CONFIG
from src.frontend.prompts.teamplates import system_prompt, user_prompt_template
from src.frontend.models.payload import ChatPayload
from src.frontend.models.endpoints import APIEndpoint
from src.frontend.services.rag_client import fetch_external_context
from src.frontend.utils.free_memory import remove_all_files_in_dir


@cl.on_chat_start
async def start_chat():

    remove_all_files_in_dir()

    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": system_prompt}],
    )

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Dev Models",
                values=CONFIG["llms"]["available"],
                initial_index=0,
            )
        ]
    ).send()



@cl.on_message
async def main(message: cl.Message):

    user_input = message.content
    message_history = cl.user_session.get("message_history")
    rag_input = ""
    context=""

    # Step 1: Collect User Input
    rag_input = user_input    
    # No Conversation due to high token count of RAG and Hardware constriants
    # conversation_summary = summarize_message_history(message_history)


    # Step 2: Fetch context from RAG microservice
    try:
        context = await fetch_external_context(rag_input)
        if isinstance(context, list):
            context = "\n\n".join(context)
    except Exception as e:
        context = ""
        await cl.Message(f"⚠️ Failed to fetch context from RAG: {str(e)}").send()


    # Step 3: Render full prompt using the Jinja2 template
    rendered_prompt = user_prompt_template.render(
        context=context,
        user_input=user_input
    )

    print(f"==== Fully Rendered Prompt ====\n\n\n{rendered_prompt}")

    # Step 3.5: Check total token count against model limit
    # MAX_TOKENS = CONFIG["llms"]["default_context_window"]
    # token_total = count_tokens(rendered_prompt)
    # for msg in message_history:
    #     token_total += count_tokens(msg["content"])

    # if token_total > MAX_TOKENS:
    #     await cl.Message(
    #         f"⚠️ The total input exceeds the model's token limit.\n"
    #         f"Allowed: {MAX_TOKENS} tokens. Current: {token_total} tokens.\n"
    #         f"Please reduce your input or clear some context."
    #     ).send()
    #     return

    # Step 4: Append user message (as rendered full prompt) to history
    message_history.append({
        "role": "user",
        "content": rendered_prompt
    })

    # Step 5: Prepare payload for Ollama
    chat_payload = ChatPayload(
        model=CONFIG["llms"]["default"],
        temperature=CONFIG["llms"]["temperature"],
        top_k=CONFIG["llms"]["top_k"],
        top_p=CONFIG["llms"]["top_p"],
        repeat_penalty=CONFIG["llms"]["repeat_penalty"],
        seed=CONFIG["llms"]["seed"],
        messages=message_history,
        stream=True
    )
    payload = chat_payload.to_dict()

    # Step 6: Send to LLM and stream result
    async with httpx.AsyncClient(timeout=None) as client:
        msg = cl.Message(content="")
        await msg.send()
        collected_text = ""

        try:
            async with client.stream("POST", APIEndpoint.OLLAMA_CHAT.url, json=payload) as response:
                response.raise_for_status()

                async for chunk in response.aiter_text():
                    chunk = chunk.strip()
                    if not chunk:
                        continue

                    try:
                        data_list = [json.loads(chunk)]
                    except json.JSONDecodeError:
                        data_list = []
                        for line in chunk.splitlines():
                            try:
                                data_list.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass

                    for data in data_list:
                        msg_obj = data.get("message", {})
                        content = msg_obj.get("content", "")

                        if content:
                            collected_text += content
                            await msg.stream_token(content)

                        if data.get("done_reason") == "stop":
                            break

        finally:
            message_history.append({
                "role": "assistant",
                "content": collected_text
            })
            await msg.update()
