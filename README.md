# my-first-agent

A tiny command-line AI agent, built live in Lightning Lesson #1. Give it a topic,
it researches the live web (SerpAPI / Google), then two agents turn that into a
finished LinkedIn post: a **Researcher** drafts it and an **Editor** sharpens it
and adds hashtags. You conduct; the agents do the work.

> **Part of my Maven Lightning Lesson, [Become a One-Person Company: Build an AI Agent Crew](https://maven.com/p/e9d2a5/become-a-one-person-company-build-an-ai-agent-crew).**
> We build this agent live. The recording is shared with everyone who registers.

## Files
- `agent.py` — the final two-agent version (Researcher -> Editor hand-off).
- `agent_single.py` — the earlier one-agent version (just the Researcher), for reference.
- `requirements.txt` — dependencies (`openai`, `python-dotenv`). Web search uses the stdlib.
- `.env.example` — template for your keys. Copy to `.env` and fill it in.

## Run it (about 2 minutes)

```bash
# 1. from inside this folder, create a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. add your keys
cp .env.example .env
#    then open .env and paste in your real values

# 4. run it
python agent.py "AI agents for beginners"
```

You should see it research the topic, then print a **DRAFT (Researcher)** and a
**FINAL (Editor)** with 3 hashtags.

Try the one-agent version too: `python agent_single.py "AI agents for beginners"`

## Keys

You need two: one for web search, one for the model.

- **SerpAPI** (search) — free tier covers this: https://serpapi.com
- **The model** — two routes. Pick one:
  - **Standard OpenAI — start here if you are new.** One key, one signup:
    https://platform.openai.com/api-keys. Set a spending cap first on
    https://platform.openai.com/settings/organization/limits, then follow
    *Want to use standard OpenAI instead of Azure?* below.
  - **Azure OpenAI** — what the video runs on, and the heavier signup: you
    create your own Azure resource and your own deployment, then put ITS name
    in `AZURE_OPENAI_DEPLOYMENT`. The name in the video is a private deployment
    and will not work on your account.

### Want to use standard OpenAI instead of Azure?
The code is identical apart from the client. In `agent.py` (and `agent_single.py`):

1. Change the import:
   `from openai import AzureOpenAI` -> `from openai import OpenAI`
2. Replace each client with:
   ```python
   client = OpenAI()  # reads OPENAI_API_KEY from the environment
   ```
3. Set `model="gpt-4o"` (or any current OpenAI model) in the `create()` calls.
4. In `.env`, set `OPENAI_API_KEY=sk-...` and `SERPAPI_API_KEY=...`.

Everything else stays the same.

## Notes
- Never hardcode keys. They live only in `.env`, which stays on your machine.
- This model expects `max_completion_tokens` (not `max_tokens`) — already set for you.
