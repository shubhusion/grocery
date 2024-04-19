from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Date, Float
from flask_login import UserMixin

db = SQLAlchemy()

# Class User (Customer/Manager)


class User(db.Model, UserMixin):
    username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    admin = Column(Boolean, nullable=False)
    cart = db.relationship("Cart", backref="user")

    def get_id(self):
        return self.username


class Section(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = db.relationship("Product", backref="section" , cascade="all,delete,delete-orphan")


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # manufacture_date = Column(Date, nullable=True)
    # expiry_date = Column(Date, nullable=True)
    unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    section_id = Column(Integer, ForeignKey("section.id"))
    cart = db.relationship(
        "Cart", backref="product", cascade="all,delete,delete-orphan"
    )
    orders = db.relationship(
        "OrderProduct", backref="product", cascade="all,delete,delete-orphan"
    )


class Order(db.Model):
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.username"))
    order_date = Column(Date, nullable=False)
    order_to_product = db.relationship("OrderProduct", backref="order")

    @property
    def total(self):
        sum = 0
        for order in self.order_to_product:
            sum = sum + order.amount
        return sum


class Cart(db.Model):
    user_id = Column(Integer, ForeignKey("user.username"), primary_key=True)
    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        primary_key=True,
    )
    quantity = Column(Integer, nullable=False, default=0)
    # user=db.relationship("User",backref="cart")
    # product=db.relationship("Product",backref="cart",cascade="all,delete,delete-orphan")

    @property
    def total(self):
        return self.quantity * self.product.price


class OrderProduct(db.Model):
    order_id = Column(Integer, ForeignKey("order.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    # product=db.relationship("Product",backref="OrderProduct",cascade="all,delete,delete-orphan")
    quantity = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)

    @property
    def amount(self):
        return self.quantity * self.rate
