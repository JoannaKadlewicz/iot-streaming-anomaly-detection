from sqlalchemy import create_engine

from bootstrap import ensure_seeded, fetch_devices
from builder import DeviceGeneratorFactory
from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.messaging import MetricProducer
from streaming import stream
import logging

logger = logging.getLogger(__name__)

def main() -> None:
    settings = get_settings()
    configure_logging(level=settings.log_level)

    engine = create_engine(settings.postgres_dsn, echo=settings.debug)

    ensure_seeded(engine, settings)

    devices = fetch_devices(engine, settings.account_id)
    if not devices:
        raise Exception(f"No devices for account_id={settings.account_id}")

    generators = [
        generator
        for device in devices
        for generator in DeviceGeneratorFactory().build(settings.account_id, device)
    ]

    producer = MetricProducer(
        bootstrap_servers=settings.kafka_bootstrap_server,
        topic=settings.kafka_topic,
    )

    logger.info("Streaming for %d generators and for %d devices just started...", len(generators), len(devices))

    try:
        stream(producer, generators)
    except KeyboardInterrupt:
        logger.info("\nStopped!.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
