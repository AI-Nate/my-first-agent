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
- **SerpAPI** — free tier covers this: https://serpapi.com
- **Azure OpenAI** — this code uses the `AzureOpenAI` client and the deployment
  name `gpt-5.6-sol` (matches the live demo). Fill the `AZURE_OPENAI_*` values in `.env`.

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
