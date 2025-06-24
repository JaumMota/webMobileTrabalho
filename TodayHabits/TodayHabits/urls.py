from django.contrib import admin
from django.urls import path, include
from TodayHabits.views import Login, Logout
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
        path('', Login.as_view(), name='login'),
        path('logout/', Logout.as_view(), name='logout'),
        path('habito/', include('habito.urls')), 
        path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
