from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from models import Event
from views import EventDetailView, \
            EventCreateView, \
            EventUpdateView, \
            EventDeleteView, \
            SegmentUpdateView, \
            SegmentCreateView, \
            SegmentDeleteView, \
            SongSegmentCreateView, \
            ActivityCreateView, \
            ActivityDeleteView, \
            RoleCreateView,  \
            ParticipantCreateView, \
            MassCreateView, \
            JSONSegmentUpdateView
from newproject.Event_Planner.views import JSONSegmentDeleteView,\
    SongSegmentUpdateView, EventListView, TemplateCreateView, OrderUpdateView,\
    AjaxActivityCreateView, JSONRoleListView, JSONParticipantListView,\
    JSONActivityDeleteView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('Event_Planner.views',
    url(r'^$', EventListView.as_view(), name='event_list_view'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail_view'),
    url(r'^create/$', EventCreateView.as_view(), name='event_create_view'),
    url(r'^create/template/$', TemplateCreateView.as_view(), name='template_event_create_view'),
    url(r'^create/mass/$', MassCreateView.as_view(), name='mass_create_view'),
    url(r'^(?P<pk>\d+)/update/$', EventUpdateView.as_view(model=Event), name='event_update_view'),
    url(r'^(?P<pk>\d+)/update/order/$', OrderUpdateView.as_view(model=Event), name='event_order_update_view'),
    url(r'^(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='event_delete_view'),
    url(r'^(?P<event_id>\d+)/segment/create/$', SegmentCreateView.as_view(), name='segment_create_view'),
    url(r'^(?P<event_id>\d+)/songsegment/create/$', SongSegmentCreateView.as_view(), name='songsegment_create_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/update/$', SegmentUpdateView.as_view(), name='segment_update_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/update/ajax/$', JSONSegmentUpdateView.as_view(), name='json_segment_update_view'),
    url(r'^(?P<event_id>\d+)/songsegment/(?P<pk>\d+)/update/$', SongSegmentUpdateView.as_view(), name='songsegment_update_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/delete/$', SegmentDeleteView.as_view(), name='segment_delete_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/delete/ajax$', JSONSegmentDeleteView.as_view(), name='json_segment_delete_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/activity/create/$', ActivityCreateView.as_view(), name='activity_create_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<pk>\d+)/activity/create/ajax/$', AjaxActivityCreateView.as_view(), name='json_activity_create_view'),
    url(r'^(?P<event_id>\d+)/segment/(?P<segment_id>\d+)/activity/(?P<pk>\d+)/delete/$', ActivityDeleteView.as_view(), name='activity_delete_view'),
    url(r'^activity/(?P<pk>\d+)/delete/ajax$', JSONActivityDeleteView.as_view(), name='json_activity_delete_view'),
    url(r'^role/create/$', RoleCreateView.as_view(), name='role_create_view'),
    url(r'^participant/create/$', ParticipantCreateView.as_view(), name='participant_create_view'),
    url(r'^role/list/$', JSONRoleListView, name='json_role_list_view'),
    url(r'^participant/list/$', JSONParticipantListView, name='json_participant_list_view'),
    
    # Examples:
    # url(r'^$', 'lit_planner.views.home', name='home'),
    # url(r'^lit_planner/', include('lit_planner.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
