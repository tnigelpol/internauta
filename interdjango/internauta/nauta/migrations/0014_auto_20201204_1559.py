# Generated by Django 3.1.2 on 2020-12-04 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nauta', '0013_auto_20201204_0500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='text',
            old_name='featured',
            new_name='copy',
        ),
        migrations.AddField(
            model_name='text',
            name='firstpost',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='text',
            name='categories',
            field=models.ManyToManyField(related_name='cat', to='nauta.Category'),
        ),
    ]
