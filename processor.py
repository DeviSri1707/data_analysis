import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import io
import base64
import re
from utils import scrape_wikipedia

async def process_request(question_text, files):
    questions = [q.strip() for q in question_text.splitlines() if q.strip()]
    
    if "highest grossing films" in question_text.lower():
        df = scrape_wikipedia()
        return handle_film_questions(df, questions)

    # Add more handlers for other datasets
    return {"error": "Unsupported question type"}

def handle_film_questions(df, questions):
    answers = []

    # Q1: How many $2 bn movies were released before 2000?
    df['Worldwide gross'] = df['Worldwide gross'].str.replace(r'[^0-9.]', '', regex=True).astype(float)
    df['Release year'] = pd.to_datetime(df['Release date'], errors='coerce').dt.year
    answers.append(int(df[(df['Worldwide gross'] >= 2000) & (df['Release year'] < 2000)].shape[0]))

    # Q2: Earliest film that grossed over $1.5 bn
    filtered = df[df['Worldwide gross'] >= 1500]
    earliest = filtered.sort_values('Release year').iloc[0]['Title']
    answers.append(earliest)

    # Q3: Correlation between Rank and Peak
    df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    df['Peak'] = pd.to_numeric(df['Peak'], errors='coerce')
    correlation = df[['Rank', 'Peak']].dropna().corr().iloc[0, 1]
    answers.append(round(correlation, 6))

    # Q4: Scatterplot
    img_uri = generate_plot(df)
    answers.append(img_uri)

    return answers

def generate_plot(df):
    df = df[['Rank', 'Peak']].dropna()
    plt.figure(figsize=(6, 4))
    plt.scatter(df['Rank'], df['Peak'], alpha=0.6)
    m, b = pd.Series(df['Peak']).corr(df['Rank']), df['Peak'].mean()
    plt.plot(df['Rank'], m * df['Rank'] + b, 'r--')
    plt.xlabel("Rank")
    plt.ylabel("Peak")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{encoded}"
