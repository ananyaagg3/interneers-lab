from django.shortcuts import render
from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

products = []
products_id_counter = 1

@api_view(['GET', 'POST'])
def product_list(request):
    global products_id_counter

    if request.method == 'GET':
        return Response(products)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data
            product["id"] = products_id_counter
            products_id_counter += 1
            products.append(product)
            return Response(product, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):

    product = next((p for p in products if p["id"] == id), None)
    
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(product)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            updated_data = serializer.validated_data
            updated_data["id"] = id
            products[products.index(product)] = updated_data
            return Response(updated_data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)







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

