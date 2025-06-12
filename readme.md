# Dhaka News RAG

## Standard Setup

### Create venv (optional)

```
python -m venv venv
.\.venv\Scripts\activate
```

### Install packages

```
pip install -r requirements.txt
pip install google-genai

```

It has 2 main file. one is bot.py that will scarp the news every day and another is gui.py that will handle the gui part

### For AI feature you need to place your gemini api key in gemini.py

### Run bot

```
python bot.py
```

### Run gui (streamlit)

```
streamlit run gui.py
```

## Docker Setup

### Using Docker Compose (Recommended)

Build and start all services:

```
docker-compose up -d --build
```

Stop all services:

```
docker-compose down
```

### Using Docker directly

Build the Docker image:

```
docker build -t dhaka-news-aggregator .
```

Run the bot:

```
docker run -d --name dhaka-news-bot -v ./news:/app/news dhaka-news-rag python bot.py
```

Run the GUI:

```
docker run -d --name dhaka-news-gui -p 8501:8501 -v ./news:/app/news dhaka-news-rag
```

Access the GUI at http://localhost:8501
