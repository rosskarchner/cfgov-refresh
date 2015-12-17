import os
import sys
import codecs

from collections import OrderedDict
import json

import glob
import importlib

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from sheerlike.helpers import IndexHelper

def read_json_file(path):
        if os.path.exists(path):
            with codecs.open(path, 'r', 'utf-8') as json_file:
                return json.loads(json_file.read(), object_pairs_hook=OrderedDict)


class ContentProcessor(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.processor_name = kwargs['processor']
        del kwargs['processor']
        self.processor_module = importlib.import_module(self.processor_name)
        self.kwargs = kwargs

    def documents(self):
        return self.processor_module.documents(self.name, **self.kwargs)

    def mapping(self):
        if 'mappings' in self.kwargs:
	    with file(self.kwargs['mappings']) as mapping_json:
		return json.load(mapping_json)
        else:
            return None


@transaction.atomic
def index_processor(es, index_name, processor, reindex=False, model_map=None):
    """
    Index all the documents provided by the given content processor for
    the given index in the given Elasticsearch instance.

    If reindex=True and the processor already exists the mapping in
    Elasticsearch will be destroyed and recreated and all documents will
    be created anew.
    """
    # If the mapping already exists, and we were called with the reindex
    # flag, remove the mapping.
    if model_map and processor.name in model_map:
        model = model_map[processor.name]
        records = model.from_sheer_processor(processor)
        [r.save() for r in records]
        return True

    mapping = es.indices.get_mapping(index=index_name, doc_type=processor.name)
    if mapping and reindex:
        print "removing existing mapping for %s (%s)" % (processor.name, processor.processor_name)
        es.indices.delete_mapping(index=index_name, doc_type=processor.name)
        mapping = {}

    # Then create the mapping if it does not exist
    if not mapping:
        print "creating mapping for %s (%s)" % (processor.name, processor.processor_name)
        # Only manually create the mapping if one is specified.
        # Otherwise, let Elasticsearch create a mapping
        mapping_supplied = processor.mapping()
        if mapping_supplied:
            es.indices.put_mapping(index=index_name,
                                   doc_type=processor.name,
                                   body={processor.name: mapping_supplied})
    # Keep track of whether the indexing process is successful
    # This is so the end user and/or Jenkins knows the job failed if everything
    # didn't index 100%
    index_success = True
    try:
        # Get the document iterator from the processor.
        document_iterator = processor.documents()
    except IOError:
        # A requests.exceptions.ConnectionError may be raised if the processor
        # can't connect to the API endpoint its getting the JSON from.
        document_iterator = []
        sys.stderr.write("error making connection for %s" % processor.name)
        index_success = False

    try:
        result = bulk(es, document_iterator, index = index_name)
    except ValueError:
        # There may be a ValueError (or JSONDecodeError, a subclass of
        # ValueError) raised by json.loads() with the API's supposedly JSON
        # output.
        sys.stderr.write("error reading documents for %s" % processor.name)
        index_success = False
    else:
        sys.stdout.write("indexed %s %s \n" % (result[0], processor.name))
    return index_success


def index(args, options):

    # This whole routine is probably being too careful
    # Explicit is better than implicit, though!
    index_processor_helper = IndexHelper()
    index_processor_helper.configure(options)
    # the IndexHelper singleton can be used in processors that
    # need to talk to elasticsearch

    es = Elasticsearch(options["elasticsearch"])
    index_name = options["index"]

    # If we're given args.reindex and NOT given a list of processors to reindex,
    # we're expected to reindex everything. Delete the existing index.
    if not options.get('processors') and options.get('reindex') and es.indices.exists(index_name):
        print "reindexing %s" % index_name
        es.indices.delete(index_name)

    # If the index doesn't exist, create it.
    if not es.indices.exists(index_name):
        if hasattr(settings, 'SHEER_ELASTICSEARCH_SETTINGS') :
            es.indices.create(index=index_name, body=json.dumps(settings.SHEER_ELASTICSEARCH_SETTINGS))
        else:
            es.indices.create(index=index_name)

    processors = settings.SHEER_PROCESSORS

    all_models = [ct.model_class() for ct in ContentType.objects.all()]
    models_for_sheer_types = {model.sheer_type:model for model in all_models if hasattr(model,'sheer_type')}

    selected_processor_names = options.get('processors', []) or []
    if len(selected_processor_names) > 0:
	configured_processors = [ContentProcessor(name, **details)
				     for name, details
				     in processors.iteritems() if name in selected_processor_names]

    else:
	configured_processors = [ContentProcessor(name, **details)
				     for name, details
				     in processors.iteritems()]


    # If any specific content processors were selected, we run them. Otherwise
    # we run all of them.

    #if  len(options['processors']) > 0:
    #    selected_processors = [p for p in processors if p.name in optionsprocessors]

    failed_processors = []
    for processor in configured_processors:
        index_sucess = index_processor(es,
                                       index_name,
                                       processor,
                                       reindex=options.get('reindex'),
                                       model_map=models_for_sheer_types)
    if not index_sucess:
        failed_processors.append(processor.name)
    # Exit with an error code != 0 if there were any issues with indexing
    if failed_processors:
        sys.exit("Indexing the following processor(s) failed: {}".format(
            ", ".join(failed_processors)))
