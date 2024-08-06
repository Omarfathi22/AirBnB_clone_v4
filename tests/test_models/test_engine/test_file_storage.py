#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes for testing
the FileStorage class, including documentation, style compliance, and functionality.
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

# Reference to the FileStorage class and a dictionary mapping class names to their respective models
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests for checking the documentation and style compliance of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class by retrieving all methods of FileStorage for documentation checks."""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Check that models/engine/file_storage.py conforms to PEP8 style guide."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (or warnings) in models/engine/file_storage.py.")

    def test_pep8_conformance_test_file_storage(self):
        """Check that tests/test_models/test_file_storage.py conforms to PEP8 style guide."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (or warnings) in tests/test_models/test_file_storage.py.")

    def test_file_storage_module_docstring(self):
        """Verify the presence and content of the docstring in the file_storage.py module."""
        self.assertIsNot(file_storage.__doc__, None,
                         "The file_storage.py module needs a docstring.")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "The file_storage.py module docstring should be descriptive.")

    def test_file_storage_class_docstring(self):
        """Verify the presence and content of the docstring in the FileStorage class."""
        self.assertIsNot(FileStorage.__doc__, None,
                         "The FileStorage class needs a docstring.")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "The FileStorage class docstring should be descriptive.")

    def test_fs_func_docstrings(self):
        """Ensure all methods in the FileStorage class have docstrings."""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{} method needs a docstring.".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{} method docstring should be descriptive.".format(func[0]))


@unittest.skipIf(models.storage_t == 'db', "Skipping tests for non-File storage configurations.")
class TestFileStorage(unittest.TestCase):
    """Tests for the functionality of the FileStorage class."""

    def test_all_returns_dict(self):
        """Verify that the all() method returns the __objects attribute as a dictionary."""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict,
                         "The all() method should return a dictionary.")
        self.assertIs(new_dict, storage._FileStorage__objects,
                      "The dictionary returned by all() should be the same as the internal __objects attribute.")

    def test_new(self):
        """Verify that the new() method correctly adds an object to the __objects attribute."""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects,
                                 "The new() method should add the object to __objects correctly.")
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """Verify that the save() method correctly saves objects to file.json."""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js),
                         "The save() method should write objects to file.json correctly.")

    def test_get(self):
        """Verify that the get() method retrieves an object of a given class by its ID."""
        storage = models.storage
        obj = State(name='Michigan')
        obj.save()
        # Check if the object can be retrieved by its ID
        self.assertEqual(obj.id, storage.get(State, obj.id).id)
        self.assertEqual(obj.name, storage.get(State, obj.id).name)
        # Verify that incorrect IDs or class types return None
        self.assertIsNot(obj, storage.get(State, obj.id + 'op'))
        self.assertIsNone(storage.get(State, obj.id + 'op'))
        self.assertIsNone(storage.get(State, 45))
        self.assertIsNone(storage.get(None, obj.id))
        self.assertIsNone(storage.get(int, obj.id))
        # Ensure that improper arguments raise TypeError
        with self.assertRaises(TypeError):
            storage.get(State, obj.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(State)
        with self.assertRaises(TypeError):
            storage.get()

    def test_count(self):
        """Verify that the count() method returns the number of objects of a given class."""
        storage = models.storage
        # Check the count of objects for various cases
        self.assertIs(type(storage.count()), int,
                      "The count() method should return an integer.")
        self.assertIs(type(storage.count(None)), int,
                      "The count() method should return an integer when no class is specified.")
        self.assertIs(type(storage.count(int)), int,
                      "The count() method should return an integer when an invalid class is specified.")
        self.assertIs(type(storage.count(State)), int,
                      "The count() method should return an integer for a valid class.")
        self.assertEqual(storage.count(), storage.count(None),
                         "The count() method should be consistent when no class is specified.")
        State(name='Lagos').save()
        self.assertGreater(storage.count(State), 0,
                           "The count() method should be greater than 0 after adding an object.")
        self.assertEqual(storage.count(), storage.count(None),
                         "The count() method should be consistent after adding an object.")
        a = storage.count(State)
        State(name='Enugu').save()
        self.assertGreater(storage.count(State), a,
                           "The count() method should increase after adding more objects.")
        Amenity(name='Free WiFi').save()
        self.assertGreater(storage.count(), storage.count(State),
                           "The count() method should reflect changes in total object count.")
        # Verify that passing an incorrect argument raises TypeError
        with self.assertRaises(TypeError):
            storage.count(State, 'op')

