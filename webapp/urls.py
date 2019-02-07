from django.urls import include, path
from .views import Login,Logout

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('log', Login.as_view()),
    path('logg', Logout.as_view())
]
