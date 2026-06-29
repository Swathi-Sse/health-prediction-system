# HealthPredict AI

A Flask-based AI health prediction application that manages patient blood test records and generates health-risk remarks using Gemini AI.

## Features

- Add patient records
- View all patients
- Edit patient details
- Delete records
- Input validation
- SQLite persistent storage
- Gemini AI powered remarks
- Search patient records
- Responsive Bootstrap dashboard

## Tech Stack

- Python
- Flask
- SQLite
- HTML/CSS
- Bootstrap
- Gemini API

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

3. Run the application:

```bash
python app.py
```

4. Open:

```text
http://127.0.0.1:5000
```

## Note

Do not upload `.env` or API keys to GitHub.
