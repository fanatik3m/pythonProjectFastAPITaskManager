from pydantic import BaseModel


class AddRoleSchema(BaseModel):
    id: int
    name: str
    password: str