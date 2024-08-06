#!/usr/bin/python3
"""
This module contains the TestUserDocs and TestUser classes.
These classes are used for testing the User class's documentation,
adherence to coding standards (PEP8), and its overall functionality.
"""

from datetime import datetime
import inspect  # Used for inspecting class methods and functions
import models  # Importing the main models module
from models import user  # Importing the user model
from models.base_model import BaseModel  # Importing the BaseModel class
import pep8  # Module for checking PEP8 compliance
import unittest  # Importing the unittest module for creating test cases

User = user.User  # Creating an alias for easier access to the User class


class TestUserDocs(unittest.TestCase):
    """
    This class contains tests to check the documentation and coding style
    of the User class. The tests include verifying PEP8 compliance,
    checking for module-level docstrings, class docstrings, and method docstrings.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up method called once before running the tests.
        Inspects the User class to gather all its methods,
        so they can be tested for proper documentation.
        """
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """
        Test to ensure that the models/user.py file conforms to PEP8 standards.
        PEP8 is the style guide for Python code, ensuring readability and consistency.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in models/user.py.")

    def test_pep8_conformance_test_user(self):
        """
        Test to ensure that the tests/test_models/test_user.py file conforms to PEP8 standards.
        Maintaining consistent style in test files is important for readability and maintainability.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings) in tests/test_models/test_user.py.")

    def test_user_module_docstring(self):
        """
        Test to verify that the user.py module contains a docstring.
        A module-level docstring is essential for understanding the purpose
        and functionality of the module.
        """
        self.assertIsNot(user.__doc__, None,
                         "The user.py module needs a docstring for clarity.")
        self.assertTrue(len(user.__doc__) >= 1,
                        "The user.py module needs a descriptive docstring.")

    def test_user_class_docstring(self):
        """
        Test to verify that the User class contains a docstring.
        Class-level docstrings should explain the role and responsibilities of the class.
        """
        self.assertIsNot(User.__doc__, None,
                         "The User class needs a docstring for clarity.")
        self.assertTrue(len(User.__doc__) >= 1,
                        "The User class needs a descriptive docstring.")

    def test_user_func_docstrings(self):
        """
        Test to verify that all methods in the User class contain docstrings.
        Method-level docstrings should explain what each method does,
        the parameters it takes, and the return value.
        """
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "The {:s} method needs a docstring.".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "The {:s} method needs a descriptive docstring.".format(func[0]))


class TestUser(unittest.TestCase):
    """
    This class contains tests to verify the functionality of the User class.
    It includes tests to check whether the User class inherits from BaseModel,
    and whether the class's attributes and methods work as expected.
    """

    def test_is_subclass(self):
        """
        Test to confirm that the User class is a subclass of BaseModel.
        This ensures that the User class inherits the core functionality
        provided by the BaseModel class, such as unique ID generation
        and automatic timestamping.
        """
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """
        Test to ensure that the User class has an 'email' attribute,
        and that its default value is an empty string or None depending
        on the storage type (file storage or database storage).
        """
        user = User()
        self.assertTrue(hasattr(user, "email"))
        if models.storage_t == 'db':
            self.assertEqual(user.email, None)
        else:
            self.assertEqual(user.email, "")

    def test_password_attr(self):
        """
        Test to ensure that the User class has a 'password' attribute,
        and that its default value is an empty string or None depending
        on the storage type (file storage or database storage).
        """
        user = User()
        self.assertTrue(hasattr(user, "password"))
        if models.storage_t == 'db':
            self.assertEqual(user.password, None)
        else:
            self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """
        Test to ensure that the User class has a 'first_name' attribute,
        and that its default value is an empty string or None depending
        on the storage type (file storage or database storage).
        """
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.first_name, None)
        else:
            self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """
        Test to ensure that the User class has a 'last_name' attribute,
        and that its default value is an empty string or None depending
        on the storage type (file storage or database storage).
        """
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.last_name, None)
        else:
            self.assertEqual(user.last_name, "")

    def test_to_dict_creates_dict(self):
        """
        Test the to_dict method of the User class to ensure it creates
        a dictionary containing all the appropriate attributes.
        This dictionary is used for serialization and deserialization
        of User objects.
        """
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
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
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """
        Test the __str__ method of the User class to ensure it returns
        the expected string representation. This is important for debugging
        and logging purposes, as it provides a human-readable output.
        """
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))

