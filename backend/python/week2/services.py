from .repository import ProductRepository, ProductCategoryRepository

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
    
    @staticmethod
    def assign_product_to_category(product_id, category):
        return ProductRepository.assign_product_to_category(product_id, category)
    
    @staticmethod
    def remove_product_from_category(product_id, category):
        return ProductRepository.remove_product_from_category(product_id, category)
    

class ProductCategoryService():

    @staticmethod
    def get_product_categories():
        return ProductCategoryRepository.get_product_categories()
    
    @staticmethod
    def get_category_by_id(id):
        return ProductCategoryRepository.get_category_from_id(id)
    
    @staticmethod
    def create_category(data):
        return ProductCategoryRepository.create_category(data)
    
    @staticmethod
    def update_category(data, id):
        return ProductCategoryRepository.update_category(data, id)
    
    @staticmethod
    def delete_category(id):
        return ProductCategoryRepository.delete_category(id)
    