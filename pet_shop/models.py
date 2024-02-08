from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow

# internal imports
from .helpers import get_image
from .helpers import get_info  # added import for second api call


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)


    def set_id(self):
        return str(uuid.uuid4()) 
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    

class Product(db.Model):
    prod_id = db.Column(db.String, primary_key=True)
    animal_type = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(200))
    image = db.Column(db.String)
    description = db.Column(db.String(50000))
    price = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, animal_type, price, quantity, color="", image="", description=""):
        self.prod_id = self.set_id()
        self.animal_type = animal_type
        self.color = color
        self.image = self.set_image(image, animal_type)
        self.description = self.set_info(description, animal_type)  # tried setting description for api call
        self.price = price
        self.quantity = quantity

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, animal_type):
        if not image:
            image = get_image(animal_type)
        return image
    
    def decrement_quantity(self, quantity):
        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity
    
    def __repr__(self):
        return f"<Animal: {self.animal_type}>"
    
    # tried creating a method that will set the info into the discription similar to set_image method
    def set_info(self, description, animal_type):
        if not description:
            description = get_info(animal_type)
        return description
    
    

class ProductSchema(ma.Schema):
    class Meta:
        fields = ['prod_id', 'animal_type', 'color', 'image', 'description', 'price', 'quantity']

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)