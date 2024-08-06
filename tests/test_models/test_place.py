#!/usr/bin/python3
"""
This module contains the TestPlaceDocs and TestPlace classes
which are used to test the Place class for proper documentation,
style compliance, and functionality.
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest
Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of the Place class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the inspect module to get all the functions of the Place class"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8 style guidelines"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in models/place.py")

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8 style guidelines"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in tests/test_models/test_place.py")

    def test_place_module_docstring(self):
        """Test for the presence of a module-level docstring in place.py"""
        self.assertIsNot(place.__doc__, None,
                         "models/place.py is missing a module docstring")
        self.assertTrue(len(place.__doc__) >= 1,
                        "models/place.py needs a more detailed docstring")

    def test_place_class_docstring(self):
        """Test for the presence of a class-level docstring in the Place class"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class is missing a class docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a more detailed docstring")

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in all methods of the Place class"""
        for func in self.place_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method is missing a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a more detailed docstring".format(func[0]))


class TestPlace(unittest.TestCase):
    """Tests the functionality and attributes of the Place class"""
    
    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id_attr(self):
        """Test that Place has the attribute city_id and it's initialized correctly"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        if models.storage_t == 'db':
            self.assertEqual(place.city_id, None)
        else:
            self.assertEqual(place.city_id, "")

    def test_user_id_attr(self):
        """Test that Place has the attribute user_id and it's initialized correctly"""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(place.user_id, None)
        else:
            self.assertEqual(place.user_id, "")

    def test_name_attr(self):
        """Test that Place has the attribute name and it's initialized correctly"""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        if models.storage_t == 'db':
            self.assertEqual(place.name, None)
        else:
            self.assertEqual(place.name, "")

    def test_description_attr(self):
        """Test that Place has the attribute description and it's initialized correctly"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        if models.storage_t == 'db':
            self.assertEqual(place.description, None)
        else:
            self.assertEqual(place.description, "")

    def test_number_rooms_attr(self):
        """Test that Place has the attribute number_rooms and it's initialized as an integer 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        if models.storage_t == 'db':
            self.assertEqual(place.number_rooms, None)
        else:
            self.assertEqual(type(place.number_rooms), int)
            self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test that Place has the attribute number_bathrooms and it's initialized as an integer 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        if models.storage_t == 'db':
            self.assertEqual(place.number_bathrooms, None)
        else:
            self.assertEqual(type(place.number_bathrooms), int)
            self.assertEqual(place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test that Place has the attribute max_guest and it's initialized as an integer 0"""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        if models.storage_t == 'db':
            self.assertEqual(place.max_guest, None)
        else:
            self.assertEqual(type(place.max_guest), int)
            self.assertEqual(place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test that Place has the attribute price_by_night and it's initialized as an integer 0"""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        if models.storage_t == 'db':
            self.assertEqual(place.price_by_night, None)
        else:
            self.assertEqual(type(place.price_by_night), int)
            self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test that Place has the attribute latitude and it's initialized as a float 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        if models.storage_t == 'db':
            self.assertEqual(place.latitude, None)
        else:
            self.assertEqual(type(place.latitude), float)
            self.assertEqual(place.latitude, 0.0)

    def test_longitude_attr(self):
        """Test that Place has the attribute longitude and it's initialized as a float 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        if models.storage_t == 'db':
            self.assertEqual(place.longitude, None)
        else:
            self.assertEqual(type(place.longitude), float)
            self.assertEqual(place.longitude, 0.0)

    @unittest.skipIf(models.storage_t == 'db', "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Test that Place has the attribute amenity_ids and it's initialized as an empty list"""
        place = Place()
        self.assertTrue(hasattr(place, "amenity_ids"))
        self.assertEqual(type(place.amenity_ids), list)
        self.assertEqual(len(place.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """Test that the to_dict method creates a dictionary with proper attributes"""
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that the values in the dictionary returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output format"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))

