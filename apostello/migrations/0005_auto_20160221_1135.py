# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 11:35
from __future__ import unicode_literals

import apostello.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apostello', '0004_auto_20160210_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='too_early_response',
            field=models.CharField(blank=True, help_text="Use this if you want a custom response before. e.g. 'You are too early for this event, please try again on Monday!'", max_length=1000, validators=[django.core.validators.RegexValidator('^[\\s\\w@?£!1$"¥#è?¤é%ù&ì\\ò(Ç)*:Ø+;ÄäøÆ,<LÖlöæ\\-=ÑñÅß.>ÜüåÉ/§à¡¿\']+$', message='You can only use GSM characters.'), apostello.validators.less_than_sms_char_limit], verbose_name='Not yet activated response'),
        ),
    ]
