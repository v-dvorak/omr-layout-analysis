# This makes it possible to use "__subclasses__()" in app.__main__.py .

# Any other solution leads to circular dependencies
# or this method of loading all datasets not working.
from .dataset_base import Dataset_OMR       # noqa: F401
from .audiolabs import AudioLabs_v2         # noqa: F401
from .musicmapp import MuscimaPP            # noqa: F401