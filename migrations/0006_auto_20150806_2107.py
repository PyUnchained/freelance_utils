# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0005_auto_20150805_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallBackNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('merchant_id', models.CharField(max_length=50)),
                ('checkout_id', models.IntegerField()),
                ('order_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('digest', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='payments_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='basetransaction',
            name='amount',
            field=models.DecimalField(max_digits=7, decimal_places=2),
        ),
    ]
