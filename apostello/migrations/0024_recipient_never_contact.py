# Generated by Django 2.0.3 on 2018-07-16 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apostello', '0023_smsoutbound_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='never_contact',
            field=models.BooleanField(default=False, help_text='Tick this box to prevent any messages being sent to this person.', verbose_name='Never Contact'),
        ),
    ]
