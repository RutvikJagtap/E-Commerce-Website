from django.db import models
from db_connection import db

# Create your models here.
person_collection = db["Person"]

cart = db["Cart"]

products = db["Products"]

orders = db["Order"]