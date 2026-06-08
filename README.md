# Your Morning Buddy

I built **Your Morning Buddy** as an AI-powered Streamlit app to help users start their day with motivation, weather information, interest-based news, and planning support.

This project uses Google Gemini to generate a daily motivational thought, create a related realistic image, summarize weather information, and provide quick summaries for news articles.

## Features

- Generate a daily motivational thought
- Generate a realistic image based on the motivational thought
- Search current weather by city
- Create a friendly weather summary
- Search news articles by user interest or topic
- Display 5 related news articles in columns
- Generate a quick summary for each news article
- Provide a smart planner section for daily planning

## Tech Stack

I used the following tools and APIs:

- Python
- Streamlit
- Google Gemini API
- OpenWeather API
- NewsAPI
- python-dotenv
- requests

## Project Structure

```text
morning-buddy-streamlit/
├── app.py
├── README.md
├── requirements.txt
├── .env
├── .gitignore
└── Services/
    ├── __init__.py
    ├── geminiService.py
    ├── weatherService.py
    └── newsService.py
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SagharBahrami/morning-buddy-streamlit.git
cd morning-buddy-streamlit
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` file

Create a `.env` file in the project root and add the required API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_newsapi_key
```

The `.env` file should not be pushed to GitHub.

### 6. Run the Streamlit app

```bash
streamlit run app.py
```

Or:

```bash
python -m streamlit run app.py
```

## Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | API key used for Google Gemini |
| `OPENWEATHER_API_KEY` | API key used for OpenWeather weather data |
| `NEWS_API_KEY` | API key used for NewsAPI article search |

## How the App Works

The app has a sidebar that allows users to choose what they want to do:

- **Home**: Generates a motivational thought and a related realistic image.
- **Get Weather of your City**: Lets the user enter a city and receive a friendly weather update.
- **News by Interest**: Lets the user enter a topic and view 5 related articles.
- **Smart Planner**: Provides a section for planning daily tasks.

## Notes

- I used separate service classes to keep the code cleaner:
  - `GeminiService` handles Gemini text and image generation.
  - `WeatherService` handles weather API requests.
  - `NewsService` handles news API requests.
- News summaries are based on the title and description returned by NewsAPI, not the full article text.
- Gemini image generation may sometimes return a temporary high-demand error. If that happens, the user can try again later.

## Future Improvements

In the future, I would like to add:

- Weather unit selection, such as Celsius or Fahrenheit
- News category filters
- Saved favorite news topics
- Deployment on Streamlit Community Cloud

## License

This project was created for learning and portfolio purposes.