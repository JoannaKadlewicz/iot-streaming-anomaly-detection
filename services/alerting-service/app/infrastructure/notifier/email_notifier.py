import smtplib
from email.mime.text import MIMEText

from domain.model.anomaly import Anomaly
from infrastructure.config import Settings
from infrastructure.template.anomaly_template import AnomalyEmailTemplate


class EmailNotifier:

    def __init__(self, settings: Settings):
        self._settings = settings
        self._template = AnomalyEmailTemplate()

    def send(self, to: str, anomaly: Anomaly) -> None:
        html_body = self._template.render(anomaly=anomaly)

        msg = MIMEText(html_body, "html")
        msg["Subject"] = f"<{anomaly.metric}> alert kicked!"
        msg["From"] = self._settings.smtp_from
        msg["To"] = to

        with smtplib.SMTP(self._settings.smtp_host, self._settings.smtp_port) as server:
            server.starttls()
            server.login(self._settings.smtp_login, self._settings.smtp_password)
            server.sendmail(self._settings.smtp_from, to, msg.as_string())
