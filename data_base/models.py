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
    "inventory_room_collection",
    Base.metadata,
    Column("inventory_id", Integer, ForeignKey("inventory.id")),
    Column("room_collection_id", Integer, ForeignKey("room_collection.id"))
)

inventory_inventory_collection = Table(
    "inventory_inventory_collections",
    Base.metadata,
    Column("inventory_id", Integer, ForeignKey("inventory.id")),
    Column("inventory_collection_id", Integer, ForeignKey("inventory_collection.id"))
)


class Inventory(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "inventory"
    height = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    dimension = Column(Float, nullable=False)
    unit = Column(Integer, nullable=True)
    room_collections = relationship("RoomCollection", secondary=inventory_room_collection)
    inventory_collections = relationship("InventoryCollection", secondary=inventory_inventory_collection)

    def __init__(self, name, unit=None, dimension=None, height=None, width=None, length=None, weight=None):
        if not dimension:
            if all((height, width, length)):
                dimension = height * width * length
        self.dimension = dimension
        self.name = name
        self.unit = unit
        self.height = height
        self.weight = weight
        self.width = width
        self.length = length


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
    estimated_cost = Column(String, nullable=False)
    estimated_hours = Column(String, nullable=False)
    movers = Column(Integer, nullable=False)
    truck_type = Column(Integer, nullable=False)
    travel_time = Column(Integer, nullable=False)
    create_date = Column(DateTime, default=dt.datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy="joined")
    address_from_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address_from = relationship("Address", lazy="joined", foreign_keys=[address_from_id])
    address_to_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address_to = relationship("Address", lazy="joined", foreign_keys=[address_to_id])
    move_size_id = Column(Integer, ForeignKey("move_size.id"), nullable=False)
    move_size = relationship("MoveSize", lazy="joined")
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False)
    service = relationship("Service", lazy="joined")
    floor_collection_from_id = Column(Integer, ForeignKey("floor_collection.id"), nullable=False)
    floor_collection_from = relationship("FloorsCollection", lazy="joined", foreign_keys=[floor_collection_from_id])
    floor_collection_to_id = Column(Integer, ForeignKey("floor_collection.id"), nullable=False)
    floor_collection_to = relationship("FloorsCollection", lazy="joined", foreign_keys=[floor_collection_to_id])
    inventory_orders = relationship("InventoryOrder")


class RoomCollection(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "room_collection"
    inventories = relationship("Inventory", secondary=inventory_room_collection)


class InventoryCollection(Base, mixin.IdMixin):
    __tablename__ = "inventory_collection"
    move_size_id = Column(Integer, ForeignKey("move_size.id"), nullable=False)
    move_size = relationship("MoveSize", lazy="joined")
    inventories = relationship("Inventory", secondary=inventory_inventory_collection)


class InventoryOrder(Base, mixin.IdMixin):
    __tablename__ = "inventory_order"
    amount = Column(Integer, nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    inventories = relationship("Inventory")
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    orders = relationship("Order")


class MoveSize(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "move_size"
    order = relationship("Order")
    inventory_collection = relationship("InventoryCollection")


class Truck(Base, mixin.IdMixin):
    __tablename__ = "truck"
    name = Column(String, nullable=False, unique=True)
    truck_type_id = Column(Integer, ForeignKey("truck_type.id", ondelete="CASCADE"), nullable=False)
    truck_type = relationship("TruckType", lazy="joined")


class TruckType(Base, mixin.IdMixin):
    __tablename__ = "truck_type"
    __table_args__ = (UniqueConstraint("height", "width", "length", name="_size"),)
    price = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    trucks = relationship("Truck", cascade="all, delete", passive_deletes=True)


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


class MoverPrice(Base, mixin.IdMixin):
    __tablename__ = "mover_price"
    movers = Column(Integer, nullable=False, unique=True)
    price = Column(Integer, nullable=False, unique=True)


class Service(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "service"
    order = relationship("Order")


class FloorsCollection(Base, mixin.IdMixin, mixin.NameMixin):
    __tablename__ = "floor_collection"


class Address(Base, mixin.IdMixin):
    __tablename__ = "address"
    __table_args__ = (UniqueConstraint("street", "zip_code_id", name="_address"),)
    street = Column(String, nullable=False)
    apartment = Column(String, nullable=True)
    zip_code_id = Column(Integer, ForeignKey("zip_code.id"), nullable=False)
    zip_code = relationship("ZipCode", lazy="joined")


class ZipCode(Base, mixin.IdMixin):
    __tablename__ = "zip_code"
    zip_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    address = relationship("Address")
