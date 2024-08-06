#!/usr/bin/python3
"""Unit tests for the BaseModel class to ensure expected behavior and proper documentation."""

from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock

# Import the BaseModel class from the models.base_model module
BaseModel = models.base_model.BaseModel

# Get the module docstring for models.base_model
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests for checking the documentation and PEP8 style compliance of BaseModel."""

    @classmethod
    def setUpClass(self):
        """Set up the methods for testing docstrings before running any tests."""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py and its corresponding test file conform to PEP8 style."""
        for path in ['models/base_model.py', 'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0, f"PEP8 errors found in {path}")

    def test_module_docstring(self):
        """Test for the existence of a module-level docstring in models/base_model.py."""
        self.assertIsNot(module_doc, None, "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base_model.py needs a more descriptive docstring")

    def test_class_docstring(self):
        """Test for the presence of a class-level docstring in the BaseModel class."""
        self.assertIsNot(BaseModel.__doc__, None, "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1, "BaseModel class needs a more descriptive docstring")

    def test_func_docstrings(self):
        """Test that all methods of the BaseModel class have appropriate docstrings."""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None, f"{func[0]} method needs a docstring")
                self.assertTrue(len(func[1].__doc__) > 1, f"{func[0]} method needs a more descriptive docstring")


class TestBaseModel(unittest.TestCase):
    """Tests for the correct functionality of the BaseModel class."""

    def test_instantiation(self):
        """Test the creation of a BaseModel instance and its attributes."""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test the creation times of two BaseModel instances and ensure they have unique datetime attributes."""
        tic = datetime.now()
        inst1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)  # Short sleep to differentiate the creation times
        tic = datetime.now()
        inst2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that each BaseModel instance has a unique id and it's in the UUID format."""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid, '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test that the to_dict method returns a dictionary containing all expected attributes."""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "name", "my_number", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """Test that the values returned by to_dict are correctly formatted as strings."""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the string representation of BaseModel matches the expected format."""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that the save method updates `updated_at` and calls `storage.save`."""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)

