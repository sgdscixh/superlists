""" dummy test """
from django.test import TestCase


class SmokeTest(TestCase):
    """dummy test"""

    def test_bad_maths(self):
        """dummy test"""
        self.assertEqual(1 + 2, 3)
