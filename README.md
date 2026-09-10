# QnA Chatbot (LangChain + Groq + Streamlit)

A minimal question-answering chatbot that talks to a Groq-hosted model through
LangChain Core. `page.py` is a Streamlit chat UI; `main.py` holds the shared
`llm` instance plus a couple of prompt-composition demos.

## Files

### `main.py` — shared LLM + demos

At import time it:

1. Loads environment variables from `.env` via `python-dotenv`.
2. Reads `GROQ_API_KEY` and raises a `RuntimeError` if it is not set.
3. Builds a module-level `ChatGroq` LLM (`openai/gpt-oss-20b`, `temperature=1`,
   `max_tokens=8192`, `top_p=0.95`, `seed=42`) exported as `llm`.

It also defines (neither is called by default — the `__main__` block is
commented out):

- `QnA()` — a terminal loop that reads from stdin (`Input:` prompt), exits on
  `exit`, and prints `AI <content>` for anything else.
- `main()` — builds a parameterized `ChatPromptTemplate`
  (`You are {lang} developer` / `{query}`), a `StrOutputParser`, and a custom
  `upper()` transform, then runs the same request two ways: manual
  (`prompt.invoke` -> `llm.invoke` -> `parser.parse` -> `upper`) and LCEL
  chained (`prompt | llm | parser | upper`).

### `page.py` — Streamlit chat app

Imports `llm` from `main.py` and renders a chat UI:

- `st.chat_input()` for the question box,
- chat history kept in `st.session_state.messages`,
- each turn: append the user message, call `llm.invoke(query)`, append and
  render the AI reply as markdown.

## Requirements

- Python >= 3.13
- A Groq API key

Dependencies (see `pyproject.toml`): `langchain-core`, `langchain-groq`,
`pydantic`, `dotenv` / `python-dotenv`, `streamlit`.

## Setup

Using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Or with pip:

```bash
pip install langchain-core langchain-groq pydantic python-dotenv streamlit
```

## Configuration

Create a `.env` file (or set the variable in your shell) with your Groq API key:

```
GROQ_API_KEY=your_api_key
```

PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key"
```

## Run

### Streamlit app (main entry point)

```bash
uv run streamlit run page.py
```

Or:

```bash
streamlit run page.py
```

This opens the chat UI in your browser (default http://localhost:8501).

### Terminal loop (optional)

Uncomment the `__main__` block at the bottom of `main.py`, then:

```bash
uv run main.py
```

Type questions at the `Input:` prompt, and `exit` to quit.
