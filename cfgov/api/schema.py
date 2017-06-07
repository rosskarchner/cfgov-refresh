from __future__ import unicode_literals
import graphene
from graphene_django import DjangoObjectType
from v1.models.base import CFGOVPage

from django.db import models


class CFGOVPageNode(DjangoObjectType):
    class Meta:
        model = CFGOVPage
        only_fields = ['title', 'date','url']


class Query(graphene.ObjectType):
    pages = graphene.List(CFGOVPageNode)

    @graphene.resolve_only_args
    def resolve_pages(self):
        return CFGOVPage.objects.live()

schema = graphene.Schema(query=Query)
