# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0002_onlinetransaction_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='onlinetransaction',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'AT', b'Academics Tuition'), (b'PT', b'Professional Tuition'), (b'ET', b'ECD Tuition'), (b'AE', b'Academics Exam/Practical'), (b'PE', b'Professionals Exam/Practical'), (b'O', b'Other')]),
        ),
        migrations.AddField(
            model_name='account',
            name='services',
            field=models.ManyToManyField(to='freelance_utils.Service', null=True),
        ),
    ]
