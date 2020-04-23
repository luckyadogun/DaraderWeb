import requests

MAILGUN_API_KEY = '3c985f1f6af27082b95048f05f3dfd2e-f135b0f1-11c096ef'
MAILGUN_API_BASE_URL = 'https://api.mailgun.net/v3/mail.darader.com/messages'


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
