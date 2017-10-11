"""TCCgo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', include('TCCgo.apps.core.urls', namespace='core')), # Main application
    url(r'^auth/', include('TCCgo.apps.authentication.urls', namespace='authentication')), # Authentication application
    url(r'^rules/', include('TCCgo.apps.rules.urls', namespace='rules')), # Rules management
    url(r'^faqs/', include('TCCgo.apps.faq.urls', namespace='faqs')),
    url(r'^forum/', include('TCCgo.apps.forum.urls', namespace='forum')),
    url(r'^text/', include('TCCgo.apps.text.urls', namespace='text')),
]
