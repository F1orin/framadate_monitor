# Framadate Monitor

A foot5 group I play with uses Framadate to schedule matches. Group organiser schedules next matches randomly. In order not to miss to join, this app is created to monitor when new dates appear to which you haven't subscribed yet.

The app automatically checks for new unanswered events and sends email notifications when they're available.

<img src="https://github.com/F1orin/framadate_monitor/blob/main/Screenshot.jpg" width="400" alt="Framadate interface">

## What it does

- Scrapes a Framadate poll using Selenium WebDriver
- Checks if a specific player has any days marked as "I don't know" 
- Sends email notifications via Mailgun when unmarked days are found
- Supports dry-run mode for testing
- Runs on GitHub Actions schedule (fits within free tier limits)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with required environment variables:
   ```
   FRAMADATE_URL='https://your-framadate-poll-url'
   PLAYER_NAME='Your Player Name'
   MAILGUN_API_KEY='your-mailgun-api-key'
   MAILGUN_DOMAIN='your-mailgun-domain'
   MAILGUN_BASE_URL='https://api.mailgun.net'
   ```

## Usage

```bash
# Run the monitor
python src/main.py

# Dry run (no email sent)
python src/main.py --dry-run

# Run with debug logging
python src/main.py --debug
```

## Requirements

- Python 3.13+
- Chrome browser (for Selenium WebDriver)
- Mailgun account for email notifications
