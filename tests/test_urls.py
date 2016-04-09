import pytest

from apostello import models
from tests.conftest import twilio_vcr


@pytest.mark.slow
@pytest.mark.parametrize(
    "url,status_code", [
        ('/', 302),
        ('/send/adhoc/', 302),
        ('/send/group/', 302),
        ('/group/all/', 302),
        ('/group/new/', 302),
        ('/group/edit/1/', 302),
        ('/group/create_all/', 302),
        ('/recipient/all/', 302),
        ('/recipient/new/', 302),
        ('/recipient/edit/1/', 302),
        ('/keyword/all/', 302),
        ('/keyword/new/', 302),
        ('/keyword/edit/1/', 302),
        ('/keyword/responses/1/', 302),
        ('/keyword/responses/archive/1/', 302),
        ('/keyword/responses/csv/1/', 302),
        ('/users/profiles/', 302),
        ('/users/profiles/1/', 302),
        ('/api/v1/users/profiles/', 403),
        ('/api/v1/users/profiles/1', 403),
        ('/api/v1/sms/in/', 403),
        ('/api/v1/sms/out/', 403),
        ('/api/v1/sms/in/recpient/1/', 403),
        ('/api/v1/sms/in/keyword/1/', 403),
        ('/api/v1/sms/in/keyword/1/archive/', 403),
        ('/api/v1/sms/in/1', 403),
        ('/api/v1/recipients/', 403),
        ('/api/v1/recipients/1', 403),
        ('/api/v1/groups/', 403),
        ('/api/v1/groups/1', 403),
        ('/api/v1/keywords/', 403),
        ('/api/v1/keywords/1', 403),
        ('/graphs/recent/', 302),
        ('/graphs/contacts/', 302),
        ('/graphs/groups/', 302),
        ('/graphs/keywords/', 302),
        ('/graphs/sms/totals/', 302),
        ('/graphs/sms/in/bycontact/', 302),
        ('/graphs/sms/out/bycontact/', 302),
        ('/config/site/', 302),
        ('/config/responses/', 302),
    ]
)
@pytest.mark.django_db
class TestNotLoggedIn:
    """Test site urls when not logged in."""

    def test_not_logged_in(
        self, url, status_code, recipients, groups, smsin, smsout, users
    ):
        assert users['c_out'].get(url).status_code == status_code


@pytest.mark.slow
@pytest.mark.parametrize(
    "url,status_code", [
        ('/', 200),
        ('/send/adhoc/', 200),
        ('/send/group/', 200),
        ('/group/all/', 200),
        ('/group/new/', 200),
        ('/group/edit/1/', 200),
        ('/group/create_all/', 200),
        ('/recipient/all/', 200),
        ('/recipient/new/', 200),
        ('/recipient/edit/1/', 200),
        ('/keyword/all/', 200),
        ('/keyword/new/', 200),
        ('/keyword/edit/1/', 200),
        ('/keyword/responses/1/', 200),
        ('/keyword/responses/archive/1/', 200),
        ('/keyword/responses/csv/1/', 200),
        ('/recipient/import/', 200),
        ('/elvanto/import/', 200),
        ('/incoming/wall/', 200),
        ('/incoming/curate_wall/', 200),
        ('/users/profiles/', 200),
        ('/users/profiles/1/', 200),
        ('/api/v1/users/profiles/', 200),
        ('/api/v1/users/profiles/1', 200),
        ('/api/v1/sms/in/', 200),
        ('/api/v1/sms/out/', 200),
        ('/api/v1/sms/in/recpient/1/', 200),
        ('/api/v1/sms/in/keyword/1/', 200),
        ('/api/v1/sms/in/keyword/1/archive/', 200),
        ('/api/v1/sms/in/1', 200),
        ('/api/v1/recipients/', 200),
        ('/api/v1/recipients/1', 200),
        ('/api/v1/groups/', 200),
        ('/api/v1/groups/1', 200),
        ('/api/v1/keywords/', 200),
        ('/api/v1/keywords/1', 200),
        ('/api/v1/sms/live_wall/all/', 200),
        ('/graphs/recent/', 200),
        ('/graphs/contacts/', 200),
        ('/graphs/groups/', 200),
        ('/graphs/keywords/', 200),
        ('/graphs/sms/totals/', 200),
        ('/graphs/sms/in/bycontact/', 200),
        ('/graphs/sms/out/bycontact/', 200),
        ('/config/site/', 200),
        ('/config/responses/', 200),
    ]
)
@pytest.mark.django_db
class TestStaff:
    """Test site urls when logged in as staff"""

    def test_staff(
        self, url, status_code, recipients, groups, smsin, smsout, keywords,
        users
    ):
        assert users['c_staff'].get(url).status_code == status_code


@pytest.mark.slow
@pytest.mark.parametrize(
    "url,status_code", [
        ('/', 200),
        ('/send/adhoc/', 302),
        ('/send/group/', 302),
        ('/group/all/', 200),
        ('/group/new/', 200),
        ('/group/edit/1/', 200),
        ('/group/create_all/', 302),
        ('/recipient/all/', 200),
        ('/recipient/new/', 200),
        ('/recipient/edit/1/', 302),
        ('/keyword/all/', 200),
        ('/keyword/new/', 200),
        ('/keyword/edit/1/', 302),
        ('/keyword/responses/1/', 302),
        ('/keyword/responses/archive/1/', 302),
        ('/keyword/responses/csv/1/', 302),
        ('/recipient/import/', 302),
        ('/elvanto/import/', 302),
        ('/incoming/wall/', 200),
        ('/incoming/curate_wall/', 200),
        ('/incoming/', 200),
        ('/users/profiles/', 302),
        ('/users/profiles/1/', 302),
        ('/api/v1/users/profiles/', 403),
        ('/api/v1/users/profiles/1', 403),
        ('/api/v1/sms/in/', 200),
        ('/api/v1/sms/out/', 200),
        ('/api/v1/sms/in/recpient/1/', 200),
        ('/api/v1/sms/in/keyword/1/', 403),
        ('/api/v1/sms/in/keyword/1/archive/', 403),
        ('/api/v1/sms/in/keyword/2/', 200),
        ('/api/v1/sms/in/keyword/2/archive/', 200),
        ('/api/v1/sms/in/1', 200),
        ('/api/v1/recipients/', 200),
        ('/api/v1/recipients/1', 200),
        ('/api/v1/groups/', 200),
        ('/api/v1/groups/1', 200),
        ('/api/v1/keywords/', 200),
        ('/api/v1/keywords/1', 200),
        ('/api/v1/sms/live_wall/all/', 200),
        ('/graphs/recent/', 200),
        ('/graphs/contacts/', 302),
        ('/graphs/groups/', 302),
        ('/graphs/keywords/', 302),
        ('/graphs/sms/totals/', 302),
        ('/graphs/sms/in/bycontact/', 302),
        ('/graphs/sms/out/bycontact/', 302),
        ('/config/site/', 302),
        ('/config/responses/', 302),
    ]
)
@pytest.mark.django_db
class TestNotStaff:
    """Test site urls when logged in a normal user"""

    def test_in(
        self, url, status_code, recipients, groups, smsin, smsout, keywords,
        users
    ):
        assert users['c_in'].get(url).status_code == status_code


@pytest.mark.slow
@pytest.mark.django_db
class TestButtonPosts:
    """Test api end points behind buttons"""

    def test_api_posts(
        self, recipients, groups, smsin, smsout, keywords, users
    ):
        for endpoint in ['sms']:
            for param in [
                'reingest', 'dealt_with', 'archived', 'display_on_wall'
            ]:
                for value in ['true', 'false']:
                    users['c_staff'].post(
                        '/api/v1/' + endpoint + '/in/1', {param: value}
                    )


@pytest.mark.slow
@pytest.mark.django_db
class TestSendingSmsForm:
    """Test the sending of SMS."""

    @twilio_vcr
    def test_send_adhoc_now(self, recipients, users):
        """Test sending a message now."""
        users['c_staff'].post(
            '/send/adhoc/', {
                'content': 'test',
                'recipients': ['1']
            }
        )

    @twilio_vcr
    def test_send_adhoc_later(self, recipients, users):
        """Test sending a message later."""
        users['c_staff'].post(
            '/send/adhoc/', {
                'content': 'test',
                'recipients': ['1'],
                'scheduled_time': '2117-12-01 00:00'
            }
        )

    def test_send_adhoc_error(self, users):
        """Test missing field."""
        resp = users['c_staff'].post('/send/adhoc/', {'content': ''})
        assert 'This field is required.' in str(resp.content)

    @twilio_vcr
    def test_send_group_now(self, groups, users):
        """Test sending a message now."""
        users['c_staff'].post(
            '/send/group/', {
                'content': 'test',
                'recipient_group': groups['test_group'].pk
            }
        )

    @twilio_vcr
    def test_send_group_later(self, groups, users):
        """Test sending a message later."""
        users['c_staff'].post(
            '/send/group/', {
                'content': 'test',
                'recipient_group': '1',
                'scheduled_time': '2117-12-01 00:00'
            }
        )

    def test_send_group_error(self, users):
        """Test missing field."""
        users['c_staff'].post('/send/group/', {'content': ''})


@pytest.mark.slow
@pytest.mark.django_db
class TestGroupForm:
    """Test group form usage"""

    def test_new_group(self, users):
        """Test creating a new group."""
        users['c_staff'].post(
            '/group/new/', {
                'name': 'test_group',
                'description': 'this is a test'
            }
        )
        test_group = models.RecipientGroup.objects.get(name='test_group')
        assert 'test_group' == str(test_group)

    def test_bring_group_from_archive(self, groups, users):
        """Test creating a group that exists in the archive."""
        users['c_staff'].post(
            '/group/new/', {
                'name': 'Archived Group',
                'description': 'this is a test'
            }
        )

    def test_edit_group(self, users):
        """Test editing a group."""
        new_group = models.RecipientGroup.objects.create(
            name='t1',
            description='t1'
        )
        new_group.save()
        pk = new_group.pk
        users['c_staff'].post(
            new_group.get_absolute_url, {
                'name': 'test_group_changed',
                'description': 'this is a test'
            }
        )
        assert 'test_group_changed' == str(
            models.RecipientGroup.objects.get(
                pk=pk
            )
        )

    def test_invalid_group_form(self, users):
        """Test submitting an invalid form."""
        resp = users['c_staff'].post(
            '/group/new/', {
                'name': '',
                'description': 'this is a test'
            }
        )
        assert 'This field is required.' in str(resp.content)

    def test_create_all_group_form(self, users, recipients):
        """Test the form to create a group composed of all recipients."""
        resp = users['c_staff'].post(
            '/group/create_all/', {
                'group_name': 'test',
            }
        )
        assert resp.status_code == 302
        assert resp.url == '/group/all/'
        assert len(models.RecipientGroup.objects.all()) == 1
        assert models.RecipientGroup.objects.all()[0].name == 'test'
        assert len(models.RecipientGroup.objects.all()[0].all_recipients) == 5

    def test_create_all_group_form_update(self, users, recipients, groups):
        """Test the form to create a group composed of all recipients.
        Test populating an already existing group.
        """
        resp = users['c_staff'].post(
            '/group/create_all/', {
                'group_name': 'Empty Group',
            }
        )
        assert resp.status_code == 302
        assert resp.url == '/group/all/'
        g = models.RecipientGroup.objects.get(name='Empty Group')
        assert len(g.all_recipients) == 5


@pytest.mark.slow
@pytest.mark.django_db
class TestOthers:
    """Test posting as a user"""

    def test_keyword_responses_404(self, keywords, users):
        assert users['c_staff'].post(
            '/keyword/responses/51234/'
        ).status_code == 404

    def test_keyword_responses_archive_all_not_ticked(self, keywords, users):
        users['c_staff'].post(
            '/keyword/responses/1/', {'tick_to_archive_all_responses': False}
        )

    def test_keyword_responses_archive_all_ticked(
        self, keywords, smsin, users
    ):
        users['c_staff'].post(
            '/keyword/responses/{}/'.format(keywords['test'].pk),
            {'tick_to_archive_all_responses': True}
        )

    def test_csv_import_blank(self, users):
        users['c_staff'].post('/recipient/import/', {'csv_data': ''})

    def test_csv_import_bad_data(self, users):
        users['c_staff'].post('/recipient/import/', {'csv_data': ',,,\n,,,'})

    def test_csv_import_good_data(self, users):
        users['c_staff'].post(
            '/recipient/import/', {
                'csv_data':
                'test,person,+447902533904,\ntest,person,+447902537994'
            }
        )

    def test_no_csv(self, users):
        assert users['c_in'].get(
            '/keyword/responses/csv/500/'
        ).status_code == 404

    def test_keyword_access_check(self, keywords, users):
        keywords['test'].owners.add(users['staff'])
        keywords['test'].save()
        assert users['c_staff'].get(
            keywords[
                'test'
            ].get_responses_url
        ).status_code == 200
        assert users['c_in'].get(
            keywords[
                'test'
            ].get_responses_url
        ).status_code == 302

    def test_check_perms_not_staff(self, users, keywords, recipients):
        assert users['c_in'].get('/incoming/').status_code == 200
        assert users['c_in'].get('/elvanto/import/').status_code == 302
        assert users['c_in'].get(
            recipients[
                'calvin'
            ].get_absolute_url
        ).status_code == 302
