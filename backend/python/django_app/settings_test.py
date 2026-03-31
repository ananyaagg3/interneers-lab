# Using a separate database so main database is not touched while running tests

import os

os.environ.setdefault("MONGO_DB_NAME", "week3_products_test")

from .settings import *