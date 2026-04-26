# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and paste your keys

source venv/bin/activate


# 3. Run (city as argument or interactively prompted)
python3 restaurant_scraper.py --city Guelph
# python restaurant_scraper.py -c Cambridge --log-level DEBUG