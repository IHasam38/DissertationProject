import ast
from datetime import datetime
from pathlib import Path
import unittest


SOURCE_FILE = (
    Path(__file__).resolve().parents[1]
    / "Source_code"
    / "smart_home_gui.py"
)


def load_validate_dob():
    tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "validate_dob"
    )
    isolated_module = ast.Module(body=[function], type_ignores=[])
    namespace = {"datetime": datetime}
    code = compile(
        ast.fix_missing_locations(isolated_module),
        str(SOURCE_FILE),
        "exec",
    )
    exec(code, namespace)
    return namespace["validate_dob"]


class TestValidateDOB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_dob = staticmethod(load_validate_dob())

    def test_valid_past_date(self):
        self.assertTrue(self.validate_dob("01/01/2000"))

    def test_malformed_date(self):
        self.assertFalse(self.validate_dob("not-a-date"))

    def test_impossible_date(self):
        self.assertFalse(self.validate_dob("31/02/2020"))

    def test_future_date(self):
        self.assertFalse(self.validate_dob("31/12/2999"))


if __name__ == "__main__":
    unittest.main()