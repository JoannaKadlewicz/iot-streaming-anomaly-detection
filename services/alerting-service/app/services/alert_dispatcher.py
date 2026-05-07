import logging

from infrastructure.delta.anomaly_reader import AnomalyReader
from infrastructure.delta.anomaly_status_writer import AnomalyStatusWriter
from infrastructure.notifier.email_notifier import EmailNotifier

logger = logging.getLogger(__name__)


class AlertDispatcher:
    def __init__(
            self,
            reader: AnomalyReader,
            writer: AnomalyStatusWriter,
            sender: EmailNotifier,
            recipient_email: str,
    ):
        self._reader = reader
        self._writer = writer
        self._sender = sender
        self._recipient = recipient_email

    def dispatch_all(self) -> None:
        anomalies = self._reader.fetch_unsent()
        logger.info("Found %d unsent anomalies", len(anomalies))

        for anomaly in anomalies:
            try:
                self._sender.send(self._recipient, anomaly)
                self._writer.mark_as_sent(anomaly)
                logger.info("Alert sent for account_id: %s / metric: %s / reason: %s", anomaly.account_id,
                            anomaly.metric, anomaly.anomaly_reason)
            except Exception:
                logger.error("Failed to send alert for %s", anomaly.account_id)
