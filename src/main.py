import argparse
import logging
from dotenv import load_dotenv

from scraper import check_player_has_unmarked_days


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
    log.debug('Environment variables loaded')

    has_unmarked_days = check_player_has_unmarked_days()
    log.info(f'has_unmarked_days: {has_unmarked_days}')


if __name__ == "__main__":
    main()
