# Amazon India Price Tracker

A Python-based price tracking application that monitors products on Amazon India, stores historical price data, detects price changes, and provides a dashboard for managing tracked products.

The application combines asynchronous web scraping, persistent SQLite storage, price comparison logic, email notifications, and a Streamlit interface in a structured Python project.

## Features

- Track products from Amazon India (`amazon.in`) using product URLs
- Scrape current product information asynchronously
- Store tracked products and historical prices in SQLite
- Detect price drops, increases, and unchanged prices
- Send email notifications when prices change
- View historical price records for individual products
- Update all tracked products in a single operation
- Display batch-update progress and results
- Handle unavailable products without interrupting the tracking process
- Delete products along with their associated price history
- Manage tracked products through a Streamlit dashboard

## Technologies Used

- **Python** — core application development
- **Streamlit** — web dashboard
- **aiohttp** — asynchronous HTTP requests
- **BeautifulSoup** — HTML parsing and data extraction
- **asyncio** — asynchronous execution
- **SQLite** — persistent data storage
- **Pandas** — data processing and presentation
- **SMTP** — email notifications

## Project Structure

```text
price_tracker/
│
├── database/
│   └── db.py
│
├── models/
│   └── products.py
│
├── scraper/
│   ├── fetcher.py
│   └── amazon_parser.py
│
├── services/
│   ├── price_tracker.py
│   └── email_service.py
│
├── utils/
│   └── retry.py
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

The project separates scraping, database operations, business logic, data models, and utility functions to keep responsibilities organized and maintainable.

## How It Works

1. A user enters an Amazon India product URL through the Streamlit dashboard.
2. The application asynchronously fetches the product page.
3. The scraper extracts the product information and current price.
4. Product information is stored in SQLite.
5. Each successful price check is recorded in the price history.
6. The current price is compared with the previously recorded price.
7. The application determines whether the price has dropped, increased, or remained unchanged.
8. Email notifications can be sent when a price change is detected.
9. Historical prices remain available through an expandable history view on the dashboard.

The application can also update all tracked products in a batch. If an individual product is unavailable or its price cannot be retrieved, it is skipped without stopping the remaining updates.

## Screenshots



The main dashboard provides an overview of tracked products, current prices, price status, and the latest check time.

![Price Tracker Dashboard]<img width="1808" height="773" alt="Screenshot 2026-07-21 095747" src="https://github.com/user-attachments/assets/ca3ebd0e-9db8-482c-a52c-849be0b7aa6a" />

### Price History

Historical price records can be expanded for each product to review previous prices and detected changes.

![Price History]<img width="1798" height="503" alt="Screenshot 2026-07-21 095810" src="https://github.com/user-attachments/assets/f0fd95e2-9951-4697-b9b4-2a6b62690147" />


### Batch Price Updates

Tracked products can be updated together with progress feedback and graceful handling of unavailable products.

![Batch Price Update] <img width="1838" height="342" alt="Screenshot 2026-07-21 095837" src="https://github.com/user-attachments/assets/74674902-a9a8-42ac-92db-c47461e4670e" />


## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd price_tracker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

## Configuration

Email notifications require sender and receiver email addresses to be configured.

Create a `.env` file in the project root:

```env
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver@example.com
```

Do not commit the `.env` file or email credentials to version control. Ensure `.env` is included in `.gitignore`.

For Gmail accounts, use an App Password instead of your regular account password.

## Key Technical Concepts

This project demonstrates practical implementation of:

- Asynchronous web scraping
- HTML parsing and structured data extraction
- Retry and error-handling strategies
- SQLite database integration
- Relational product and price-history storage
- Historical price comparison
- Batch processing with failure isolation
- Email notification workflows
- Streamlit application development
- Separation of application responsibilities into reusable modules

## Future Improvements

Potential extensions include:

- Support for additional Amazon marketplaces
- Support for additional e-commerce platforms
- Scheduled automatic price checks
- Target-price alerts configured by the user
- Deployment to a cloud platform
- REST API access to tracked-product and price-history data

## Limitations

- The scraper currently targets **Amazon India (`amazon.in`)**.
- Web scraping depends on the current structure of the target website. Changes to Amazon's HTML structure may require updates to the parser.
- Product availability and dynamically rendered content can affect price extraction.

## Disclaimer

This project was developed for educational and portfolio purposes. Users are responsible for ensuring that their use of web scraping complies with the terms, policies, and applicable requirements of the websites being accessed.
