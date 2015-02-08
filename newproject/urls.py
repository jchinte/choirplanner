from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import UserCreateView, AdminUserUpdateView, UserDetailView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newproject.views.home', name='home'),
    # url(r'^newproject/', include('newproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^songs/', include('SongManager.urls')),
    url(r'^events/', include('Event_Planner.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login_view'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/create/$', UserCreateView.as_view()),
    (r'^accounts/perms/(?P<slug>\w+)/$', AdminUserUpdateView.as_view()),
    (r'^users/(?P<slug>\w+)/$', UserDetailView.as_view()),
    
    #(r'^songs/$', 'SongManager.views.index'),
    #(r'^songs/(?P<song_id>\d+)/$', 'SongManager.views.detail'),
    #url(r'^songs/(?P<song_id>\d+)/modify/$', 'SongManager.views.modify', name = 'modify_song'),
    #(r'^songs/search/$', 'SongManager.views.search'),
    #url(r'^songs/add/$', 'SongManager.views.add', name = 'add_new_song'),
)
