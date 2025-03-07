from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import LegalDocument

# Create your views here.
def legal(request):
    return render(request, "legal/legal.html")

def privacy_policy(request):
    policy = get_object_or_404(LegalDocument, title="Privacy Policy")
    return render(request, "legal/privacy_policy.html", {"policy": policy})

def terms_of_service(request):
    terms = get_object_or_404(LegalDocument, title="Terms of Service")
    return render(request, "legal/terms_of_service.html", {"terms": terms})

def accept_cookies(request):
    response = HttpResponse("Cookies accepted!")
    response.set_cookie("cookies_accepted", "true", max_age=60*60*24*365) # Cookies lasts for 1 year
    return redirect("/")