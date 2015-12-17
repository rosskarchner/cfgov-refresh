from django.conf import settings
from .base import *
from .events import *
from .molecules import *
from .organisms import *
from .snippets import *
from .landing_page import *
from .sublanding_page import *
from .blog import *
from .ref import *

if settings.DEBUG:
    from .demo import *
