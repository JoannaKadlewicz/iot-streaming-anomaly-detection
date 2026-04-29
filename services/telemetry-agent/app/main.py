import numpy as np
from kafka import KafkaProducer

from builder import DeviceGeneratorFactory
from infrastructure.config.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.messaging import metric_producer, MetricProducer
from infrastructure.persistence.repository import AccountRepository, DeviceRepository
from seed.seed import load_samples


# from generators.blood_pressure import BloodPressureGenerator
# from generators.context import MetricContext
# from generators.heart_rate import HeartRateGenerator
# from generators.steps import StepsGenerator
# from generators.temperature import BodyTemperatureGenerator
#
# ctx = MetricContext(
#     account_id="acc-1",
#     device_id="dev-1",
#     rng=np.random.default_rng(),
# )
#
# temperature_generator = BodyTemperatureGenerator(context=ctx, unit="C")
# heart_rate_generator = HeartRateGenerator(context=ctx)
# steps_generator = StepsGenerator(context=ctx)
# blood_pressure_generator = BloodPressureGenerator(context=ctx)
#
# while True:
#     print(temperature_generator.next_event())
# #     sleep(2)
#


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.postgres_dsn, echo=False)
    with Session(engine) as session:
        account_repo = AccountRepository(session)
        if not account_repo.has_accounts():
            load_samples(settings)

    factory = DeviceGeneratorFactory()
    #
    producer = MetricProducer(bootstrap_servers=session.kafka_bootstrap_server, topic=settings.kafka_topic)
    with Session(engine) as session:
        device_repo = DeviceRepository(session)
        devices = device_repo.get_devices_by_account_id(settings.account_id)

        for device in devices:
            metric_generators = factory.build(settings.account_id, device)


            while True:
                for generator in metric_generators:
                    metric = generator.next_event()

                    producer.send_metric(metric = metric, key=device.device_id)






if __name__ == "__main__":
    main()
