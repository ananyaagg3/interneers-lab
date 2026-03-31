from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from week2.tests.integration.base import MongoIntegrationTestCase

class ProductApisE2ETests(MongoIntegrationTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_end_to_end_product_category_and_remove_flow(self):
        #create category
        cat_payload = {
            "title": "E2E Category",
            "description": "For integration flow"
        }
        cat_resp = self.client.post("/category/", cat_payload, format="json")
        self.assertEqual(cat_resp.status_code, 201)
        category_id = cat_resp.data["id"]

        #create product in the category
        product_payload = {
            "name": "E2E Pen",
            "description": "Smooth",
            "category": category_id,
            "price": "10.00",
            "brand": "Reynolds",
            "quantity_within_the_warehouse": 12,
        }
        create_resp = self.client.post("/products/", product_payload, format="json")
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.data["id"]
        self.assertEqual(create_resp.data["category"], category_id)
        self.assertEqual(create_resp.data["category_title"], "E2E Category")

        #category products list
        list_resp = self.client.get(f"/category/{category_id}/products/")
        self.assertEqual(list_resp.status_code, 200)
        self.assertTrue(any(p["id"] == product_id for p in list_resp.data))

        #remove product from category
        remove_resp = self.client.delete(f"/category/{category_id}/products/{product_id}/")
        self.assertEqual(remove_resp.status_code, 204)

        #product detail - unlink from category check
        detail_resp = self.client.get(f"/products/{product_id}/")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIsNone(detail_resp.data["category"])

    def test_bulk_csv_upload_creates_products(self):
        csv_bytes = (
            b"name,description,price,brand,quantity_within_the_warehouse,category\n"
            b"CSV Pen,Smooth,10.50,Reynolds,90,\n"
            b"CSV Book,Ruled pages,20.00,Classmate,40,\n"
        )
        upload = SimpleUploadedFile("products.csv", csv_bytes, content_type="text/csv")

        resp = self.client.post("/products/bulk/", {"file": upload}, format="multipart")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["created"], 2)
        self.assertEqual(resp.data["failed"], 0)
        self.assertEqual(len(resp.data["product_ids"]), 2)
