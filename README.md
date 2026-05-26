# AI Code Reviewer (Streamlit + Groq)

A simple web app that reviews source code using the Groq API.

## Features

- Paste source code and choose a programming language
- Syntax-highlighted code preview before review
- One-click AI code review
- Markdown-formatted review with:
  - Summary
  - Potential bugs
  - Security issues
  - Performance improvements
  - Best practices
  - Score out of 10
  - Suggested improved code
- Graceful handling for empty input
- Session history (kept for the current browser session)
- `.env` configuration support
- Optional LangSmith tracing for prompt/review observability

## Project Files

- `app.py` - Streamlit app and Groq integration
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables
- `utils/prompts.py` - Prompt template builder for structured markdown reviews
- `utils/reviewer.py` - Groq client setup, optional LangSmith wrapping, and review call

## Suggested Structure

```text
ai-code-reviewer/
│── app.py
│── requirements.txt
│── .env.example
│── README.md
│── utils/
│   ├── reviewer.py
│   └── prompts.py
```

## Local Setup

1. **Create and activate a virtual environment**

   Windows (cmd):

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bat
   pip install -r requirements.txt
   ```

3. **Create your environment file**

   Copy `.env.example` to `.env` and set values:

   ```env
   GROQ_API_KEY=your_real_key
   GROQ_MODEL=llama-3.1-8b-instant

   # Optional LangSmith tracing
   LANGSMITH_TRACING=false
   LANGSMITH_API_KEY=your_langsmith_key
   LANGSMITH_PROJECT=ai-code-reviewer
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   ```

4. **Run the app**

   ```bat
   streamlit run app.py
   ```

## How LangSmith Tracing Works (Optional)

Tracing is enabled only when:

- `LANGSMITH_TRACING=true`
- and LangSmith environment variables are configured

When enabled, request data like prompt input, model, language context, and generated review can be observed in your LangSmith project.

## Streamlit Cloud Deployment

1. Push this project to GitHub.
2. Open Streamlit Community Cloud and create a **New app**.
3. Select your repository, branch, and set main file path to:

   ```
   app.py
   ```

4. In Streamlit Cloud app settings, add secrets for your environment values (at minimum `GROQ_API_KEY`).
5. Deploy.

### Recommended Streamlit Cloud Secrets

```toml
GROQ_API_KEY="your_real_key"
GROQ_MODEL="llama-3.1-8b-instant"
LANGSMITH_TRACING="false"
LANGSMITH_API_KEY="your_langsmith_key"
LANGSMITH_PROJECT="ai-code-reviewer"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
```

## Notes

- If `GROQ_API_KEY` is missing, the app will show an error when generating a review.
- Session history resets when the Streamlit session restarts.

# simple-AI-code-reviewer 
