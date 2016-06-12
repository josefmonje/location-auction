# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20150328_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldprice',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
