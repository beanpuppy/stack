from estoult import Query, Field, op

from .base import BaseSchema


class User(BaseSchema):
    __tablename__ = "users"

    email = Field(str)
    password = Field(str)
    type = Field(str, default="user")

    @classmethod
    def get_by_email(cls, email):
        user = (
            Query(cls)
            .get_or_none()
            .where(cls.email == email, op.is_null(cls.tombstoned))
            .execute()
        )

        return user
