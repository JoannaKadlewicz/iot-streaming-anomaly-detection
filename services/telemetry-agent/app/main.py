import logging

from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.messaging import MetricProducer
from services.bootstrap.bootstrap import fetch_devices
from services.factory.generator_factory import DeviceGeneratorFactory
from services.producer.streaming import stream

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    configure_logging(level=settings.log_level)

    devices = fetch_devices(settings.file_source)
    if not devices:
        raise Exception(f"No devices found in source_path: {settings.file_source}")

    factory = DeviceGeneratorFactory()
    all_generators = []
    for device in devices:
        device_generators = factory.build(device.account_id, device)
        all_generators.extend(device_generators)

    producer = MetricProducer(
        bootstrap_servers=settings.kafka_bootstrap_server,
        topic=settings.kafka_topic,
    )

    logger.info("Streaming for %d generators and for %d devices just started...", len(all_generators), len(devices))

    try:
        stream(producer, all_generators)
    except KeyboardInterrupt:
        logger.info("\nStopped!.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
