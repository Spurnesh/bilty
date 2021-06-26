from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from bilty import views

urlpatterns = [
    path("login/", views.LoginAuth.as_view(), name="login"),
    path("add-bilty/", views.BiltyView.as_view(), name="add-bilty"),
    path("add-user/", views.UserView.as_view(), name="add-user"),
    path("get-user/", views.GetUserView.as_view(), name="get-user"),
]