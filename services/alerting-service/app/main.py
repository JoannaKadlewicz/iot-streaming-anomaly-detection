from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.delta.anomaly_reader import AnomalyReader
from infrastructure.delta.anomaly_status_writer import AnomalyStatusWriter
from infrastructure.notifier.email_notifier import EmailNotifier
from infrastructure.spark.session import create_spark_session
from services.alert_dispatcher import AlertDispatcher


def main():
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)

    dispatcher = AlertDispatcher(
        reader=AnomalyReader(spark, settings.anomalies_delta_path),
        writer=AnomalyStatusWriter(spark, settings.anomalies_delta_path),
        sender=EmailNotifier(settings),
        recipient_email=settings.smtp_to)

    dispatcher.dispatch_all()


if __name__ == "__main__":
    main()
