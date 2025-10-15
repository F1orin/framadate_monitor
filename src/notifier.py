import os
import requests


def send_email(subject: str, body: str):
    api_key = os.environ["MAILGUN_API_KEY"]
    domain = os.environ["MAILGUN_DOMAIN"]
    base_url = os.environ["MAILGUN_BASE_URL"]

    url = f"{base_url}/v3/{domain}/messages"
    resp = requests.post(
        url,
        auth=("api", api_key),
        data={
            "from": f"Mailgun Sandbox <postmaster@{domain}>",
            "to": "Florin Bicher <f.bicher@gmail.com>",
            "subject": subject,
            "text": body,
        }
    )
    resp.raise_for_status()
