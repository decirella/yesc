"""Tests that yesc can be imported as a library without triggering execution."""

import sys


def test_import_does_not_trigger_execution():
    """Importing yesc.yesc should not call parse_args() or main().

    Before the fix, importing yesc.yesc at module level calls
    parser.parse_args() and main(args), which fails or runs unintended code.
    After the fix, import should succeed silently.
    """
    # Remove yesc from sys.modules if previously imported, to test fresh import
    for key in list(sys.modules):
        if key == "yesc" or key.startswith("yesc."):
            del sys.modules[key]

    # This import should succeed without side effects
    from yesc.yesc import main

    assert callable(main)


def test_parser_not_at_module_level():
    """parser should only exist inside if __name__ == '__main__', not as a
    module attribute accessible on import."""
    from yesc import yesc as yesc_module

    assert not hasattr(yesc_module, "parser")
