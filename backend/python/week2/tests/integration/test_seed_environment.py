from week2.models import Product, ProductCategory
from week2.tests.integration.base import MongoIntegrationTestCase

class SeedEnvironmentTests(MongoIntegrationTestCase):
    def test_default_categories_exist(self):
        self.assertGreaterEqual(ProductCategory.objects.count(), 3)
        self.assertTrue(ProductCategory.objects(title="Food").first())

    def test_integration_seed_product_exists(self):
        p = Product.objects(name="__integration_seed_product__").first()
        self.assertIsNotNone(p)
        self.assertEqual(p.brand, "TestBrand")