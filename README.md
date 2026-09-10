# QnA Chatbot (LangChain + Groq + Streamlit)

A minimal question-answering chatbot that talks to a Groq-hosted model through
LangChain. `page.py` is a Streamlit chat UI and `stream_page.py` is the same UI
with token-by-token streaming; `main.py` holds the shared `llm` / `llm_stream`
instances plus prompt-composition demos; `structure_output.py` shows structured
(Pydantic) output extraction; `custom_tool.py` is a tool-calling agent.

## Files

### `main.py` — shared LLM + demos

At import time it:

1. Loads environment variables from `.env` via `python-dotenv`.
2. Reads `GROQ_API_KEY` and raises a `RuntimeError` if it is not set.
3. Builds a module-level `ChatGroq` LLM (`openai/gpt-oss-20b`, `temperature=1`,
   `max_tokens=8192`, `top_p=0.95`, `seed=42`) exported as `llm`, plus
   `llm_stream` — the same configuration with `streaming=True` for use with
   `.stream()`.

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
- each turn: append the user message, call `llm.invoke(st.session_state.messages)`
  (the full history is passed so the model has conversational memory), append
  and render the AI reply as markdown.

### `stream_page.py` — Streamlit chat app (streaming)

Same layout as `page.py`, but imports `llm_stream` and renders the reply as it
arrives:

- chat history kept as `{role, content}` dicts in `st.session_state.messages`,
- calls `llm_stream.stream(st.session_state.messages)` and iterates the chunks,
  accumulating `chunk.content` (handling both plain-string and list/`{"type":
  "text"}` content shapes),
- writes the growing text into a single `st.empty()` placeholder so the message
  updates in place, then appends the final text to history.

### `custom_tool.py` — tool-calling agent

Builds a LangChain agent with `create_agent` (from `langchain.agents`) over three
`@tool`-decorated functions:

- `add_number(a, b)` — sum of two numbers,
- `multiply_number(a, b)` — product of two numbers,
- `square(a)` — `a ** a` for the given number.

The agent uses `llm` as its model with the system prompt
`"You are math teach and use tool for calculation"`. A terminal loop reads from
stdin (`Ask:` prompt), exits on `break`, appends each question as a
`HumanMessage`, invokes the agent with the running `messages` list, carries
`response["messages"]` forward as history, and prints the content of every
message in the turn (tool calls, tool results, and the final answer).

### `stream_demo.py` — streaming prompt scaffold

Minimal scaffolding that imports `llm_stream` and defines a two-message
`ChatPromptTemplate` (`AI expert` system role, `{query}` user role) for
experimenting with `.stream()` from a script.

### `structure_output.py` — structured output example

Shows `llm.with_structured_output(...)` returning a validated Pydantic object
instead of free text:

- `User` — a `BaseModel` with `name`, `age`, `email` fields (each with a
  `Field(description=...)`).
- `ResponseStructure` — wraps a `type: Literal["single", "array"]` discriminator
  and `data: User | list[User]`.
- `execute()` binds the schema with
  `model = llm.with_structured_output(ResponseStructure)`, invokes it on a block
  of text containing several people, and prints `result.model_dump()`. The
  prompt asks the model to return just one user.

## Requirements

- Python >= 3.13
- A Groq API key

Dependencies (see `pyproject.toml`): `langchain`, `langchain-core`,
`langchain-groq`, `pydantic`, `dotenv` / `python-dotenv`, `streamlit`.

## Setup

Using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Or with pip:

```bash
pip install langchain langchain-core langchain-groq pydantic python-dotenv streamlit
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

### Streamlit app with streaming

```bash
uv run streamlit run stream_page.py
```

Same chat UI as `page.py`, but the AI reply streams in token by token.

### Tool-calling agent

```bash
uv run custom_tool.py
```

Ask a math question at the `Ask:` prompt (e.g. `what is 12 * 7, then squared?`);
the agent calls the `add_number` / `multiply_number` / `square` tools and prints
each message in the turn. Type `break` to quit.

### Structured output example

```bash
uv run structure_output.py
```

Prints a `model_dump()` dict of the extracted `ResponseStructure`.

### Terminal loop (optional)

Uncomment the `__main__` block at the bottom of `main.py`, then:

```bash
uv run main.py
```

Type questions at the `Input:` prompt, and `exit` to quit.
