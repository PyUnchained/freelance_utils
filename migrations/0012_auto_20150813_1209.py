# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0011_auto_20150810_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='P4APayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.CharField(max_length=20, unique=True, null=True)),
                ('digest', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='callbacknotification',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='order',
            field=models.CharField(max_length=100, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='p4apayment',
            name='call_back',
            field=models.ForeignKey(to='freelance_utils.CallBackNotification', null=True),
        ),
    ]
