import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = 'do-not-reply@sandbox42830d132a454aaf93fe25a086d698c2.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)

        if api_key is None:
            raise MailgunException("Failed to load Mailgun API key")
        if domain is None:
            raise MailgunException('Failed to load Mailgun Domain')

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={
                            "from": f"{cls.FROM_EMAIL} <do-not-reply@sandbox42830d132a454aaf93fe25a086d698c2.mailgun.org/>",
                            "to": email,
                            "subject": subject,
                            "text": text,
                            "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response



