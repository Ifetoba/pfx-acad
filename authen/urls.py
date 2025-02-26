from django.urls import path
from . import views

app_name = "authen"

urlpatterns = [
    path("verify-email/<uuid:token>/", views.verify_email, name="verify-email"),
    path("password-reset/", views.PasswordResetView.as_view(template_name='authen/password_reset.html'), name="password-reset"),
    path("password-reset/done/", views.PasswordResetDoneView.as_view(template_name='authen/password_reset_done.html'), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(template_name='authen/password_reset_confirm.html'), name="password-reset-confirm"),
    path("password-reset-complete/", views.PasswordResetCompleteView.as_view(template_name='authen/password_reset_complete.html'), name="password-reset-complete"),
    path("password-change/", views.PasswordChangeView.as_view(template_name='authen/password_change.html'), name="password-change"),
    path("password-change/done/", views.PasswordChangeDoneView.as_view(template_name='authen/password_change_done.html'), name="password-change-done"),
]
