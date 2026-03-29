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