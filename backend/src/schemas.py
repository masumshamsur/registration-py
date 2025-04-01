from pydantic import BaseModel

class UserSchema(BaseModel):
    firstname: str
    lastname: str
