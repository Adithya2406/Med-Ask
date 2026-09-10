import os
import random
from pathlib import Path

import openai
import pandas as pd
from flask import Flask, jsonify, render_template_string, request


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)


def _read_csv(name, **kwargs):
    path = BASE_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, on_bad_lines="skip", **kwargs)


def _load_medical_terms():
    terms = set()
    for filename in ("med_list.csv", "med_list2.csv"):
        frame = _read_csv(filename)
        if "Terms" in frame:
            terms.update(str(value).strip().lower() for value in frame["Terms"].dropna())
    return terms


def _load_quotes():
    frame = _read_csv("quotes.csv")
    if "Quotes" in frame:
        return [str(value) for value in frame["Quotes"].dropna()]
    return ["Ask clear questions and verify health information with a professional."]


MEDICAL_TERMS = _load_medical_terms()
QUOTES = _load_quotes()


PAGE = """
<!doctype html>
<title>Med-Ask</title>
<h1>Med-Ask</h1>
<p>{{ quote }}</p>
<form method="post" action="/result">
  <label for="query">Medical question</label>
  <input id="query" name="query" required>
  <button type="submit">Ask</button>
</form>
{% if answer %}<h2>Response</h2><p>{{ answer }}</p>{% endif %}
<p><strong>Educational prototype:</strong> not medical advice or a diagnosis.</p>
"""


@app.get("/")
@app.get("/home")
def home():
    return render_template_string(PAGE, quote=random.choice(QUOTES), answer=None)


@app.route("/result", methods=["POST", "GET"])
def result():
    query = (request.values.get("query") or "").strip()
    answer = answer_query(query)
    if request.is_json:
        return jsonify({"answer": answer})
    return render_template_string(PAGE, quote=random.choice(QUOTES), answer=answer)


@app.post("/inaccurate")
def record_unrecognized_query():
    query = (request.values.get("query") or "").strip()
    if not query:
        return jsonify({"saved": False, "reason": "empty query"}), 400

    path = BASE_DIR / "in_query.csv"
    frame = _read_csv("in_query.csv", index_col=0)
    existing = set(frame.iloc[:, 0].astype(str)) if not frame.empty else set()
    words = sorted(existing | set(query.lower().split()))
    pd.DataFrame({"term": words}).to_csv(path)
    return jsonify({"saved": True})


def answer_query(query):
    if not query:
        return "Enter a question."

    tokens = set(query.lower().split())
    if MEDICAL_TERMS and not tokens.intersection(MEDICAL_TERMS):
        return "This does not appear to be a medical query."

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "The application is not configured. Set OPENAI_API_KEY before starting it."

    response = openai.Completion.create(
        engine=os.getenv("OPENAI_MODEL", "text-davinci-003"),
        prompt=query,
        max_tokens=400,
    )
    text = response.choices[0].text.strip()
    return "This response is informational only: " + text


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG") == "1",
        port=int(os.getenv("PORT", "5002")),
    )
