# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import auction.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lot', models.CharField(max_length=20, null=True, blank=True)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/static/', location=b'staticfiles'), null=True, upload_to=auction.models.upload_to_db, blank=True)),
                ('image_src', models.CharField(max_length=150, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('town', models.CharField(max_length=30, null=True, blank=True)),
                ('postcode', models.CharField(max_length=20, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('guide_price', models.CharField(max_length=30, null=True, blank=True)),
                ('price', models.FloatField(null=True)),
                ('auctioneer', models.CharField(max_length=50, null=True, blank=True)),
                ('auction_date', models.DateField(null=True, blank=True)),
                ('lease_details', models.TextField(null=True, blank=True)),
                ('vendor', models.CharField(max_length=50, null=True, blank=True)),
                ('viewing_time', models.TextField(null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Geocode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postcode', models.CharField(unique=True, max_length=10)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoldPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('LR_ID', models.CharField(max_length=38, null=True, blank=True)),
                ('paid_price', models.FloatField(null=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('postcode', models.CharField(max_length=8, null=True, blank=True)),
                ('property_type', models.CharField(max_length=1)),
                ('old_new', models.CharField(max_length=1)),
                ('tenure', models.CharField(max_length=1)),
                ('PAON', models.CharField(max_length=100)),
                ('SAON', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=50)),
                ('town', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('record', models.CharField(max_length=1)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
