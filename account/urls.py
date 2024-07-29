from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    path('',index, name='index'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    # path('logina/', RegisterLogin.as_view(), name='logina'),
    path('register/',RegisterView.as_view(), name='register'),
    path('employeeinfo/',EmployeeinfoView.as_view(), name='employeeinfo'),
    path('relationship/',RelationshipView.as_view(), name='relationship'),
    path('profile/',ProfileListView.as_view(),name='profile'),
    path('profile/update/<int:id>/',ProfileUpdateView.as_view(),name='profile_update'),
    path('profile/delete/<int:id>/',ProfileDeleteView.as_view(),name='profile_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('packages/', PaymentOptionsView.as_view(), name='packages'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
