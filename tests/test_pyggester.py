import unittest
from unittest.mock import patch
from pathlib import Path
from pyggester.pyggester import PyggesterDynamic


class PyggesterDynamicTestCase(unittest.TestCase):
    def setUp(self):
        self.pyggester = PyggesterDynamic("/path/to/files")

    def test_fetch_files(self):
        with patch.object(PyggesterDynamic, "fetch_files") as mock_fetch_files:
            mock_fetch_files.return_value = [
                ("/path/to/file1.py",),
                ("/path/to/file2.py",),
                ("/path/to/file3.py",),
            ]

            files = self.pyggester.fetch_files("/path/to/files")

            self.assertEqual(len(files), 3)
            self.assertEqual(files[0], ("/path/to/file1.py",))
            self.assertEqual(files[1], ("/path/to/file2.py",))
            self.assertEqual(files[2], ("/path/to/file3.py",))

    def test_transform_as(self):
        with patch.object(PyggesterDynamic, "transform_as") as mock_transform_as:
            mock_transform_as.return_value = "transformed code"

            code = "original code"
            # pylint: disable=E1111
            transformed_code = self.pyggester.transform_as("/path/to/file.py", code)

            self.assertEqual(transformed_code, "transformed code")

    def test_save_transformed_code(self):
        with patch.object(
            PyggesterDynamic, "save_transformed_code"
        ) as mock_save_transformed_code:
            original_path = Path("/path/to/file.py")
            code = "transformed code"

            self.pyggester.save_transformed_code(original_path, code)

            mock_save_transformed_code.assert_called_once_with(original_path, code)
