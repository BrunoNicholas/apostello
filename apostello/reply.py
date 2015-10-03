# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ValidationError

from apostello.models import Recipient
from apostello.tasks import (check_recent_outgoing_log, notify_office_mail,
                             update_msgs_name, warn_on_blacklist,
                             warn_on_blacklist_receipt)
from apostello.utils import fetch_default_reply


def keyword_replier(k, person_from):
    try:
        reply = k.construct_reply(person_from)
    except AttributeError:
        reply = fetch_default_reply('keyword_no_match')
        reply = person_from.personalise(reply)

    return reply


def get_person_or_ask_for_name(from_, sms_body, keyword_obj):
    try:
        person_from = Recipient.objects.get(number=from_)
    except Recipient.DoesNotExist:
        person_from = Recipient.objects.create(number=from_,
                                               first_name='Unknown',
                                               last_name='Person')
        person_from.save()
        if keyword_obj == "name":
            pass
        else:
            from apostello.models import SiteConfiguration
            config = SiteConfiguration.get_solo()
            if not config.disable_all_replies:
                person_from.send_message(content=fetch_default_reply('auto_name_request'),
                                         sent_by="auto name request")
                notify_office_mail.delay(
                    '[Apostello] Unknown Contact!',
                    'SMS:%s\nFrom:%s\n\n\nThis person is unknown and has been asked for their name.' % (sms_body, from_),
                )

    return person_from


def reply_to_incoming(person_from, from_, sms_body, keyword):
    # update outgoing log 1 minute from now:
    if not settings.TESTING:
        check_recent_outgoing_log.apply_async(args=[0], countdown=60)

    if keyword == "start":
        person_from.is_blocking = False
        person_from.save()
        return fetch_default_reply('start_reply')
    elif keyword == "stop":
        person_from.is_blocking = True
        person_from.save()
        warn_on_blacklist.delay(person_from.id)
        return ''
    elif keyword == "name":
        warn_on_blacklist_receipt.delay(person_from.id, sms_body)
        try:
            # update person's name:
            person_from.first_name = sms_body.split()[1].strip()
            person_from.last_name = " ".join(sms_body.split()[2:]).strip()
            if len(person_from.last_name) < 1:
                raise ValidationError('No last name')
            person_from.save()
            # update old messages with this person's name
            update_msgs_name.delay(person_from.id)
            # thank person
            notify_office_mail.delay(
                '[Apostello] New Signup!',
                'SMS:\n\t%s\nFrom:\n\t%s\n' % (sms_body, from_),
            )
            return fetch_default_reply('name_update_reply') % person_from.first_name
        except (ValidationError, IndexError):
            notify_office_mail.delay(
                '[Apostello] New Signup - FAILED!',
                'SMS:\n\t%s\nFrom:\n\t%s\n' % (sms_body, from_),
            )
            return fetch_default_reply('name_failure_reply')
    else:
        # otherwise construct reply
        warn_on_blacklist_receipt.delay(person_from.id, sms_body)
        return keyword_replier(keyword, person_from)
