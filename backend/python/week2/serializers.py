from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'brand', 'quantity_within_the_warehouse']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate_quantity_within_the_warehouse(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value