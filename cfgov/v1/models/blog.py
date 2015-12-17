from .base import CFGOVPage

from sheerlike.models import SheerlikeWagtailPageMixin

class BlogPage(CFGOVPage, SheerlikeWagtailPageMixin):
    sheer_type = 'posts'
