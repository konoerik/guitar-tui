"""Placeholder test so pytest exits 0 until real tests are added."""


def test_package_importable() -> None:
    import guitar_tui

    assert guitar_tui.__version__ == "0.1.0"
