import os
from cars_license_plates_db import DB
import parking_lot
import unittest

EXAMPLE_LICENSE_PLATES_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'example_images')

INVALID_IMAGE_FILE = 'not_exist_image.jpg'
INVALID_IMAGE_URL = 'http://not_exist_image.jpg'
NON_LICENSE_PLATE = 'https://i.ytimg.com/vi/4riem49Yjus/maxresdefault.jpg'

PRIVATE_CAR_LICENSE_PLATES = [os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'private_1.png'),
                              os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'private_2.jpg')]

MILITARY_LAW_ENFORCEMENT_LICENSE_PLATES = [os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'military_law_1.png'),
                                           os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'military_law_2.jpeg')]

GAS_OPERATOR_LICENSE_PLATES = [os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'gas_operator_1.jpg')]

PUBLIC_TRANSPORTATION_LICENSE_PLATES = [os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'public_1.png')]

PROHIBITED_LICENSE_PLATES = [os.path.join(EXAMPLE_LICENSE_PLATES_IMAGES_DIR, 'prohibited_plate_1.png')]


class TestParkingLot(unittest.TestCase):
    TEST_MODE = True
    db = DB(TEST_MODE)

    @classmethod
    def setUpClass(cls):
        cls.db.drop_table()
        cls.db.create_table()

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_table()

    def test_invalid_image_file(self):
        with self.assertRaises(Exception):
            parking_lot.process_licence_plate(INVALID_IMAGE_FILE, self.TEST_MODE)

    def test_invalid_image_url(self):
        with self.assertRaises(Exception):
            parking_lot.process_licence_plate(INVALID_IMAGE_URL, self.TEST_MODE)

    def test_non_license_plates(self):
        with self.assertRaises(Exception):
            parking_lot.process_licence_plate(NON_LICENSE_PLATE, self.TEST_MODE)

    def test_private_license_plates(self):
        for item in PRIVATE_CAR_LICENSE_PLATES:
            prohibited, car_type = parking_lot.process_licence_plate(item, self.TEST_MODE)
            self.assertFalse(prohibited)
            self.assertEqual(car_type, parking_lot.PRIVATE_VEHICLE_TYPE)

    def test_military_law_enforcement_license_plates(self):
        for item in MILITARY_LAW_ENFORCEMENT_LICENSE_PLATES:
            prohibited, car_type = parking_lot.process_licence_plate(item, self.TEST_MODE)
            self.assertTrue(prohibited)
            self.assertEqual(car_type, parking_lot.MILITARY_LAW_VEHICLE_TYPE)

    def test_gas_operator_license_plates(self):
        for item in GAS_OPERATOR_LICENSE_PLATES:
            prohibited, car_type = parking_lot.process_licence_plate(item, self.TEST_MODE)
            self.assertTrue(prohibited)
            self.assertEqual(car_type, parking_lot.GAS_OPERATOR_VEHICLE_TYPE)

    def test_public_transportation_license_plates(self):
        for item in PUBLIC_TRANSPORTATION_LICENSE_PLATES:
            prohibited, car_type = parking_lot.process_licence_plate(item, self.TEST_MODE)
            self.assertTrue(prohibited)
            self.assertEqual(car_type, parking_lot.PUBLIC_TRANSPORTATION_VEHICLE_TYPE)

    def test_prohibited_license_plates(self):
        for item in PROHIBITED_LICENSE_PLATES:
            prohibited, car_type = parking_lot.process_licence_plate(item, self.TEST_MODE)
            self.assertTrue(prohibited)
            self.assertEqual(car_type, parking_lot.PRIVATE_VEHICLE_TYPE)


if __name__ == '__main__':
    unittest.main()
