# Generated by Django 2.1.8 on 2019-04-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_creation', '0002_auto_20190407_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_details',
            name='title',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
