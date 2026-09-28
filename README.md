# Framadate Monitor

A foot5 group I play with uses Framadate to schedule matches. Group organiser schedules next matches randomly. In order not to miss to join, this app is created to monitor when new dates appear to which you haven't subscribed yet.

The app automatically checks for new unanswered events and sends email notifications when they're available.

<img src="https://github.com/F1orin/framadate_monitor/blob/main/Screenshot.png" width="600" alt="Framadate interface">

## What it does

- Scrapes a Framadate poll using Selenium WebDriver
- Checks whether a specific player has any unanswered dates
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
   NOTIFICATION_EMAIL='recipient@example.com'
   MAILGUN_API_KEY='your-mailgun-api-key'
   MAILGUN_DOMAIN='your-mailgun-domain'
   MAILGUN_BASE_URL='https://api.mailgun.net'
   ```

## Usage

Run locally after completing the setup:

```bash
# Run the monitor and send an email when needed
python src/main.py

# Check the poll without sending email
python src/main.py --dry-run --info

# Show detailed diagnostic logs
python src/main.py --debug

# List all options
python src/main.py --help
```

Available options:

| Option | Description |
| --- | --- |
| `--dry-run` | Check the live poll without sending email. Only `FRAMADATE_URL` and `PLAYER_NAME` are required. |
| `--info` | Show normal operational messages. |
| `--debug` | Show detailed diagnostic messages; takes precedence over `--info`. |

Options can be combined. Without `--dry-run`, `NOTIFICATION_EMAIL` and the
Mailgun variables are also required, and an email is sent to that address when
unanswered dates are found.

The included GitHub Actions workflow runs automatically every day at 09:00 and
18:00 UTC. It can also be started manually from
**Actions → check-and-alert → Run workflow**.
Configure `PLAYER_NAME` as a repository variable and the remaining values,
including `NOTIFICATION_EMAIL`, as repository secrets.

A separate test workflow runs the test suite on every push and pull request.

## Requirements

- Python 3.11+
- Chrome browser (for Selenium WebDriver)
- Mailgun account for email notifications
