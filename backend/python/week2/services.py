from .repository import ProductRepository

class ProductService():

    @staticmethod
    def get_products():
        products = ProductRepository.get_products()
        return products
    
    @staticmethod
    def get_product_by_id(id):
        product = ProductRepository.get_product_by_id(id)
        return product

    @staticmethod
    def create_product(data):
        product = ProductRepository.create_product(data)
        return product

    @staticmethod
    def update_product(id, data):
        product = ProductRepository.update_product(id, data)
        return product
        
    @staticmethod
    def delete_product(id):
        return ProductRepository.delete_product(id)
        
