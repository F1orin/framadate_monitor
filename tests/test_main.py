"""Command-line error handling regressions."""

import os
from pathlib import Path
import subprocess
import sys
import unittest

from test_new_interface import INVALID_VOTE_POLL_URL


REPOSITORY_ROOT = Path(__file__).parent.parent


class MainErrorHandlingTests(unittest.TestCase):
    def test_poll_interface_error_exits_cleanly(self):
        environment = os.environ.copy()
        environment.update({
            "FRAMADATE_URL": INVALID_VOTE_POLL_URL,
            "PLAYER_NAME": "Answered Player",
        })

        result = subprocess.run(
            [sys.executable, "src/main.py", "--dry-run"],
            cwd=REPOSITORY_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 4)
        self.assertIn(
            "Unexpected vote label in Framadate poll: 'Maybe'",
            result.stderr,
        )
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
