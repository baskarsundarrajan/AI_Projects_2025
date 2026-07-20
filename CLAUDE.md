# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this repository is

A **teaching monorepo** collecting independent AI engineering projects built by M.Sc AI (2025) student groups under faculty guidance. Each top-level directory is a **self-contained project with its own stack, dependencies, and README** — there is no shared build system, no common framework, and no cross-project code.

Key implications:

- **Scope changes to a single project's directory.** Projects don't depend on each other; a change in one should never touch another.
- **Each project's README is the source of truth** for its setup and usage. This file is a map, not a replacement.
- Contributions historically arrived as **pull requests from student forks** into `main` (the default branch).

## Project map

| Directory | Project | Stack | Entry point |
|---|---|---|---|
| repo root | Ollama Legal PDF RAG — Q&A over Indian legal case PDFs | Jupyter, LangChain, Ollama, Chroma, Gradio | `Legal_RAG.ipynb` |
| `quiz-app/` | "Quizzy" — quiz generation/evaluation from uploaded PDFs (most substantial project) | FastAPI + Celery + Redis + Weaviate + Groq backend; Next.js 15 / React 19 / Tailwind frontend; Firebase auth | `backend/app/app.py`, `frontend/` |
| `group_02/CodeSensei-main/` | CodeSensei — coding-assistant chat app | FastAPI backend (shells out to `ollama run llama3.2` via subprocess); React 19 + Vite frontend | `server/app.py`, `frontend/` |
| `Group5_AI-Powered-Music-Therapist/` | Therapist chatbot + music generation | Flask, Ollama (`gemma3:4b`, `gemma2:2b`), FER facial sentiment, Beatoven API | `src/app.py` |
| `AI_BOT_Group7/` | "Pandora" AI counselor bot | FAISS + SentenceTransformers RAG, fine-tuned Flan-T5 | `counselor_demo_app.py` |
| `KONKANI POEM NEXT WORD PREDICTION/` | GPT-2 fine-tuning for Konkani poetry (developed on Colab) | transformers, torch, datasets | `Trial_1.ipynb` / `trial_1.py` |
| `health-agent/` | "Sehat" — personal health agent (diet, fitness, mood, habits) with tool-calling and SQLite memory | FastAPI + Ollama (`llama3.2`) backend; vanilla HTML/JS dashboard + chat | `app.py` |
| `images/`, `*.pdf`, `*.pptx` | Reports, slides, screenshots — deliverables, not source | — | — |

Note the directory name `KONKANI POEM NEXT WORD PREDICTION` contains **spaces** — always quote the path in shell commands.

## Running the projects

There are no Makefiles, Dockerfiles, or CI workflows. Everything is run manually per project.

### quiz-app

Backend (from `quiz-app/backend/app/`):

```bash
uvicorn app:app --reload
celery -A core.config.celery_config.celery worker --loglevel=info -Q file_processing
```

Requires running Redis and Weaviate instances, Firebase credentials, and a Groq API key. Configuration is env-var driven via `python-dotenv` — see `quiz-app/backend/app/core/config/settings.py` for the full list (`DEBUG`, `GOOGLE_APPLICATION_CREDENTIALS`, `REDIS_URL`, `WEAVIATE_URL`, `WEAVIATE_API_KEY`, `TMP_FOLDER`, `GROQ_API_KEY`). There is no `.env.example`; keep secrets in an untracked `.env`.

Backend layout is layered: `api/v1/router/` (endpoints), `core/config/` (service configs), `services/` (question generation, evaluation, auth), `utils/` (PDF vectorization, text splitting), `task/` (Celery tasks). Follow this structure when adding backend code.

Frontend (from `quiz-app/frontend/`): `npm install`, then

```bash
npm run dev     # next dev --turbopack
npm run build
npm run lint    # next lint — the only lint command wired up in this project
```

### CodeSensei (`group_02/CodeSensei-main/`)

Backend (from `server/`): `uvicorn app:app --reload`. Requires Ollama installed locally with the `llama3.2` model pulled — the server invokes the `ollama` CLI via `subprocess`.

Frontend (from `frontend/`): `npm run dev` (Vite), `npm run build`, `npm run lint` (ESLint).

### Music Therapist (`Group5_AI-Powered-Music-Therapist/`)

From `src/`: `python app.py` (Flask, port 5000). Requires `ollama serve` with `gemma3:4b` and `gemma2:2b` pulled, plus webcam access for facial sentiment.

### Legal RAG (root) and Konkani prediction

Notebook-driven — open in Jupyter and run cells. Legal RAG requires a local Ollama instance and installs deps from the root `requirements.txt`. The Konkani project was developed on Google Colab; `trial_1.py` is the exported script form of the notebook.

### Sehat health agent (`health-agent/`)

From `health-agent/`: `pip install -r requirements.txt`, then `uvicorn app:app --reload` and open http://localhost:8000. Requires local Ollama with `llama3.2` pulled (model/URL/DB path configurable via `HEALTH_AGENT_MODEL`, `OLLAMA_URL`, `HEALTH_AGENT_DB`). State lives in a gitignored `health_agent.db` SQLite file. The LLM logs data via Ollama tool calls defined in `health_tools.py`; the agent loop is in `agent.py`.

### Pandora bot (`AI_BOT_Group7/`)

Python scripts with no requirements manifest — deps listed in its README (`faiss-cpu`, `sentence-transformers`, `transformers`, `torch`). Run `python counselor_demo_app.py`.

## Testing and CI

**There are no tests and no CI.** The only test-named file, `quiz-app/test.py`, is entirely commented out (scratch code). No pytest/tox config, no GitHub Actions, no pre-commit hooks. Don't search for a test command — verify changes by running the affected app manually. If you add tests to a project, keep them inside that project's directory.

## Gotchas and conventions

- **External services won't exist in a sandbox.** Nearly every project assumes locally running services: Ollama (Legal RAG, CodeSensei, Music Therapist), Redis + Weaviate + Firebase + Groq (quiz-app). Expect runtime failures in CI/sandbox environments; static verification (imports, lint, build) is often the best you can do.
- **README vs. code mismatches exist.** e.g. some READMEs say `uvicorn main:app` but the actual module is `app.py` (`uvicorn app:app`). Trust the code.
- **Committed artifacts are not source.** `__pycache__/*.pyc` files, HuggingFace model/tokenizer files (`quiz-app/backend/app/model/ml_model/`, `AI_BOT_Group7/counselor_faiss.index`), PDFs/PPTX reports, and the large generated `quiz-app/backend/app/output_data/output.md` are all committed. Don't edit them, don't regenerate them unprompted, and avoid committing new binaries or caches.
- **No root `.gitignore`.** Only `quiz-app/` and the CodeSensei frontend have their own. Check `git status` carefully before staging — it's easy to pick up caches, venvs, or `node_modules`.
- **Secrets have leaked here before.** An API key was previously committed to `Legal_RAG.ipynb` and had to be scrubbed, and a Beatoven API token appears hardcoded in the Music Therapist project. Never hardcode or commit keys; use environment variables and flag any credentials you encounter in the code.
- **Known quirks — flag, don't silently "fix":** the quiz-app frontend has both `next.config.js` and `next.config.mjs`, and its `package.json` includes the typosquat package `"axois"` alongside the real `axios`. Some notebooks use Windows-style backslash paths (student machines were Windows). Mention these if relevant, but don't change them without being asked.
- **Mixed maturity levels.** These are student projects: expect commented-out code, print debugging, and inconsistent style. Match the local style of whichever project you're editing rather than imposing repo-wide conventions.

## Git workflow

- Default branch: `main`. Do feature work on branches; students contributed via PRs from personal forks.
- Keep commits scoped to one project. Use clear, descriptive commit messages (the existing history mixes styles; err toward descriptive).
- Before committing, double-check the diff for stray binaries, caches, and credentials — the repo's history shows all three have slipped in before.
