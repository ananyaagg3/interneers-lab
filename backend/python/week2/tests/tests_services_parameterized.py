from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase
from week2.services import ProductService, ProductCategoryService

class ProductServiceParameterizedTests(SimpleTestCase):

    @patch("week2.services.ProductRepository")
    def test_get_products(self, mock_repo):
        cases = [
            ([], []),
            (["a"], ["a"]),
            (["x", "y"], ["x", "y"]),
        ]
        for repo_return, expected in cases:
            with self.subTest(repo_return=repo_return):
                mock_repo.get_products.reset_mock()
                mock_repo.get_products.return_value = repo_return
                result = ProductService.get_products()
                mock_repo.get_products.assert_called_once_with()
                self.assertEqual(result, expected)

    @patch("week2.services.ProductRepository")
    def test_delete_product(self, mock_repo):
        for return_value in (True, False):
            with self.subTest(return_value=return_value):
                mock_repo.delete_product.reset_mock()
                mock_repo.delete_product.return_value = return_value
                oid = MagicMock()
                result = ProductService.delete_product(oid)
                mock_repo.delete_product.assert_called_once_with(oid)
                self.assertIs(result, return_value)

    @patch("week2.services.ProductRepository")
    def test_assign_product_to_category(self, mock_repo):
        pid = MagicMock()
        category = MagicMock()
        cases = [
            (("saved_product", None), ("saved_product", None)),
            ((None, "Product not found"), (None, "Product not found")),
        ]
        for repo_return, expected in cases:
            with self.subTest(repo_return=repo_return):
                mock_repo.assign_product_to_category.reset_mock()
                mock_repo.assign_product_to_category.return_value = repo_return
                result = ProductService.assign_product_to_category(pid, category)
                mock_repo.assign_product_to_category.assert_called_once_with(pid, category)
                self.assertEqual(result, expected)

    @patch("week2.services.ProductRepository")
    def test_remove_product_from_category(self, mock_repo):
        pid = MagicMock()
        category = MagicMock()
        cases = [
            (("prod", None), ("prod", None)),
            ((None, "Product not found"), (None, "Product not found")),
            ((None, "Not in category"), (None, "Not in category")),
        ]

        for repo_return, expected in cases:
            with self.subTest(repo_return=repo_return):
                mock_repo.remove_product_from_category.reset_mock()
                mock_repo.remove_product_from_category.return_value = repo_return
                result = ProductService.remove_product_from_category(pid, category)
                mock_repo.remove_product_from_category.assert_called_once_with(pid, category)
                self.assertEqual(result, expected)


class ProductCategoryServiceParameterizedTests(SimpleTestCase):

    @patch("week2.services.ProductCategoryRepository")
    def test_get_product_categories(self, mock_repo):
        cases = [[], ["only"], ["a", "b", "c"]]
        for repo_return in cases:
            with self.subTest(repo_return=repo_return):
                mock_repo.get_product_categories.reset_mock()
                mock_repo.get_product_categories.return_value = repo_return
                result = ProductCategoryService.get_product_categories()
                mock_repo.get_product_categories.assert_called_once_with()
                self.assertEqual(result, repo_return)

    @patch("week2.services.ProductCategoryRepository")
    def test_delete_category(self, mock_repo):
        for return_value in (True, False):
            with self.subTest(return_value=return_value):
                mock_repo.delete_category.reset_mock()
                mock_repo.delete_category.return_value = return_value
                oid = MagicMock()
                result = ProductCategoryService.delete_category(oid)
                mock_repo.delete_category.assert_called_once_with(oid)
                self.assertIs(result, return_value)
