# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldprice',
            name='date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
