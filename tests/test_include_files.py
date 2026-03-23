"""Tests for include_files() fnmatch pattern support."""

import importlib
import sys
from pathlib import Path

# Import yesc.py directly (avoid conflict with installed single-file module)
for _key in list(sys.modules):
    if _key == "yesc" or _key.startswith("yesc."):
        del sys.modules[_key]
_script_path = Path(__file__).resolve().parent.parent / "yesc.py"
_spec = importlib.util.spec_from_file_location("yesc_module", _script_path)
_yesc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_yesc)
include_files = _yesc.include_files


def test_empty_exclude_includes_all():
    """Empty exclude string includes all files."""
    assert include_files("any.txt", "") is True


def test_exact_match_excludes():
    """Exact filename match excludes the file."""
    assert include_files("Thumbs.db", "Thumbs.db") is False


def test_exact_no_match_includes():
    """Non-matching filename is included."""
    assert include_files("photo.jpg", "Thumbs.db") is True


def test_substring_bug_fixed():
    """Partial filename must not match — regression test for substring bug."""
    assert include_files("dat", "data,photo.jpg") is True
    assert include_files("hoto", "data,photo.jpg") is True
    assert include_files("oto.jp", "data,photo.jpg") is True


def test_multiple_exact_names():
    """Multiple comma-separated exact names: match and no-match."""
    exclude = "Thumbs.db,.DS_Store,desktop.ini"
    assert include_files("Thumbs.db", exclude) is False
    assert include_files(".DS_Store", exclude) is False
    assert include_files("desktop.ini", exclude) is False
    assert include_files("photo.jpg", exclude) is True


def test_fnmatch_wildcard_star():
    """Star wildcard matches any characters."""
    assert include_files("._photo.jpg", "._*") is False
    assert include_files("._anything", "._*") is False
    assert include_files("photo.jpg", "._*") is True


def test_fnmatch_wildcard_question():
    """Question mark matches exactly one character."""
    assert include_files("a1.tmp", "a?.tmp") is False
    assert include_files("ab.tmp", "a?.tmp") is False
    assert include_files("abc.tmp", "a?.tmp") is True


def test_fnmatch_bracket_pattern():
    """Bracket pattern matches character set."""
    assert include_files("file.jpg", "*.[jJ][pP][gG]") is False
    assert include_files("file.JPG", "*.[jJ][pP][gG]") is False
    assert include_files("file.png", "*.[jJ][pP][gG]") is True


def test_multiple_patterns():
    """Multiple patterns in comma-separated list."""
    exclude = "._*,~$*"
    assert include_files("._photo.tif", exclude) is False
    assert include_files("~$document.xlsx", exclude) is False
    assert include_files("photo.tif", exclude) is True


def test_whitespace_handling():
    """Whitespace around patterns is stripped."""
    assert include_files("._photo.tif", "._* , ~$*") is False
    assert include_files("~$doc.xlsx", "._* , ~$*") is False
    assert include_files("photo.tif", " ._* , ~$* ") is True


def test_no_print_output(capsys):
    """include_files must not print anything to stdout."""
    include_files("Thumbs.db", "Thumbs.db")
    include_files("photo.jpg", "Thumbs.db")
    include_files("any.txt", "")
    include_files("._file", "._*")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_called_with_filename_only():
    """All yesc call sites pass Path(file).name, not full paths.

    fnmatch * matches everything including /, but this is safe because
    yesc always passes just the filename (e.g., 'photo.tif', not
    'subdir/photo.tif'). Verify patterns work on bare filenames.
    """
    assert include_files("photo.tif", "*.tif") is False
    assert include_files("photo.tif", "*.jpg") is True
