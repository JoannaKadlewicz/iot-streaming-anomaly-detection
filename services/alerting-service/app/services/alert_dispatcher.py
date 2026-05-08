import logging

from domain.model.anomaly import Anomaly
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
            dry_run: bool = True
    ):
        self._reader = reader
        self._writer = writer
        self._sender = sender
        self._recipient = recipient_email
        self._dry_run = dry_run

    def dispatch_all(self) -> None:
        anomalies: list[Anomaly] = self._reader.fetch_unsent()
        logger.info("Found %d unsent anomalies", len(anomalies))

        for anomaly in anomalies:
            try:
                if not self._dry_run:
                    self._sender.send(self._recipient, anomaly)
                    logger.info("Notification sent for account_id: %s / metric: %s / reason: %s", anomaly.account_id,
                                anomaly.metric, anomaly.anomaly_reason)
                else:
                    logger.info("DRY_RUN: Alert printed for: %s", anomaly)

                self._writer.mark_as_sent(anomaly)

            except Exception:
                logger.error("Failed to send alert for %s", anomaly.account_id)
