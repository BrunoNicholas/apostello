from django.conf.urls import url
from rest_framework.permissions import IsAuthenticated

from api.drf_permissions import (CanSeeContactNames, CanSeeGroups,
                                 CanSeeIncoming, CanSeeKeyword, CanSeeKeywords,
                                 CanSeeOutgoing)
from api.serializers import (KeywordSerializer, RecipientGroupSerializer,
                             RecipientSerializer, SmsInboundSerializer,
                             SmsOutboundSerializer)
from api.views import (ApiCollection, ApiCollectionAllWall,
                       ApiCollectionKeywordSms, ApiCollectionKeywordWall,
                       ApiCollectionRecentSms, ApiMember)
from apostello.models import (Keyword, Recipient, RecipientGroup, SmsInbound,
                              SmsOutbound)

# api
urlpatterns = [
    # sms views
    url(r'^v1/sms/in/$',
        ApiCollection.as_view(
            model_class=SmsInbound,
            serializer_class=SmsInboundSerializer,
            permission_classes=(IsAuthenticated, CanSeeIncoming)
        ),
        name='in_log'),
    url(r'^v1/sms/out/$',
        ApiCollection.as_view(
            model_class=SmsOutbound,
            serializer_class=SmsOutboundSerializer,
            permission_classes=(IsAuthenticated, CanSeeOutgoing),
        ),
        name='out_log'),
    url(r'^v1/sms/live_wall/in/$',
        ApiCollectionAllWall.as_view(
            permission_classes=(IsAuthenticated, CanSeeIncoming)
        ),
        name='all_live_wall'),
    url(r'^v1/sms/live_wall/only_live/in/$',
        ApiCollectionAllWall.as_view(
            permission_classes=(IsAuthenticated, CanSeeIncoming),
            only_live=True
        ),
        name='all_live_wall_only_live'),
    url(r'^v1/sms/in/recpient/(?P<pk>\d+)/$',
        ApiCollectionRecentSms.as_view(
            permission_classes=(IsAuthenticated, CanSeeContactNames, CanSeeIncoming)),
        name='contact_recent_sms'),
    url(r'^v1/sms/in/keyword/(?P<pk>\d+)/$',
        ApiCollectionKeywordSms.as_view(
            permission_classes=(IsAuthenticated, CanSeeKeywords, CanSeeKeyword, CanSeeIncoming),
            archive=False
        ),
        name='keyword_sms'),
    url(r'^v1/sms/live_wall/in/keyword/(?P<pk>\d+)/$',
        ApiCollectionKeywordWall.as_view(
            permission_classes=(IsAuthenticated, CanSeeKeywords, CanSeeKeyword, CanSeeIncoming),
        ),
        name='keyword_live_wall'),
    url(r'^v1/sms/live_wall/only_live/in/keyword/(?P<pk>\d+)/$',
        ApiCollectionKeywordWall.as_view(
            permission_classes=(IsAuthenticated, CanSeeKeywords, CanSeeKeyword, CanSeeIncoming),
            only_live=True,
        ),
        name='keyword_live_wall_only_live'),
    url(r'^v1/sms/in/keyword/(?P<pk>\d+)/archive/$',
        ApiCollectionKeywordSms.as_view(
            permission_classes=(IsAuthenticated, CanSeeKeywords, CanSeeKeyword, CanSeeIncoming),
            archive=True),
        name='keyword_sms_archive'),
    url(r'^v1/sms/in/(?P<pk>[0-9]+)$',
        ApiMember.as_view(
            model_class=SmsInbound,
            serializer_class=SmsInboundSerializer,
            permission_classes=(IsAuthenticated, CanSeeIncoming),
        ),
        name='sms_in_member'),
    # recipient views
    url(r'^v1/recipients/$',
        ApiCollection.as_view(
            model_class=Recipient,
            serializer_class=RecipientSerializer,
            filter_list=True,
            filters={'is_archived': False},
            permission_classes=(IsAuthenticated, CanSeeContactNames)
        ),
        name='recipients'),
    url(r'^v1/recipients/(?P<pk>[0-9]+)$',
        ApiMember.as_view(
            model_class=Recipient,
            serializer_class=RecipientSerializer,
            permission_classes=(IsAuthenticated, CanSeeContactNames)
        ),
        name='recipient'),
    # group views
    url(r'^v1/groups/$',
        ApiCollection.as_view(
            model_class=RecipientGroup,
            serializer_class=RecipientGroupSerializer,
            filter_list=True,
            filters={'is_archived': False},
            permission_classes=(IsAuthenticated, CanSeeGroups)
        ),
        name='recipient_groups'),
    url(r'^v1/groups/(?P<pk>[0-9]+)$',
        ApiMember.as_view(
            model_class=RecipientGroup,
            serializer_class=RecipientGroupSerializer,
            permission_classes=(IsAuthenticated, CanSeeGroups)
        ),
        name='group'),
    # keyword views
    url(r'^v1/keywords/$',
        ApiCollection.as_view(
            model_class=Keyword,
            serializer_class=KeywordSerializer,
            filter_list=True,
            filters={'is_archived': False},
            permission_classes=(IsAuthenticated, CanSeeKeywords)
        ),
        name='keywords'),
    url(r'^v1/keywords/(?P<pk>[0-9]+)$',
        ApiMember.as_view(
            model_class=Keyword,
            serializer_class=KeywordSerializer,
            permission_classes=(IsAuthenticated, CanSeeKeyword)
        ),
        name='keyword'),
]
