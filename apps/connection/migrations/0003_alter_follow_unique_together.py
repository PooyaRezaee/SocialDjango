# Generated by Django 4.1.7 on 2023-04-05 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0002_alter_follow_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]