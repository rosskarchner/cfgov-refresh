# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0013_add_sublanding'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('sheer_document', models.TextField(blank=True)),
                ('sheer_document_type', models.CharField(max_length=255, blank=True)),
                ('sheer_document_id', models.CharField(max_length=1000, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage', models.Model),
        ),
    ]
