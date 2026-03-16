from .models import Product

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
    def create_product(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update_product(id, data):
        product = Product.objects(pk=id).first()

        if product:
            for key, value in data.items():
                setattr(product, key, value)
            product.save()
            return product
        return None
        
        
    @staticmethod
    def delete_product(id):
        product = Product.objects(pk=id).first()
            
        if product:    
            product.delete()
            return True
        return False
        
