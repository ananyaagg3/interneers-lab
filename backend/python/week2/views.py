import csv
import io

from django.shortcuts import render
from .serializers import ProductSerializer, DateRangeFilterSerializer, ProductCategorySerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .services import ProductService, ProductCategoryService
from bson import ObjectId
from datetime import datetime, timedelta

def csv_row_to_product_payload(row):
    key_map = {
        "qty": "quantity_within_the_warehouse",
        "quantity": "quantity_within_the_warehouse",
    }
    payload = {}
    for raw_key, raw_val in row.items():
        if raw_key is None:
            continue
        k = (raw_key or "").strip().lower().replace(" ", "_")
        k = key_map.get(k, k)
        if k not in (
            "name",
            "description",
            "price",
            "brand",
            "quantity_within_the_warehouse",
            "category",
        ):
            continue
        v = raw_val.strip() if isinstance(raw_val, str) else raw_val
        if k == "category" and (v is None or v == ""):
            continue
        payload[k] = v
    return payload


#week2
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = ProductService.get_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#week2
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    id = ObjectId(id)
    product = ProductService.get_product_by_id(id)
    
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
        
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = ProductService.update_product(id, serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        ProductService.delete_product(id)
        return Response(status=status.HTTP_204_NO_CONTENT)

#week3
@api_view(['GET'])
def product_updated_last_month(request):
    last_month = datetime.utcnow() - timedelta(days=30)
    products = Product.objects(updated_at__gte=last_month)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#week3
@api_view(['GET'])
def product_filter_by_date(request):
    serializer = DateRangeFilterSerializer(data=request.query_params)
    if serializer.is_valid():
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        products = Product.objects(created_at__gte=start_date, created_at__lte=end_date)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#week4
@api_view(['GET', 'POST'])
def product_category_list(request):

    if request.method == 'GET':
        product_categories = ProductCategoryService.get_product_categories()
        serializer = ProductCategorySerializer(product_categories, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = ProductCategoryService.create_category(serializer.data)
            return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#week4
@api_view(['GET', 'PUT', 'DELETE'])
def product_category_detail(request, id):
    id = ObjectId(id)
    category = ProductCategoryService.get_category_by_id(id)

    if not category:
        return Response({"error":"Category not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductCategorySerializer(category)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = ProductCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            category = ProductCategoryService.update_category(serializer.data, id)
            return Response(ProductCategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        ProductCategoryService.delete_category(id)
        return Response(status=status.HTTP_204_NO_CONTENT)

#week4
@api_view(['GET', 'POST'])
def products_by_category(request, id):
    category = ProductCategoryService.get_category_by_id(id)
    if not category:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        products = Product.objects(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            oid = ObjectId(product_id)
        except Exception:
            return Response({"error": "Invalid Product ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        product, err = ProductService.assign_product_to_category(oid, category)
        if err == "Product not found":
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    
#week4
@api_view(['DELETE'])
def remove_products_from_category(request, id, product_id):
    category = ProductCategoryService.get_category_by_id(id)
    if not category:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        oid = ObjectId(product_id)
    except Exception:
        return Response({"error": "Invalid Product ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    product, err = ProductService.remove_product_from_category(oid, category)
    if err == "Product not found":
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    if err == "Not in category":
        return Response({"error": "Product not in this category"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_204_NO_CONTENT)

#week4
@api_view(['POST'])
def products_bulk_csv(request):
    upload = request.FILES.get("file")
    if not upload:
        return Response({"error": "Attach a CSV file using the form field name: file"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        text = upload.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return Response({"error": "CSV must be UTF-8 encoded"}, status=status.HTTP_400_BAD_REQUEST)
    
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        return Response({"error": "CSV has no header row"}, status=status.HTTP_400_BAD_REQUEST)
    
    created = 0
    errors = []
    product_ids = []
    for row_num, row in enumerate(reader, start=2):
        if not row or not any((v or "").strip() for v in row.values()):
            continue
        payload = csv_row_to_product_payload(row)
        serializer = ProductSerializer(data=payload)
        if not serializer.is_valid():
            errors.append({"row": row_num, "errors": serializer.errors})
            continue
        try:
            product = ProductService.create_product(serializer.validated_data)
        except Exception as e:
            errors.append({"row": row_num, "errors": str(e)})
            continue
        created += 1
        product_ids.append(str(product.id))

    return Response(
        {
            "created": created,
            "failed": len(errors),
            "errors":errors,
            "product_ids": product_ids
        },
        status=status.HTTP_200_OK
    )


# FOR IN-MEMORY OPERATIONS
# products = []
# products_id_counter = 1

# @api_view(['GET', 'POST'])
# def product_list(request):
#     global products_id_counter

#     if request.method == 'GET':
#         return Response(products)
    
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             product = serializer.validated_data
#             product["id"] = products_id_counter
#             products_id_counter += 1
#             products.append(product)
#             return Response(product, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):

#     product = next((p for p in products if p["id"] == id), None)
    
#     if not product:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         return Response(product)
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(data=request.data)

#         if serializer.is_valid():
#             updated_data = serializer.validated_data
#             updated_data["id"] = id
#             products[products.index(product)] = updated_data
#             return Response(updated_data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         products.remove(product)
#         return Response(status=status.HTTP_204_NO_CONTENT)




# FOR PAGINATION
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.order_by('id')
#     serializer_class = ProductSerializer
#     pagination_class = LimitOffsetPagination
#     # pagination_class.page_size = 1
#     # pagination_class.page_query_param = 'pagenum'
#     # pagination_class.page_size_query_param = 'size'
#     # pagination_class.max_page_size = 2

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'


# NORMAL FIRST WAY
# Create your views here.
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

