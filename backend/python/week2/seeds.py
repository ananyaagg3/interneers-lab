#week4 advanced
def seed_product_categories():
    from .models import ProductCategory

    defaults = [
        ("Food", "Groceries, snacks, and packaged food."),
        ("Kitchen Essentials", "Cookware, utensils, and small appliances."),
        ("Stationary", "Pens, notebooks, and office supplies"),
    ]

    for title, description in defaults:
        if not ProductCategory.objects(title=title).first():
            ProductCategory(title=title, description=description).save()

#week5
def seed_test_data():
    from decimal import Decimal

    from .models import Product, ProductCategory

    seed_product_categories()
    if Product.objects(name="__integration_seed_product__").first():
        return
    cat = ProductCategory.objects(title="Food").first()
    Product(
        name="__integration_seed_product__",
        description="Created by seed_test_data for integration tests.",
        category=cat,
        price=Decimal("1.00"),
        brand="TestBrand",
        quantity_within_the_warehouse=1,
    ).save()

def clear_week2_collections():
    from django.conf import settings

    from .models import Product, ProductCategory

    db_name = getattr(settings, "MONGO_DB_NAME", None)
    if db_name != "week3_products_test":
        raise RuntimeError(
            "clear_week2_collections refused: use django_app.settings_test"
            f"(expected MONGO_DB_NAME 'week3_products_test', got {db_name!r})."
        )

    Product.drop_collection()
    ProductCategory.drop_collection()