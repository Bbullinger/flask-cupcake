from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True
with app.app_context():
    db.drop_all()
    db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg",
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg",
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            Cupcake.query.delete()

        ########what is the syntax **CUPCAKE_DATA?########
        cupcake = Cupcake(**CUPCAKE_DATA)
        with app.app_context():
            db.session.add(cupcake)
            db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(
                data,
                {
                    "cupcakes": [
                        {
                            "id": self.cupcake.id,
                            "flavor": "TestFlavor",
                            "size": "TestSize",
                            "rating": 5,
                            "image_url": "http://test.com/cupcake.jpg",
                        }
                    ]
                },
            )

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(
                data,
                {
                    "cupcake": {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image_url": "http://test.com/cupcake.jpg",
                    }
                },
            )

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data["cupcake"]["id"], int)

            ############## WHAT IS del?##############
            del data["cupcake"]["id"]

            self.assertEqual(
                data,
                {
                    "cupcake": {
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image_url": "http://test.com/cupcake2.jpg",
                    }
                },
            )

            self.assertEqual(Cupcake.query.count(), 2)

    #####THIS IS MY CODE #######
    def test_patch_cupcake(self):
        with app.test_client() as client:

            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(
                url, json={"cupcake": {"flavor": "chocolate", "size": "humongous"}}
            )
            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(
                data,
                {
                    "flavor": "chocolate",
                    "size": "humongous",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg",
                },
            )

    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.josn

            self.assertEqual(data, {"message": "deleted"})
            self.assertEqual(Cupcake.query.count(), 0)
