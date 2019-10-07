"""itcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import handler404, handler500, url

from django.conf import settings
from django.conf.urls.static import static

from itcs.views import index_page

from django.views.generic import RedirectView

#for overriding django auth view
#from django.contrib.auth import views as auth_views
#from mariner.forms import LoginForm
from api.urls import router

handler404 = 'itcs.views.page_not_found'
handler500 = 'itcs.views.server_error'

urlpatterns = [
    path('', index_page, name='index_page'),
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    path('mariner/api/', include('api.urls')),
    url(r'^mariner/api/', include(router.urls)),
    path('mariner/', include('mariner.urls')),
    #override django login/loguot view with CRM template
    path('mariner/', include('django.contrib.auth.urls')),
    #path('mariner/login/', auth_views.LoginView.as_view(template_name="crm_login.html"), name="crm_login"),
    #path('mariner/logout/', auth_views.LogoutView, {'next_page': 'mariner/login/'}),

    path('regulations/', include('regulations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
