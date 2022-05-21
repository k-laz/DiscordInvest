import os

from dotenv import load_dotenv
import finnhub

load_dotenv()
API_KEY = os.getenv('FINNHUB_SANDBOX_API')

finnhub_client = finnhub.Client(api_key=API_KEY)
print(finnhub_client.quote('AAPL'))
