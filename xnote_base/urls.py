from django.conf.urls import url
from . import views

app_name = 'xnote_base'
urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^profile$', views.my_profile, name='profile'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^followers$', views.followers_page, name='followers_page'),
    url(r'^following$', views.following_page, name='following_page'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^check_username$', views.check_username, name='check_username'),
    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^follow$', views.follow, name='follow'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),
    url(r'^new_group$', views.new_group , name='new_group'),
    url(r'^new_group_action$', views.new_group_action, name='new_group_action'),
    url(r'^single_post$', views.single_post, name='single_post'),
    url(r'^(?P<name>\w+)$', views.view_page, name='view_page'),

]
