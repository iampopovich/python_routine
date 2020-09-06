import requests
import unittest


def order_create(data=None):  # ms
    data = {
        "id": 0,
        "petId": 0,
        "quantity": 0,
        "shipDate": "2020-06-18T19:20:47.565Z",
        "status": "placed",
        "complete": True
    }
    req = requests.post(
        "https://petstore.swagger.io/v2/store/order",
        json=data)
    return req.elapsed.total_seconds()


def order_get_by_id(_id=1):
    req = requests.get(
        'https://petstore.swagger.io/v2/store/order/{}'.format(_id)
    )
    return req.status_code


class testOrderCreate(unittest.TestCase):

    def test_order_create(self):
        time = order_create()
        self.assertLessEqual(time, 200)


class testOrderGetByID(unittest.TestCase):

    def test_order_get_by_id(self):
        code = order_get_by_id()
        self.assertEqual(code, 210)


if __name__ == '__main__':
    unittest.main()
