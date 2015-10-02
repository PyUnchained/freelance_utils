# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_number', models.CharField(max_length=12, null=True)),
                ('bal', models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BaseTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('date', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OnlineTransaction',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelance_utils.BaseTransaction')),
                ('is_verified', models.BooleanField(default=False)),
            ],
            bases=('freelance_utils.basetransaction',),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelance_utils.BaseTransaction')),
                ('type', models.CharField(max_length=1, choices=[(b'C', b'Credit'), (b'D', b'Debit'), (b'R', b'Refund')])),
            ],
            bases=('freelance_utils.basetransaction',),
        ),
        migrations.AddField(
            model_name='basetransaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='history',
            field=models.ManyToManyField(to='freelance_utils.Transaction', blank=True),
        ),
    ]
