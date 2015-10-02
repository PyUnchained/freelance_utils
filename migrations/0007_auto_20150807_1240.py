# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0006_auto_20150806_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='callbacknotification',
            old_name='checkout_id',
            new_name='checkout',
        ),
        migrations.RenameField(
            model_name='callbacknotification',
            old_name='merchant_id',
            new_name='merchant',
        ),
        migrations.RenameField(
            model_name='callbacknotification',
            old_name='order_id',
            new_name='order',
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
