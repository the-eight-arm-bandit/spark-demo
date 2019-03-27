import unittest

from lib.parse_logs import field_from_log


class TestFieldsFromEventLog(unittest.TestCase):
    def test_that_it_is_parsed_correctly(self):
        line = 'k=b647816af4ec42e5994eb622e3087d11	y={"geo": {"country": "can"}}'
        self.assertEqual(
            field_from_log(line),
            ("b647816af4ec42e5994eb622e3087d11", "can")
        )


"""
PYTHONPATH=/usr/lib/spark/python:$PYTHONPATH py.test tests/test_parse_logs.py
"""
