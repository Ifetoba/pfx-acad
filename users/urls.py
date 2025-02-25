from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.register, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("profile/", views.profile, name="profile")
    # path("admin/dashboard", views.admin_dashboard, name="admin-dashboard"),
    # path("instructor/dashboard", views.instructor_dashboard, name="instructor-dashboard")
]
