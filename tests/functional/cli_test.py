from subprocess import run


def test_help():
    """Test the commando --help command."""
    run(["commando", "--help"], check=True)


def test_version():
    """Test the commando --version command."""
    run(["commando", "--version"], check=True)
