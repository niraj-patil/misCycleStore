# Generated by Django 4.0.2 on 2022-03-20 13:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cycleStoreApp', '0002_employee_finances_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='finances',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='finances',
            name='type',
            field=models.CharField(choices=[('-', 'Debit'), ('+', 'Credit'), ('~', 'Values')], default=datetime.datetime(2022, 3, 20, 13, 36, 34, 16415, tzinfo=utc), max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='finances',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
