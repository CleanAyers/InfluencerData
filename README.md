# InfluencerData

This project is designed to gather academic data on food influencers by scraping comments from Instagram reels. The data collected will be used to analyze trends, engagement, and audience interactions with food influencers.

## Features

- **Batch Scraping**: Use `batch_template.py` to scrape comments from multiple Instagram reels in one session.
- **Customizable**: Easily configure the reels to scrape by editing the `REEL_IDENTIFIERS` list in `batch_template.py`.
- **Session Management**: Reuses cookies stored in `cookie.json` for seamless login and scraping.

## How to Use

### 1. Install Dependencies
Ensure you have Python 3.7+ installed. Install the required dependencies using:

```bash
pip install -r InstaScrape/requirements.txt
```

### 2. Configure `batch_template.py`
- Navigate to an influencer's reels page: `https://www.instagram.com/{influencer}/reel/`.
- Copy the desired reel IDs (shortcodes) from the URL (e.g., `DQag0vAD5na`).
- Paste the shortcodes into the `REEL_IDENTIFIERS` list in `batch_template.py`.

Example:
```python
REEL_IDENTIFIERS: List[str] = [
    "DQag0vAD5na",
    "DP45pCmAYwh",
    "DPcN771gZqG",
]
```

### 3. Create `cookie.json`
To create your own `cookie.json`:
1. Open your browser and navigate to `https://www.instagram.com`.
2. Log in to your Instagram account.
3. Right-click the webpage and select **Inspect** (or press `Ctrl+Shift+I` / `Cmd+Option+I`).
4. Go to the **Application** tab, then **Storage** > **Cookies** > `https://www.instagram.com`.
5. Copy the following cookies: `sessionid`, `csrftoken`, `mid`, and `ds_user_id`.
6. Create a file named `cookie.json` in the `InstaScrape` directory with the following structure:
   ```json
   {
       "cookies": {
           "sessionid": "your_sessionid",
           "csrftoken": "your_csrftoken",
           "mid": "your_mid",
           "ds_user_id": "your_ds_user_id"
       }
   }
   ```

### 4. Run the Scraper
Activate your virtual environment and run the batch scraper:

```bash
source venv/bin/activate
python3 InstaScrape/batch_template.py
```

The script will scrape comments for each reel in the `REEL_IDENTIFIERS` list and save the output in `download_comments/json` and `download_comments/txt`.

## Output
- **JSON Files**: Contain structured data with usernames, comments, and timestamps.
- **TXT Files**: Contain plain text comments for easy reading.

## Disclaimer
This project is for academic purposes only. Ensure you comply with Instagram's terms of service and data usage policies when using this tool.