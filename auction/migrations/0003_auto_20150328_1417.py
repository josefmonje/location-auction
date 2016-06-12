# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auto_20150322_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='PAON',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='SAON',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='county',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='district',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='locality',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='old_new',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='paid_price',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='property_type',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='record',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='street',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='tenure',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldprice',
            name='town',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
