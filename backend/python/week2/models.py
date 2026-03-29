from mongoengine import Document, StringField, IntField, DecimalField, DateTimeField, ReferenceField
from datetime import datetime


class ProductCategory(Document):
    title = StringField(max_length=200)
    description = StringField()

    def __str__(self):
        return f'{self.title}'


class Product(Document):
    name = StringField(max_length=200)
    description = StringField()
    # category = StringField(max_length=100)
    category = ReferenceField(ProductCategory, null=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    brand = StringField(max_length=100)
    quantity_within_the_warehouse = IntField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.brand}'
    




# from django.db import models

# # Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     brand = models.CharField(max_length=100)
#     quantity_within_the_warehouse = models.IntegerField()

#     def __str__(self):
#         return self.name + ' ' + self.brand

