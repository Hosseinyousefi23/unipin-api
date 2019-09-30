from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from api.views import PostViewSet, Offers, TagViewSet
from . import views

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='post')
router.register(r'tag', TagViewSet, base_name='tag')

urlpatterns = [
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/', include('rest_auth.urls')),
]
urlpatterns += router.urls
urlpatterns += [
    url(r'api-token-auth/', obtain_jwt_token),
    url(r'api-token-refresh/', refresh_jwt_token),
    url(r'offers', Offers.as_view(), name='offers'),
    url(r'^$', views.main_page, name='main_page'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^profile$', views.my_profile, name='profile'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^forgot_password$', views.forgot_password, name='forgot'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^check_username$', views.check_username, name='check_username'),
    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^single_post$', views.single_post, name='single_post'),
    url(r'^(?P<name>\w+)$', views.view_page, name='view_page'),

]
