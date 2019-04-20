# Generated by Django 2.1.7 on 2019-04-20 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_creation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_tickets',
            name='addressed_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='all_tickets',
            name='read_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='all_tickets',
            name='resolved_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket_details',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='ticket_details',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
