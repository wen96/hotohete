from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('web.urls'))
]
