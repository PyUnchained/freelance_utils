try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from django.contrib.sitemaps import*
from django.contrib.sitemaps.views import sitemap
from django.core.urlresolvers import reverse
from django.conf.urls.static import static

class ViewSitemap(Sitemap):
    """Reverses all static views defined in the urlpatterns"""

    def items(self):
        # Return list of url names for views to include in sitemap
        item_list = []
        for item in urlpatterns:
            #Identifies all of the names of the views in urlpatterns
            #and removes the entry for the sitempas view itself
            if 'django.contrib.sitemaps' not in item.name:
                item_list.append(item.name)

        return item_list

    def location(self, item):
        return reverse(item)