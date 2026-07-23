"""
A tiny command-line AI agent.

What it does:
  1. Takes a topic from the command line.
  2. Researches it on the live web using SerpAPI (Google search).
  3. Sends the research to an Azure OpenAI chat model.
  4. The model writes a short, punchy LinkedIn post.
  5. Prints the post to the terminal.

Run it like:
  python agent.py "your topic here"
"""

import os
import sys
import json
import urllib.parse
import urllib.request

from dotenv import load_dotenv
from openai import AzureOpenAI


# ---------------------------------------------------------------------------
# Step 0: Load configuration from the .env file (never hardcode secrets).
# ---------------------------------------------------------------------------
load_dotenv()  # reads the .env file in this folder into environment variables

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def research_topic(topic):
    """Search Google via SerpAPI and return a few top results as text."""
    # Build the request URL: https://serpapi.com/search.json?engine=google&q=...&api_key=...
    params = urllib.parse.urlencode(
        {
            "engine": "google",
            "q": topic,
            "api_key": SERPAPI_API_KEY,
        }
    )
    url = "https://serpapi.com/search.json?" + params

    # Make the GET request and parse the JSON response.
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    # Grab the top few organic search results (title, snippet, link).
    results = data.get("organic_results", [])[:5]

    if not results:
        return "No search results were found."

    # Turn the results into a simple block of text to feed the model.
    lines = []
    for item in results:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        lines.append(f"- {title}\n  {snippet}\n  ({link})")

    return "\n".join(lines)


def write_linkedin_post(topic, research):
    """Ask the Azure OpenAI model to write a LinkedIn post from the research."""
    # Create the Azure OpenAI client using values from .env.
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    # The instructions we give the model.
    system_prompt = (
        "You are a sharp social media writer. "
        "Write a short, punchy LinkedIn post (3-5 sentences). "
        "Make it engaging and professional. Do NOT include any hashtags."
    )
    user_prompt = (
        f"Topic: {topic}\n\n"
        f"Here is some fresh research from the web:\n{research}\n\n"
        "Write the LinkedIn post based on this."
    )

    # Call the chat model. Note: Azure uses the *deployment* name as the model,
    # and this model expects max_completion_tokens (not max_tokens).
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_completion_tokens=400,
    )

    return response.choices[0].message.content.strip()


def edit_linkedin_post(draft):
    """Second agent: an editor that sharpens the draft and adds hashtags.

    This is a separate agent from the researcher/writer above. It has its own
    system prompt (an editor persona) but calls the same Azure OpenAI model.
    """
    # Create the Azure OpenAI client using values from .env.
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    # The editor's instructions.
    system_prompt = (
        "You are a punchy social media editor. "
        "Rewrite the given LinkedIn draft to be more engaging and scroll-stopping, "
        "while keeping it short (3-5 sentences). "
        "Then add exactly 3 relevant hashtags on their own line at the end."
    )
    user_prompt = f"Here is the draft post to improve:\n\n{draft}"

    # Call the same model (the deployment name), using max_completion_tokens.
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_completion_tokens=400,
    )

    return response.choices[0].message.content.strip()


def main():
    # Make sure the user gave us a topic on the command line.
    if len(sys.argv) < 2:
        print('Usage: python agent.py "some topic"')
        sys.exit(1)

    topic = sys.argv[1]

    print(f"Researching: {topic} ...\n")
    research = research_topic(topic)

    # Agent 1: the researcher/writer drafts the post.
    print("Agent 1 (Researcher) is writing a draft ...\n")
    draft = write_linkedin_post(topic, research)

    # Agent 2: the editor sharpens the draft and adds hashtags.
    print("Agent 2 (Editor) is polishing it ...\n")
    final = edit_linkedin_post(draft)

    # Print both versions, clearly labeled.
    print("=" * 60)
    print("DRAFT (Researcher)")
    print("=" * 60)
    print(draft)
    print()
    print("=" * 60)
    print("FINAL (Editor)")
    print("=" * 60)
    print(final)
    print("=" * 60)


if __name__ == "__main__":
    main()
