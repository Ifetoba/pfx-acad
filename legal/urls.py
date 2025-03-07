from django.urls import path
from .views import privacy_policy, terms_of_service, legal, accept_cookies

app_name = 'legal'

urlpatterns = [
    path("",legal, name="legal"),
    path("privacy-policy/", privacy_policy, name="privacy-policy"),
    path("terms-of-service/", terms_of_service, name="terms-of-service"),
    path("accept-cookies/", accept_cookies, name="accept-cookies"),
]
