# Generated by Django 3.2.7 on 2021-12-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_link',
            field=models.URLField(blank=True, null=True, verbose_name='Github'),
        ),
    ]
