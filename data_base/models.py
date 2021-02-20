import datetime as dt
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, UniqueConstraint, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from . import mixin

"""
Объекты для перевозки
- название
- высота
- ширина
- глубина
- обьем
- вес
- единицы измерения
"""

Base = declarative_base()
inventory_room_collection = Table(
    "inventory_collection",
    Base.metadata,
    Column("inventory_id", Integer, ForeignKey("inventory.id")),
    Column("room_collection_id", Integer, ForeignKey("room_collection.id"))
)

room_collection_order = Table(
    "room_collection_order",
    Base.metadata,
    Column("room_collection_id", Integer, ForeignKey("room_collection.id")),
    Column("order_id", Integer, ForeignKey("order.id"))
)

room_collection_move_size = Table(
    "room_collection_move_size",
    Base.metadata,
    Column("room_collection_id", Integer, ForeignKey("room_collection.id")),
    Column("move_size_id", Integer, ForeignKey("move_size.id"))
)

floor_collection_order = Table(
    "floor_collection_order",
    Base.metadata,
    Column("floor_collection_id", Integer, ForeignKey("floor_collection.id")),
    Column("order_id", Integer, ForeignKey("order.id"))
)


class Inventory(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "inventory"
    height = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    deep = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    dimension = Column(Float, nullable=False)
    unit = Column(Integer, nullable=False)
    room_collections = relationship("RoomCollection", secondary=inventory_room_collection)

    def __init__(self, name, unit, dimension=None, height=None, width=None, deep=None, weight=None):
        if not dimension:
            if all((height, width, deep)):
                dimension = height * width * deep
        self.dimension = dimension
        self.name = name
        self.unit = unit
        self.height = height
        self.weight = weight
        self.width = width
        self.deep = deep


class User(Base, mixin.IdMixin):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("firstname", "email", "phone_number", name="_user"),)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    orders = relationship("Order")


class Order(Base, mixin.IdMixin):
    __tablename__ = "order"
    move_date = Column(Date, nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    estimated_hours = Column(Integer, nullable=False)
    travel_time = Column(Integer, nullable=False)
    create_date = Column(DateTime, default=dt.datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    users = relationship("User", lazy="joined")
    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", lazy="joined")
    move_size_id = Column(Integer, ForeignKey("move_size.id"))
    move_size = relationship("MoveSize", lazy="joined")
    service_id = Column(Integer, ForeignKey("services.id"))
    service = relationship("Services", lazy="joined")
    room_collections = relationship("RoomCollection", secondary=room_collection_order)
    floor_collection = relationship("FloorsCollection", secondary=floor_collection_order)


# TODO: Модель таблицы диапозонов времени работ


class RoomCollection(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "room_collection"
    preset = Column(Boolean, default=False, nullable=False)
    inventories = relationship("Inventory", secondary=inventory_room_collection)
    orders = relationship("Order", secondary=room_collection_order)
    move_sizes = relationship("MoveSize", secondary=room_collection_move_size)


class MoveSize(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "move_size"
    order = relationship("Order")
    room_collections = relationship("RoomCollection", secondary=room_collection_move_size)


class Truck(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "truck"
    truck_type_id = Column(Integer, ForeignKey("truck_type.id"))
    truck_type = relationship("TruckType")


class TruckType(Base, mixin.IdMixin):
    __tablename__ = "truck_type"
    __table_args__ = (UniqueConstraint("height", "width", "length", name="_size"),)
    price = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    trucks = relationship("Truck")


class Calendar(Base, mixin.IdMixin):
    __tablename__ = "calendar"
    start_date = Column(Date, nullable=False, unique=True)
    end_date = Column(Date, nullable=False, unique=True)
    price_tag_id = Column(Integer, ForeignKey("price_tag.id"), nullable=False)
    price_tag = relationship("PriceTag", lazy="joined")


class PriceTag(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "price_tag"
    price = Column(Integer, nullable=False, unique=True)
    calendar = relationship("Calendar")


class Services(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "services"
    order = relationship("Order")


class FloorsCollection(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "floor_collection"
    order = relationship("Order", secondary=floor_collection_order)


class Address(Base, mixin.IdMixin):
    __tablename__ = "address"
    __table_args__ = (UniqueConstraint("house_number", "zip_code_id", "street_id", "apartment", name="_address"),)
    house_number = Column(String, nullable=False)
    apartment = Column(String, nullable=True)
    zip_code_id = Column(Integer, ForeignKey("zip_code.id"), nullable=False)
    street_id = Column(Integer, ForeignKey("street.id"), nullable=False)
    zip_code = relationship("ZipCode", lazy="joined")
    street = relationship("Street", lazy="joined")
    order = relationship("Order")


class ZipCode(Base, mixin.IdMixin):
    __tablename__ = "zip_code"
    zip_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    address = relationship("Address")


class Street(Base, mixin.IdMixin):
    __tablename__ = "street"
    street_name = Column(String, nullable=False, unique=True)
    address = relationship("Address")
