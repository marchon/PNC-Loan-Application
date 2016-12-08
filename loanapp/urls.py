from django.conf.urls import url
from . import views
from loanapp.views import LoanCreate, LoanUpdate


urlpatterns = [
	url(r'^$', views.index),
	url(r'^main/', views.index, name='index'),
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^dash/', views.dashboard, name='dashboard'),
    url(r'^profile/', views.make_profile, name='make_profile'),
    # url(r'^loanterms/(?P<loan_id>[0-9]+)/$', views.update_loan, name='update_loan'),
    url(r'^loanterms/', views.make_loan, name='make_loan'),
    url(r'^revisitloan/', views.revisit_loan, name='revisit_loan'),
    # url(r'loan/add/$', LoanCreate.as_view(), name='loan-add'),
    # url(r'loan/(?P<pk>[0-9]+)/$', LoanUpdate.as_view(), name='loan-update'),
    url(r'^users/', views.users),
    # url(r'^email/$',views.email, name='email')
]