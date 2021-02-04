from sqlalchemy import Column, Integer, String

class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)

class NameMixin:
    name = Column(String, nullable=False)
