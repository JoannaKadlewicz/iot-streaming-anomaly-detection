import json
from time import sleep

import numpy as np
from kafka import KafkaProducer
from sqlmodel import create_engine, SQLModel, Session
from models import Account
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from kafka import KafkaProducer
from entities.base import Base
from repository.device_repository import DeviceRepository

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres", echo=True)
Base.metadata.create_all(engine)

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/iot_streaming", echo=True)



from generators.blood_pressure import BloodPressureGenerator
from generators.context import MetricContext
from generators.heart_rate import HeartRateGenerator
from generators.steps import StepsGenerator
from generators.temperature import BodyTemperatureGenerator
SQLModel.metadata.create_all(engine)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda event: json.dumps(event).encode("utf-8")
)


# first_account = Account(name="Konto Joasi")
# second_account = Account(name="Konto Hubcia")

producer.send("events", b'myszka')
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




ctx = MetricContext(
    account_id="1",
    device_id="101",
    rng=np.random.default_rng()
)

batch_size = 10000
counter = 0


temperature_generator = BodyTemperatureGenerator(context=ctx, unit="C")
heart_rate_generator = HeartRateGenerator(context=ctx)
steps_generator = StepsGenerator(context=ctx)
blood_pressure_generator = BloodPressureGenerator(context=ctx)
while True:
    producer.send("metrics2", temperature_generator.next_event())
    producer.send("metrics2", heart_rate_generator.next_event())
    producer.send("metrics2", steps_generator.next_event())
    producer.send("metrics2", blood_pressure_generator.next_event())
    counter += 1
    if counter >= batch_size:
        producer.flush()
        counter = 0

