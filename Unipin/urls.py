"""xnote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from Unipin.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    url(r'^admin/?', admin.site.urls),
    url(r'^api/v1/', include('xnote_base.urls')),
    # url(r'^.*', TemplateView.as_view(template_name='home.html'), name="home")
]
