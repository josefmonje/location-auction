# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_soldprice_geom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='geom',
            new_name='point',
        ),
        migrations.RenameField(
            model_name='soldprice',
            old_name='geom',
            new_name='point',
        ),
    ]
