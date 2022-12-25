import unittest

from core.rut import validate_rut, rut_to_dict

class TestRut(unittest.TestCase):
    def setUp(self) -> None:
        self.rut = "11.111.111-1"

    def test_validate_rut(self):
        self.assertTrue(validate_rut(self.rut))

    def test_rut_to_dict(self):
        self.assertEqual(
            rut_to_dict(self.rut),
            {
                "rut": "11111111",
                "dv": "1",
                "rutcntr": "11.111.111-1",
            },
        )