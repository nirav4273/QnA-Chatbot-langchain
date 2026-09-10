# QnA Chatbot (LangChain + Groq)

A minimal example that runs a question-answering prompt against a Groq-hosted
model using LangChain Core. It demonstrates two ways to compose the same call:
invoking each piece manually, and wiring them together with LCEL (`|`) chaining.

## What `main.py` does

1. Loads environment variables from `.env` via `python-dotenv`.
2. Builds a `ChatGroq` LLM (`openai/gpt-oss-20b`, `temperature=1`,
   `max_tokens=8192`, `top_p=0.95`, `seed=42`).
3. Defines a `ChatPromptTemplate` with a parameterized system message
   (`You are {lang} developer`) and user message (`{query}`).
4. Defines a `StrOutputParser` and a custom `upper()` transform that
   uppercases the model output.
5. Runs the prompt two ways:
   - **Manual:** `prompt.invoke(...)` -> `llm.invoke(...)` -> `parser.parse(...)` -> `upper(...)`
   - **Chained (LCEL):** `chain = prompt | llm | parser | upper`, then `chain.invoke(...)`

Both calls use `lang="JavaScript"` and `query="Write basic LRU steps"`, and
print the result.

## Requirements

- Python >= 3.13
- A Groq API key

Dependencies (see `pyproject.toml`):

- `langchain-core`
- `langchain-groq`
- `pydantic`
- `dotenv` / `python-dotenv`

## Setup

Using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Or with pip:

```bash
pip install langchain-core langchain-groq pydantic python-dotenv
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

The program raises a `RuntimeError` if `GROQ_API_KEY` is not set.

## Run

```bash
uv run main.py
```

Or:

```bash
python main.py
```
