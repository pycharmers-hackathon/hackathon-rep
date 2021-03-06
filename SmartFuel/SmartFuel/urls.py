from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from SmartFuel.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SmartFuel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^smartfuel/$', index),
    url(r'^nearest/', nearest_fuel_stations),
    url(r'^optimal/', aco_controller),
)
