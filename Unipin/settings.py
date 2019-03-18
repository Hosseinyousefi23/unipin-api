try:
    from .local_settings import *
except (FileNotFoundError, ImportError):
    from .default_settings import *
