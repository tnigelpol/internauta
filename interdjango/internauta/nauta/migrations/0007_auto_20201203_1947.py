# Generated by Django 3.1.2 on 2020-12-03 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nauta', '0006_auto_20201009_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='text',
            name='next_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='nauta.text'),
        ),
        migrations.AddField(
            model_name='text',
            name='previous_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='nauta.text'),
        ),
        migrations.AddField(
            model_name='text',
            name='cat',
            field=models.ManyToManyField(to='nauta.Category'),
        ),
    ]
