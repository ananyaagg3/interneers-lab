from rest_framework import serializers
from .models import Product, ProductCategory

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.CharField(max_length=100, required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(max_length=100, allow_blank=False)
    quantity_within_the_warehouse = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_brand(self, value):
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Brand is required and cannot be empty.")
        return str(value).strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate_quantity_within_the_warehouse(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.brand or not str(instance.brand).strip():
            data["brand"] = "Unspecified"
        cat = instance.category
        if cat:
            data["category"] = str(cat.id)
            data["category_title"] = cat.title
        else:
            data["category"] = None
            data["category_title"] = None
        return data


class DateRangeFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    

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