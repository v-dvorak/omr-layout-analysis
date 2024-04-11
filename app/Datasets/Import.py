# This makes it possible to use "__subclasses__()" in app.__main__.py .

# Any other solution leads to circular dependencies
# or this method of loading all datasets not working.
from .DatasetOMR import Dataset_OMR       # noqa: F401
from .AudioLabs import AudioLabs_v2         # noqa: F401
from .MuscimaPP import MuscimaPP            # noqa: F401
