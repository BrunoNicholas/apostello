# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 09:53
from __future__ import unicode_literals

import os

from django.db import migrations


def add_twilio(apps, schema_editor):
    config, _ = apps.get_model('site_config', 'SiteConfiguration').objects.get_or_create()
    config.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    config.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    config.twilio_from_num = os.environ.get('TWILIO_FROM_NUM')
    try:
        cost = float(os.environ.get('TWILIO_SENDING_COST'))
    except TypeError:
        cost = None
    config.twilio_sending_cost = cost
    config.save()


def add_email(apps, schema_editor):
    config, _ = apps.get_model('site_config', 'SiteConfiguration').objects.get_or_create()
    config.email_host = os.environ.get('DJANGO_EMAIL_HOST')
    config.email_host_user = os.environ.get('DJANGO_EMAIL_HOST_USER')
    config.email_host_password = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
    config.email_from = os.environ.get('DJANGO_FROM_EMAIL')
    try:
        port = int(os.environ.get('DJANGO_EMAIL_HOST_PORT', 587))
    except TypeError:
        port = None
    config.email_port = port
    config.save()

class Migration(migrations.Migration):

    dependencies = [
        ('site_config', '0013_auto_20171025_1053'),
    ]

    operations = [
        migrations.RunPython(add_twilio),
        migrations.RunPython(add_email),
    ]
