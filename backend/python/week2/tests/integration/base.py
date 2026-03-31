from django.test import TestCase

from week2.seeds import clear_week2_collections, seed_test_data

class MongoIntegrationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        clear_week2_collections()
        seed_test_data()