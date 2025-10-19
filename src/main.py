import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from notifier import send_email
from scraper import check_player_has_unmarked_days, PlayerNotFoundError


def _validate_env(required_vars: list[str]):
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise KeyError(
            f"Missing required environment variables: {', '.join(missing)}")


def main():
    parser = argparse.ArgumentParser(description="Framadate Monitor")
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--info', action='store_true',
                        help='Enable info logging')
    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    elif args.info:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level)
    log = logging.getLogger(__name__)

    log.info("Logging configured at %s", logging.getLevelName(log_level))

    log.debug('Loading environment variables')
    load_dotenv()
    try:
        _validate_env([
            "FRAMADATE_URL",
            "PLAYER_NAME",
            "MAILGUN_API_KEY",
            "MAILGUN_DOMAIN",
            "MAILGUN_BASE_URL"
        ])
    except KeyError as e:
        log.error(str(e))
        sys.exit(1)
    log.info('Environment variables validated')

    try:
        framadate_url = os.environ["FRAMADATE_URL"]
        player_name = os.environ["PLAYER_NAME"]

        has_unmarked_days = check_player_has_unmarked_days(
            framadate_url, player_name)

        if has_unmarked_days:
            send_email(
                subject="[Framadate monitor] New matches available",
                body=f"{player_name} has unanswered matches in the Framadate: {framadate_url}"
            )
            log.info(f"Found unmartked days for '{player_name}', email sent")
        else:
            log.info(
                f"All days are marked for '{player_name}', email not sent")
    except PlayerNotFoundError as e:
        log.error(str(e))
        sys.exit(2)


if __name__ == "__main__":
    main()
