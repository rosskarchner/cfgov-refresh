from .local import *


MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware'
] + list(MIDDLEWARE_CLASSES)
