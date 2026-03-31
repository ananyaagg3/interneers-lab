from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase
from week2.services import ProductService, ProductCategoryService

@patch("week2.services.ProductRepository")
class ProductServiceTests(SimpleTestCase):
    def test_get_products(self, mock_repo):
        mock_repo.get_products.return_value = ["p1", "p2"]

        result = ProductService.get_products()

        mock_repo.get_products.assert_called_once_with()
        self.assertEqual(result, ["p1", "p2"])

    def test_get_product_by_id(self, mock_repo):
        oid = MagicMock()
        mock_repo.get_product_by_id.return_value = {"id": oid}

        result = ProductService.get_product_by_id(oid)

        mock_repo.get_product_by_id.assert_called_once_with(oid)
        self.assertEqual(result, {"id": oid})

    def test_create_product(self, mock_repo):
        data = {"name": "Pen", "brand": "X"}
        mock_repo.create_product.return_value = "saved"

        result = ProductService.create_product(data)

        mock_repo.create_product.assert_called_once_with(data)
        self.assertEqual(result, "saved")

    def test_update_product(self, mock_repo):
        oid = MagicMock()
        data = {"name": "Pen", "brand": "Y"}
        mock_repo.update_product.return_value = "updated"

        result = ProductService.update_product(oid, data)

        mock_repo.update_product.assert_called_once_with(oid, data)
        self.assertEqual(result, "updated")

    def test_delete_product(self, mock_repo):
        oid = MagicMock()
        mock_repo.delete_product.return_value = True

        result = ProductService.delete_product(oid)

        mock_repo.delete_product.assert_called_once_with(oid)
        self.assertTrue(result)

    def test_assign_product_to_category(self, mock_repo):
        pid = MagicMock()
        category = MagicMock()
        mock_repo.assign_product_to_category.return_value = ("prod", None)

        result = ProductService.assign_product_to_category(pid, category)

        mock_repo.assign_product_to_category.assert_called_once_with(pid, category)
        self.assertEqual(result, ("prod", None))

    def test_remove_product_from_category(self, mock_repo):
        pid = MagicMock()
        category = MagicMock()
        mock_repo.remove_product_from_category.return_value = ("prod", None)

        result = ProductService.remove_product_from_category(pid, category)

        mock_repo.remove_product_from_category.assert_called_once_with(pid, category)
        self.assertEqual(result, ("prod", None))


@patch("week2.services.ProductCategoryRepository")
class ProductCategoryServiceTests(SimpleTestCase):

    def test_get_product_categories(self, mock_repo):
        mock_repo.get_product_categories.return_value = ["c1"]

        result = ProductCategoryService.get_product_categories()

        mock_repo.get_product_categories.assert_called_once_with()
        self.assertEqual(result, ["c1"])

    def test_get_category_by_id(self, mock_repo):
        oid = MagicMock()
        mock_repo.get_category_from_id.return_value = "c1"

        result = ProductCategoryService.get_category_by_id(oid)

        mock_repo.get_category_from_id.assert_called_once_with(oid)
        self.assertEqual(result, "c1")

    def test_create_category(self, mock_repo):
        data = {"title": "t1", "description": "d1"}
        mock_repo.create_category.return_value = "Success"

        result = ProductCategoryService.create_category(data)

        mock_repo.create_category.assert_called_once_with(data)
        self.assertEqual(result, "Success")

    def test_update_category(self, mock_repo):
        oid = MagicMock()
        data = {"title": "t2"}
        mock_repo.update_category.return_value = "Updated"

        result = ProductCategoryService.update_category(data, oid)

        mock_repo.update_category.assert_called_once_with(data, oid)
        self.assertEqual(result, "Updated")
    
    def test_delete_category(self, mock_repo):
        oid = MagicMock()
        mock_repo.delete_category.return_value = True

        result = ProductCategoryService.delete_category(oid)

        mock_repo.delete_category.assert_called_once_with(oid)
        self.assertTrue(result)
