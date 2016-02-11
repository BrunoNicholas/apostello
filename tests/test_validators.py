# -*- coding: utf-8 -*-
import pytest
from django.conf import settings
from django.core.exceptions import ValidationError

from apostello.validators import (
    gsm_validator, no_overlap_keyword, not_twilio_num, twilio_reserved,
    validate_lower
)


class TestLower:
    def test_ok(self):
        validate_lower('all_lower_case')

    def test_upper_chars(self):
        with pytest.raises(ValidationError):
            validate_lower('Upper case')


class TestNoTwilioNum():
    def test_ok(self):
        not_twilio_num('+447905639803')

    def test_upper_chars(self):
        with pytest.raises(ValidationError):
            not_twilio_num(settings.TWILIO_FROM_NUM)


class TestNoReserved:
    def test_ok(self):
        twilio_reserved('not_stop')

    def test_match(self):
        for x in [
            "stop", "stopall", "unsubscribe", "cancel", "end", "quit", "start",
            "yes", "help", "info", "name"
        ]:
            with pytest.raises(ValidationError):
                twilio_reserved(x)


class TestGsm:
    def test_ok(self):
        gsm_validator('This is an ok message')

    def test_upper_chars(self):
        with pytest.raises(ValidationError):
            gsm_validator('This is not an ok message…')


@pytest.mark.django_db
class TestNoOverlapKeyword:
    def test_new_ok(self, keywords):
        no_overlap_keyword('new_keyword')

    def test_new_bad(self, keywords):
        with pytest.raises(ValidationError):
            no_overlap_keyword('test_keyword')

    def test_new_bad_special(self):
        with pytest.raises(ValidationError):
            no_overlap_keyword('name')

    def test_stop(self):
        with pytest.raises(ValidationError):
            no_overlap_keyword('stop')

    def test_updating(self, keywords):
        no_overlap_keyword('test')
