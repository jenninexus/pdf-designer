import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("export_profile", Path(__file__).with_name("export-profile.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ExportTest(unittest.TestCase):
    def test_allowlist_and_default_email(self):
        person = {"name": "Alex Example", "contact": {"email": "other@example.org", "emailRules": {"default": "approved@example.org", "personal": "private@example.org"}, "web": "https://example.org", "location": "Somewhere", "salary": "100"}, "vault": {"claims": ["private"]}}
        self.assertEqual(module.extract(person), {"version": 1, "fields": {"fullName": "Alex Example", "email": "approved@example.org", "website": "https://example.org"}})

    def test_no_fallback_to_unapproved_email(self):
        with self.assertRaises(ValueError):
            module.extract({"contact": {"email": "other@example.org"}})

    def test_reject_control_characters(self):
        self.assertEqual(module.extract({"name": "A\nB", "contact": {"emailRules": {"default": "valid@example.org"}}})["fields"], {"email": "valid@example.org"})

    def test_output_path_boundary(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            allowed = root / "resumes" / "alex" / "resources" / "profile.json"
            self.assertEqual(module.validate_output(allowed, "alex", root), allowed.resolve())
            outside = Path(directory) / "private-profile.json"
            self.assertEqual(module.validate_output(outside, "alex", root), outside.resolve())
            for forbidden in (root / "docs" / "profile.json", root / "examples" / "profile.json", root / "resumes" / "other" / "resources" / "profile.json"):
                with self.assertRaises(ValueError):
                    module.validate_output(forbidden, "alex", root)

    def test_slug(self):
        self.assertTrue(module.SLUG.fullmatch("example-user_2"))
        for invalid in ("../user", "UPPER", "user.json", ""):
            self.assertFalse(module.SLUG.fullmatch(invalid))


if __name__ == "__main__":
    unittest.main()
