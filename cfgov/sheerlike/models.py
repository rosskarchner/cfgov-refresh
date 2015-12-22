from django.db import models

from wagtail.wagtailcore.models import Page

class SheerlikeWagtailPageMixin(models.Model):
    class Meta:
        abstract = True

    sheer_document = models.TextField(blank=True)
    sheer_document_type = models.CharField(max_length=255, blank=True)
    sheer_document_id = models.CharField(max_length=1000, blank=True)

    @classmethod
    def from_sheer_processor(cls,processor, reindex=False, **kwargs):
        
        instances = []
        generator = processor.processor_module.documents(processor.name,**processor.kwargs)
        
        for document in generator:
            field_values = cls.field_values_from_sheer_document(document)
            parent = cls.find_parent_for_document(document)
            document_type = processor.name
            document_id = document['_id']
            instances.append(cls(sheer_document_id=document_id,
                    sheer_document_type=document_type, 
                    sheer_document=document, **field_values))

        return instances

    @classmethod
    def field_values_from_sheer_document(cls,document):
        """Override this to populate other fields"""

        return {}

    @staticmethod
    def find_parent_for_document(document):
        raise NotImplementedError("You must implement find_parent_for_document")
