# Generated by Django 5.2 on 2025-05-02 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='type',
            new_name='name',
        ),
    ]
