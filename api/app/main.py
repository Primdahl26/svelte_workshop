from fastapi import FastAPI
from faker import Faker
import strawberry
from strawberry.fastapi import GraphQLRouter
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

FAKER_AMOUNT = 1000
fake = Faker(["da-DK"])


@strawberry.type
class Insight:
    id: uuid.UUID
    employee_name: str
    employee_email: str
    managers_name: str
    manager_email: str
    department_name: str

data = [
    Insight(
        id=uuid.uuid4(),
        employee_name=fake.first_name() + " " + fake.last_name(),
        employee_email=fake.email(),
        managers_name=fake.first_name() + " " + fake.last_name(),
        manager_email=fake.email(),
        department_name=fake.job(),
    )
    for _ in range(FAKER_AMOUNT)
]


@strawberry.type
class Query:
    @strawberry.field
    def get_insight(self, skip: int = 0, limit: int = 20) -> list[Insight]:
        return data[skip:limit]


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def read_root():
    return {"Svelte": "Er mega nice!"}


@app.get("/indsigt")
def indsigt():
    return [
        {
            "uuid": uuid.uuid4(),
            "employee_name": fake.first_name() + " " + fake.last_name(),
            "employee_email": fake.email(),
            "managers_name": fake.first_name() + " " + fake.last_name(),
            "manager_email": fake.email(),
            "department_name": fake.job(),
        }
        for _ in range(FAKER_AMOUNT)
    ]

