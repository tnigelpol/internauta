# Generated by Django 3.1.2 on 2020-12-04 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nauta', '0015_auto_20201204_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='chapter',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
