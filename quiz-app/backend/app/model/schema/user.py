from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    name: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123",
            }
        }
