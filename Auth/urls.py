from django.urls import path
from  .views import register,loginUser,logout_user, get_user_data
app_name = 'Auth'
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", loginUser, name="login"),
    path("logout/", logout_user, name="logout"),
    path("get-user-data/", get_user_data, name="get-user-data")
]