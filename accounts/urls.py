from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signUp/$', views.sign_up_view, name="signUp"),
    url(r'^logIn/$', views.log_in_view, name="logIn"),
    url(r'^logOut/$', views.log_out_view, name="logOut"),
    url(r'^myAccount/$', views.my_account_view, name="myAccount"),
    url(r'^myContribution/$', views.my_contribution_view,
        name="myContribution"),
]