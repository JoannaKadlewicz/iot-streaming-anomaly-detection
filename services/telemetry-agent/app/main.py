from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from kafka import KafkaProducer
from entities.base import Base
from repository.device_repository import DeviceRepository

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    repository = DeviceRepository(session)
    devices = repository.get_devices_by_account_id(1)
    for d in devices:
        print(d)





producer = KafkaProducer(bootstrap_servers="localhost:9092")

producer.send("metrics", b"Joasia")

producer.flush()



#
# import numpy as np
#
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
# print(temperature_generator.next_event())
# print(heart_rate_generator.next_event())
# print(steps_generator.next_event())
# print(blood_pressure_generator.next_event())
