# Price Comparison for Pakistani Women's Fashion Brands

Welcome to the project! We are building a platform to aggregate and compare prices for women's fashion brands in Pakistan, starting with Alkaram Studio, Sapphire, and Nishat Linen.

## What the User Sees (The Experience)
When a user types something like:
> "5k se kam mein shaadi ke liye embroidered suit chahiye"

The system will show a list of beautiful product cards, each containing:
- Product image
- Name and brand (Alkaram, Sapphire, Nishat)
- Price (and the old price if on sale, showing the discount)
- A "View on store" button that links directly to the original product page.

Results are intelligently sorted by price or best value. The user taps a card, lands on the brand's page, and completes their purchase there.

## What are we doing? (Technical Flow)
We are creating a full-stack web application. Here is the flow of how it will work:
1. **Data Collection (Scraping)**: We will write Python scripts to visit the brands' websites, extract product details (names, prices, images, links), and clean the data.
2. **Data Storage (Database)**: We will save this cleaned data into a local SQLite database so we can search it quickly without scraping the websites every time someone searches.
3. **Backend API**: We will build a FastAPI server. This server will talk to our database and provide the data to our frontend based on user searches (e.g., filtering by budget and brand).
4. **Frontend UI**: We will build a mobile-friendly user interface where users can enter their search queries and budget, and see the results beautifully displayed side-by-side.
5. **Automation**: We will set up a scheduler to automatically run our scrapers every few hours to keep prices and stock up to date.

## Essential Additions to the Plan
Based on best practices, we are adding these critical components to ensure the system is robust and handles errors gracefully:
1. **`categorizer.py`**: A dedicated script to parse titles/tags and assign categories (embroidered, printed, lawn, chiffon, 3-piece, unstitched). This is crucial for precise searching.
2. **`scrape_runs` Table**: A database table to log every scraper run (time, products found, success/fail status). If a brand changes their layout and breaks our scraper, we will know immediately.
3. **Configuration & `.env`**: Centralizing delays, user agents, DB paths, and brand URLs so they are not hardcoded across multiple files.
4. **Logging (`utils/logger.py`)**: Saving scraper errors to a log file for easy debugging.
5. **Testing (`tests/` folder)**: Small tests specifically for the normalizer and categorizer, as pricing/category errors directly impact the user experience.
6. **Out-of-stock Handling**: Products that disappear from a store will be marked as "unavailable" rather than deleted, so we don't show ghost products to users.

## Folder Structure (Updated)
Here is the updated folder structure for our project:

```text
dress-scraper/
│
├── scrapers/               # Data collection scripts
│   ├── __init__.py
│   ├── base_scraper.py     # Common functions (delays, headers)
│   ├── alkaram.py          
│   ├── sapphire.py         
│   ├── nishat.py           
│   ├── normalizer.py       # Standardizing data (e.g., PKR formatting)
│   └── categorizer.py      # Extracting categories from tags/titles
│
├── database/               # Data storage
│   ├── __init__.py
│   ├── models.py           # Products, Price History, and scrape_runs tables
│   └── db_setup.py         # DB connection and creation
│
├── backend/                # FastAPI server
│   ├── __init__.py
│   ├── main.py             
│   ├── routes.py           
│   └── schemas.py          
│
├── frontend/               # User interface
│   ├── index.html          
│   ├── style.css           
│   └── app.js              
│
├── utils/                  # Helper utilities
│   ├── __init__.py
│   └── logger.py           # Centralized logging for errors
│
├── tests/                  # Automated testing
│   ├── test_normalizer.py
│   └── test_categorizer.py
│
├── data/                   
│   └── products.db         
│
├── .env                    # Environment variables (secret/config)
├── config.py               # Loads .env variables (delays, User-Agent)
├── main_scheduler.py       # Script that runs scrapers on a timer
├── requirements.txt        
└── plan.md                 # Project documentation (this file)
```

## Future Features (V2 & Beyond)
Once the base version is working, we will add these features to make the app stand out:
- **Budget-first search**: "Mere paas Rs. 5,000 hain, embroidered suit dikhao." (Our unique selling point).
- **Sale filter**: Show "Only items on sale" with discount percentage calculations.
- **Price history chart**: A graph showing product price over time to verify if a discount is genuine.
- **Price drop alert**: Users can save a product and get notified (Email/WhatsApp) when the price drops.
- **Wishlist / Favourites**: Allow users to save their favorite items.
- **Size availability filter**: Filter out products that aren't available in the user's size.
- **Best value ranking**: Sort not just by price, but by deal quality (e.g., 3-piece vs 2-piece for the same price).
- **Share button**: Easy sharing to WhatsApp, tailored for local user behavior.
- **Roman Urdu / Urdu search**: Support for queries like "kadhai wala suit" to stand out from generic English-only platforms.
- **More brands**: Integrate Khaadi, Gul Ahmed, Limelight, Beechtree, etc.
- **Click tracking**: Track outbound clicks for analytics and future affiliate marketing.

## Next Steps
We will proceed step-by-step as you requested. 

Once you are ready, you can prompt me with the first step:
> "Ab Alkaram ka scraper likho. Pehle check karo ke /products.json kaam karta hai ya nahi, aur data CSV mein save karo."
