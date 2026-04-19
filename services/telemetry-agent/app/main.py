from sqlmodel import create_engine, SQLModel, Session
from models import Account

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/iot_streaming", echo=True)



SQLModel.metadata.create_all(engine)



# first_account = Account(name="Konto Joasi")
# second_account = Account(name="Konto Hubcia")



# batch_size = 1000
#
# with Session(engine) as session:
#     buffer = []
#
#     for i in range(1_000_000):
#         buffer.append(Account(name=f"Konto no_{i}"))
#
#         if len(buffer) == batch_size:
#             session.add_all(buffer)
#             session.commit()
#             buffer.clear()
#
#     if buffer:
#         session.add_all(buffer)
#         session.commit()