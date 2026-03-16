from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(max_length=100)
    quantity_within_the_warehouse = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate_quantity_within_the_warehouse(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    
class DateRangeFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'category', 'price', 'brand', 'quantity_within_the_warehouse']

#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Price must be positive")
#         return value
    
#     def validate_quantity_within_the_warehouse(self, value):
#         if value < 0:
#             raise serializers.ValidationError("Quantity cannot be negative")
#         return value