#!/usr/bin/python3
"""
This module contains the TestStateDocs and TestState classes.
These classes are used for testing the State class's documentation,
adherence to coding standards (PEP8), and its overall functionality.
"""

from datetime import datetime  # Importing datetime for timestamp comparison
import inspect  # Used for inspecting class methods and functions
import models  # Importing the main models module
from models import state  # Importing the state model
from models.base_model import BaseModel  # Importing the BaseModel class
import pep8  # Module for checking PEP8 compliance
import unittest  # Importing the unittest module for creating test cases

State = state.State  # Creating an alias for easier access to the State class


class TestStateDocs(unittest.TestCase):
    """
    This class contains tests to check the documentation and style
    of the State class, including PEP8 compliance and the presence of docstrings.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up method called once before running the tests.
        Inspects the State class to gather all its methods,
        so they can be tested for proper documentation.
        """
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """
        Test to ensure that the models/state.py file conforms to PEP8 standards.
        PEP8 is the style guide for Python code, ensuring readability and consistency.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in models/state.py.")

    def test_pep8_conformance_test_state(self):
        """
        Test to ensure that the tests/test_models/test_state.py file conforms to PEP8 standards.
        Maintaining consistent style in test files is important for readability and maintainability.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in tests/test_models/test_state.py.")

    def test_state_module_docstring(self):
        """
        Test to verify that the state.py module contains a docstring.
        A module-level docstring is essential for understanding the purpose
        and functionality of the module.
        """
        self.assertIsNot(state.__doc__, None,
                         "The state.py module needs a docstring for clarity.")
        self.assertTrue(len(state.__doc__) >= 1,
                        "The state.py module needs a descriptive docstring.")

    def test_state_class_docstring(self):
        """
        Test to verify that the State class contains a docstring.
        Class-level docstrings should explain the role and responsibilities of the class.
        """
        self.assertIsNot(State.__doc__, None,
                         "The State class needs a docstring for clarity.")
        self.assertTrue(len(State.__doc__) >= 1,
                        "The State class needs a descriptive docstring.")

    def test_state_func_docstrings(self):
        """
        Test to verify that all methods in the State class contain docstrings.
        Method-level docstrings should explain what each method does,
        the parameters it takes, and the return value.
        """
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "The {:s} method needs a docstring.".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "The {:s} method needs a descriptive docstring.".format(func[0]))


class TestState(unittest.TestCase):
    """
    This class contains tests to verify the functionality of the State class.
    It includes tests to check whether the State class inherits from BaseModel,
    and whether the class's attributes and methods work as expected.
    """

    def test_is_subclass(self):
        """
        Test to confirm that the State class is a subclass of BaseModel.
        This ensures that the State class inherits the core functionality
        provided by the BaseModel class, such as unique ID generation
        and automatic timestamping.
        """
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """
        Test to ensure that the State class has a 'name' attribute,
        and that its default value is an empty string or None depending
        on the storage type (file storage or database storage).
        """
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """
        Test the to_dict method of the State class to ensure it creates
        a dictionary containing all the appropriate attributes.
        This dictionary is used for serialization and deserialization
        of State objects.
        """
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """
        Test the values within the dictionary returned by the to_dict method.
        Ensures that date and time attributes are correctly converted to strings
        and match the format specified.
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """
        Test the __str__ method of the State class to ensure it returns
        the expected string representation. This is important for debugging
        and logging purposes, as it provides a human-readable output.
        """
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))

