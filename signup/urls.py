from django.conf.urls import url
from signup import views

urlpatterns = [
    url(r'^$', views.signup),
    url(r'^city_api/$', views.city_api),
    url(r'^get_city_detail/$', views.get_city_detail),
    url(r'^user_selected_data/$', views.user_selected_data),
]
