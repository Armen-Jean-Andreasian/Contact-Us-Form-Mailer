import smtplib
import ssl
from typing import NewType

Email = NewType('Email', str)


class Mailer:
    """ By default, it's set up to work with Gmail. """

    def __init__(
        self,
        your_email: Email,
        your_password: str,
        host: str = "smtp.gmail.com",
        port: int = 465,

    ):
        self.your_email = your_email
        self.your_password = your_password
        self.host = host
        self.port = port

        self._context = ssl.create_default_context()
        self._last_email_status: bool = None
        self._last_email_err: str = None

    def send_email(
        self,
        receiver: Email,
        subject: str,
        body: str
    ) -> tuple[bool, str] | tuple[bool, None]:

        content = f"Subject: {subject}\n\n{body}"

        try:
            with smtplib.SMTP_SSL(self.host, self.port, context=self._context) as server:
                server.login(self.your_email, self.your_password)
                server.sendmail(self.your_email, receiver, content)
        except Exception as err:
            self._last_email_err = str(err)
            self._last_email_status = False
        else:
            self._last_email_err = None
            self._last_email_status = True

    @property
    def status(self):
        return self._last_email_status

    @property
    def reason(self):
        return self._last_email_err

    def flush_last_email_metadata(self):
        self._last_email_err = None
        self._last_email_status = None
