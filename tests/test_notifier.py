import os
import unittest
from unittest.mock import patch

from src.notifier import send_email


class NotifierTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "MAILGUN_API_KEY": "test-api-key",
            "MAILGUN_DOMAIN": "mail.example.com",
            "MAILGUN_BASE_URL": "https://api.example.com",
            "NOTIFICATION_EMAIL": "alerts@example.com",
        },
        clear=True,
    )
    @patch("src.notifier.requests.post")
    def test_send_email_uses_recipient_from_environment(self, post):
        send_email("Subject", "Body")

        self.assertEqual(
            post.call_args.kwargs["data"]["to"],
            "alerts@example.com",
        )
        post.return_value.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
