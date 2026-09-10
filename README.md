# Med-Ask

Med-Ask is a Flask prototype that classifies incoming questions as medical or non-medical and uses a language model to produce a conversational informational response.

> This project is an educational prototype. It does not diagnose conditions, recommend treatment, or replace a qualified healthcare professional.

## Features

- Browser-based Flask interface
- Vocabulary-based medical-query screening
- Language-model response generation
- User feedback collection for unrecognized terms
- Random health-message display from a local CSV file

## Project structure

The application source is under `Med-Ask/`:

| File | Purpose |
|---|---|
| `app.py` | Flask routes and response-generation logic |
| `in_query.csv` | Terms submitted through the feedback route |
| `logo.png`, `logobig.jpg`, `finallogo.jpg` | Interface assets |

The original prototype also expects `med_list.csv`, `med_list2.csv`, `quotes.csv`, and a `templates/` directory. Those assets are not present in this repository snapshot and must be restored before the full interface can run.

## Setup

```bash
git clone <repository-url>
cd Med-Ask/Med-Ask

python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

Configure the language-model credential through the environment rather than source code:

```bash
export OPENAI_API_KEY=<your-key>
```

Then start the development server:

```bash
python app.py
```

The default port is `5002`. Override it with the `PORT` environment variable.

## Security

No credentials are stored in the repository. Keep local secrets in environment variables or an ignored `.env` file, and never commit that file.

## Limitations

- The current code uses a legacy completion API and is preserved as a project prototype.
- Responses may be inaccurate or incomplete.
- Required vocabulary and template assets must be restored locally.
- User-submitted health information should not be retained in production without an appropriate privacy and security design.
