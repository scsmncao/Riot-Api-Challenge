from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'riotApiChallenge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apItems.views.index', name='index'),
    url(r'^item/(?P<id>[0-9]+)$', 'apItems.views.item', name='item'),
]
