import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_API_BASE_URL = os.getenv("MAILGUN_API_BASE_URL")


def send_email(recipient=None, subject=None, html_content=None, text=None):
    return requests.post(
        MAILGUN_API_BASE_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "Darader <donotreply@mail.darader.com>",
            "to": [recipient],
            "subject": subject,
            "html": html_content,
            "text": text
        }
    )
