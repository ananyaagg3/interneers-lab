from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView


def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    path(
        'product-tile/',
        TemplateView.as_view(template_name='week6/product_tile.html'),
        name='product_tile',
    ),
    path('', include('week1.urls')),
    path('', include('week2.urls')),
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
]

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server. Ananya this side.")

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', hello_world),
# ]
