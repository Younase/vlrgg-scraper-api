# vlrgg-scraper-api
simple API to scrape Tournament stats from vlr.gg


## Usage

Follow these steps to use the API effectively:

### 1. Select a VLR Tournament URL
- Navigate to the tournament's stats page on VLR.gg.
- Apply any necessary filters.
- Copy the page URL. For example: `https://www.vlr.gg/event/stats/2237/lioness-cup-2024?exclude=27655.27656.27657.27659&min_rounds=100&agent=all`

### 2. Encode the VLR Tournament URL
- Use a URL encoding tool such as [URL Encoder](https://www.urlencoder.org/) to encode the copied URL.
- Example of an encoded URL: `https://vlrgg-scraper-api.onrender.com/get_csv?url=<encoded-url>`

### 3. Make the Request using the Encoded URL
- Example request: `https://vlrgg-scraper-api.onrender.com/get_csv?url=https%3A%2F%2Fwww.vlr.gg%2Fevent%2Fstats%2F2237%2Flioness-cup-2024%3Fexclude%3D27655.27656.27657.27659%26min_rounds%3D100%26agent%3Dall`


## Deployment

### 1. Prerequisites
- Ensure you have Python installed on your server.
- [optional] Set up a virtual environment for your Flask application.

### 2. Install Dependencies
- `pip install -r requirements.txt`

### 3. Deploy
- Use gunicorn for deployment: `gunicorn --bind 0.0.0.0:8000 wsgi:app`

### 4. Use the API locally
- access the API locally using `https://localhost:8000/get_csv?url=<encoded-url>`
