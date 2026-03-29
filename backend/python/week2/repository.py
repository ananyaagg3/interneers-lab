from .models import Product, ProductCategory
from bson import ObjectId

class ProductRepository():

    @staticmethod
    def get_products():
        products = Product.objects.all()
        return products
    
    @staticmethod
    def get_product_by_id(id):
        product = Product.objects(pk=id).first()
        return product

    @staticmethod
    def resolve_category(cat_id):
        if not cat_id:
            return None
        return ProductCategory.objects(pk=cat_id).first()

    @staticmethod
    def create_product(data):
        cat_id = data.pop("category", None)
        category = ProductRepository.resolve_category(cat_id)
        data["category"] = category
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update_product(id, data):
        product = Product.objects(pk=id).first()

        if not product:
            return None
        cat_id = data.pop("category", None)
        if cat_id is not None:
            data["category"] = ProductRepository.resolve_category(cat_id)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(id):
        product = Product.objects(pk=id).first()
            
        if product:    
            product.delete()
            return True
        return False
    
    @staticmethod
    def assign_product_to_category(product_id, category):
        product = Product.objects(pk=product_id).first()
        if not product:
            return None, "Product not found"
        product.category = category
        product.save()
        return product, None
    
    @staticmethod
    def remove_product_from_category(product_id, category):
        product = Product.objects(pk=product_id).first()
        if not product:
            return None, "Product not found"
        if not product.category or str(product.category.id) != str(category.id):
            return None, "Not in category"
        product.category = None
        product.save()
        return product, None
    

class ProductCategoryRepository():

    @staticmethod
    def get_product_categories():
        categories = ProductCategory.objects.all()
        return categories
    
    @staticmethod
    def get_category_from_id(id):
        category = ProductCategory.objects(pk=id).first()
        return category
    
    @staticmethod
    def create_category(data):
        category = ProductCategory(**data)
        category.save()
        return category
    
    @staticmethod
    def update_category(data, id):
        category = ProductCategory.objects(pk=id).first()

        if category:
            for key, values in data.items():
                setattr(category, key, values)
            category.save()
            return category
        return None
    
    @staticmethod
    def delete_category(id):
        category = ProductCategory.objects(pk=id).first()

        if category:
            category.delete()
            return True
        return False
    