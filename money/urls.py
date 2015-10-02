try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from django.contrib.sitemaps import*
from django.contrib.sitemaps.views import sitemap
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls.static import static


urlpatterns = patterns('',

    #Pay4App-only
    url(r'^P4A_payment/', 'ilsa_site.views.online_payment',
        name = 'p4a_payment'),
)