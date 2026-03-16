from django.urls import path, re_path
from . import views


urlpatterns = [
    path("products/", views.product_list),
    path("products/lastmonth/", views.product_updated_last_month),
    path("products/filter/", views.product_filter_by_date),
    re_path(r"^products/(?P<id>[0-9a-fA-F]{24})/$", views.product_detail),

]

# urlpatterns = [
#     path("products/", views.ProductList.as_view()),
#     path("products/<int:id>/", views.ProductDetail.as_view()),
# ]
