# -*- coding: utf-8 -*-
import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import View
from django_twilio.decorators import twilio_view
from phonenumber_field.validators import validate_international_phonenumber
from twilio import twiml

from apostello.decorators import check_user_perms, keyword_access_check
from apostello.forms import (ArchiveKeywordResponses, CsvImport, ElvantoImport,
                             SendAdhocRecipientsForm, SendRecipientGroupForm)
from apostello.mixins import LoginRequiredMixin, ProfilePermsMixin
from apostello.models import (Keyword, Recipient, RecipientGroup,
                              SiteConfiguration)
from apostello.reply import get_person_or_ask_for_name, reply_to_incoming
from apostello.tasks import import_elvanto_groups, log_msg_in, post_to_slack
from apostello.utils import exists_and_archived


class SimpleView(LoginRequiredMixin, ProfilePermsMixin, View):
    template_name = ''
    required_perms = []

    def get(self, request, *args, **kwargs):
        context = dict()
        if "recipients" in self.template_name:
            context['archived_contacts'] = Recipient.objects.filter(is_archived=True).count()
            context['blacklisted_contacts'] = Recipient.objects.filter(is_blocking=True).count()
            context['total_contacts'] = Recipient.objects.count() - context['archived_contacts'] - context['blacklisted_contacts']
        return render(request, self.template_name, context)


class SendAdhoc(LoginRequiredMixin, ProfilePermsMixin, View):
    required_perms = []

    def get(self, request, *args, **kwargs):
        return render(request, "apostello/send_adhoc.html", {'form': SendAdhocRecipientsForm})

    def post(self, request, *args, **kwargs):
        form = SendAdhocRecipientsForm(request.POST, ('recipients',))
        if form.is_valid():
            for recipient in form.cleaned_data['recipients']:
                # send and save message
                recipient.send_message(content=form.cleaned_data['content'],
                                       eta=form.cleaned_data['scheduled_time'],
                                       sent_by=str(request.user))

            if form.cleaned_data['scheduled_time'] is None:
                messages.info(request, "Sending \"%s\"...\nPlease check the logs for verification..." % (form.cleaned_data['content']))
            else:
                messages.info(request, "'%s' has been successfully queued." % form.cleaned_data['content'])
            return redirect(reverse("send_adhoc"))
        else:
            return render(request, "apostello/send_adhoc.html", {'form': form})


class SendGroup(LoginRequiredMixin, ProfilePermsMixin, View):
    required_perms = []

    def get(self, request, *args, **kwargs):
        context = {
            'form': SendRecipientGroupForm,
            'group_nums': [(x.id, x.calculate_cost) for x in RecipientGroup.objects.all()]}
        return render(request, "apostello/send_group.html", context)

    def post(self, request, *args, **kwargs):
        context = {'group_nums': [(x.id, x.calculate_cost) for x in RecipientGroup.objects.all()]}
        form = SendRecipientGroupForm(request.POST)
        if form.is_valid():
            form.cleaned_data['recipient_group'].send_message(
                content=form.cleaned_data['content'],
                eta=form.cleaned_data['scheduled_time'],
                sent_by=str(request.user)
            )
            if form.cleaned_data['scheduled_time'] is None:
                messages.info(request, "Sending '%s' to '%s'...\nPlease check the logs for verification..." % (form.cleaned_data['content'], form.cleaned_data['recipient_group']))
            else:
                messages.info(request, "'%s' has been successfully queued." % form.cleaned_data['content'])
            return redirect(reverse('send_group'))
        else:
            context['form'] = form
            return render(request, "apostello/send_group.html", context)


class ItemView(LoginRequiredMixin, ProfilePermsMixin, View):
    form_class = None
    redirect_url = ''
    identifier = ''
    model_class = None
    required_perms = []

    def get(self, request, *args, **kwargs):
        context = dict()
        context['identifier'] = self.identifier
        try:
            # if editing, form needs to be populated
            pk = kwargs['pk']
            instance = get_object_or_404(self.model_class, pk=pk)
            context['object'] = instance
            form = self.form_class(instance=instance)
            context['submit_text'] = "Update"
            if self.identifier == "keyword":
                context['keyword'] = Keyword.objects.get(pk=pk)
            if self.identifier == 'recipient':
                context['sms_history'] = True
        except KeyError:
            # otherwise, use a blank form
            form = self.form_class
            context['submit_text'] = "Submit"

        context['form'] = form

        return render(request, "apostello/item.html", context)

    def post(self, request, *args, **kwargs):
        try:
            instance = self.model_class.objects.get(pk=kwargs['pk'])  # original instance
            form = self.form_class(request.POST, instance=instance)
        except KeyError:
            form = self.form_class(request.POST)

        if form.is_valid():
            # if form is valid, save, otherwise handle different type of errors
            form.save()
            return redirect(self.redirect_url)
        else:
            new_instance = exists_and_archived(form, self.model_class, self.identifier)
            if new_instance is not None:
                # if we have a clash with existing object and it is archived,
                # redirect there, otherwise return form with errors
                messages.info(request, "'%s' already exists. Click the button to bring it back from the archive." % str(new_instance))
                return redirect(new_instance.get_absolute_url())
            else:
                return render(request, "apostello/item.html",
                              dict(form=form,
                                   redirect_url=self.redirect_url,
                                   submit_text="Submit",
                                   identifier=self.identifier,
                                   object=new_instance)
                              )


@keyword_access_check
@login_required
def keyword_responses(request, pk, archive=False):
    keyword = get_object_or_404(Keyword, pk=pk)

    if archive is False and request.method == 'POST':
        form = ArchiveKeywordResponses(request.POST)
        if form.is_valid() and form.cleaned_data['tick_to_archive_all_responses']:
            for sms in keyword.fetch_matches():
                sms.is_archived = True
                sms.save()
            return redirect(reverse("keyword_responses", kwargs={'pk': pk}))

    context = {"keyword": keyword, "archive": archive}
    if archive is False:
        context["form"] = ArchiveKeywordResponses

    return render(request, "apostello/keyword_responses.html", context)


@keyword_access_check
@login_required
def keyword_csv(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + keyword.keyword + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['From', 'Time', 'Keyword', 'Message'])

    # write response rows
    for sms_ in keyword.fetch_matches():
        writer.writerow([sms_.sender_name.encode('utf8'), sms_.time_received, sms_.matched_keyword.encode('utf8'), sms_.content.encode('utf8')])

    return response


@keyword_access_check
@login_required
def keyword_wall(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    return render(request, "apostello/wall.html", {'keyword': keyword})


@login_required
def wall(request):
    return render(request, "apostello/wall.html", {})


@keyword_access_check
@login_required
def keyword_wall_curate(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    return render(request, "apostello/wall_curator.html", {'keyword': keyword})


@login_required
def wall_curate(request):
    return render(request, "apostello/wall_curator.html", {})


@login_required
@check_user_perms
def import_recipients(request):
    if request.method == 'POST':
        form = CsvImport(request.POST)
        if form.is_valid():
            csv_string = u"first_name,last_name,number\n" + form.cleaned_data['csv_data']
            data = [x for x in csv.DictReader(io.StringIO(csv_string))]
            bad_rows = list()
            for row in data:
                try:
                    validate_international_phonenumber(row['number'])
                    obj = Recipient.objects.get_or_create(number=row['number'])[0]
                    obj.first_name = row['first_name'].strip()
                    obj.last_name = row['last_name'].strip()
                    obj.is_archived = False
                    obj.full_clean()
                    obj.save()
                except Exception:
                    # catch bad rows and display to the user
                    bad_rows.append(row)
            if len(bad_rows) == 0:
                messages.success(request, "Importing your data now...")
                return redirect('/')
            else:
                messages.warning(request, "Uh oh, something went wrong with these imports!")
                return render(request, "apostello/importer.html", {'form': CsvImport(), 'bad_rows': bad_rows})

        context = {'form': form}
        return render(request, 'apostello/importer.html', context)

    else:
        context = {'form': CsvImport()}
        return render(request, 'apostello/importer.html', context)


class ElvantoImportView(LoginRequiredMixin, ProfilePermsMixin, View):
    required_perms = []

    def get(self, request, *args, **kwargs):
        context = {'form': ElvantoImport()}
        return render(request, "apostello/elvanto.html", context)

    def post(self, request, *args, **kwargs):
        form = ElvantoImport(request.POST)
        if form.is_valid():
            group_ids = form.cleaned_data['elvanto_groups']
            # start async task:
            import_elvanto_groups.delay(group_ids, request.user.email)
            messages.success(request, "Your groups are being updated, you should get an email confirmation when they are done.")
            return redirect("/")

        context = {'form': form}
        return render(request, "apostello/elvanto.html", context)


@twilio_view
def sms(request):
    r = twiml.Response()
    params = request.POST
    from_ = params['From']
    sms_body = params['Body'].strip()
    keyword_obj = Keyword.match(sms_body)
    # get person object and optionally ask for their name
    person_from = get_person_or_ask_for_name(from_, sms_body, keyword_obj)
    log_msg_in.delay(params, timezone.now(), person_from.pk)
    post_to_slack.delay("%s\nFrom: %s\n(matched: %s)" % (sms_body, str(person_from), str(keyword_obj)))

    reply = reply_to_incoming(person_from, from_, sms_body, keyword_obj)

    config = SiteConfiguration.get_solo()
    if not config.disable_all_replies:
        r.message(reply)

    return r
