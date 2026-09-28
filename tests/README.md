Run from the repository root with dependencies installed and Chrome available:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The same test suite runs in GitHub Actions on every push and pull request.

The fixture contains the minimal table structure required by the scraper, derived
from the Framadate interface snapshot saved on 2026-09-28. It is safe to publish:
real names, poll and vote identifiers, edit links, forms, comments, totals and
external resources have been removed.

The fixture has four dates at 12h30 and two synthetic participants. `Answered
Player` has answered all dates (No, Yes, If needed, Yes); `Unanswered Player`
has one Yes and three empty cells. The fixture tests the DOM contract used by the
scraper rather than the page's visual appearance.

Tests use local HTML and never submit votes or send email.
Chrome and its Selenium driver are required; Selenium may download the driver
on first use.

Five structure checks describe the fields needed by the monitor and verify that
the fixture contains no links, forms or external identifiers. Three regression
tests call the scraper for answered, unanswered and missing participants. One
notifier test verifies that the recipient comes from `NOTIFICATION_EMAIL`.
Passing the local fixture checks alone does not prove compatibility with the live
service; use a live dry run for an end-to-end check.
