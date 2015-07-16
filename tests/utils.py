def is_lib_available(library):
    """
    Check if a Python library is available.
    """
    try:
        __import__(library)
        return True
    except ImportError:
        return False