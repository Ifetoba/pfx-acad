import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course, CourseEnrollment
from users.models import CustomUser

api_key = stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.
@csrf_exempt
def create_checkout_session(request, course_id):
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    course = Course.objects.get(id=course_id)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': 'Course Enrollment',
                        },
                        'unit_amount': int(course.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={'course_id': course.id} ,# Pass Course id
            success_url= YOUR_DOMAIN + f"/payments/success/{course.id}", # Redirects to success page
            cancel_url= YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

def payment_success(request, course_id):
    if not request.user.is_authenticated:
        return redirect("users:signin") # Ensure user is logged in
    
    course = get_object_or_404(Course, id=course_id)

    # Enroll user in the course
    CourseEnrollment.objects.get_or_create(user=request.user, course = course)

    return render(request, "payments/success.html", {"course": course})


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         return JsonResponse({'status': 'error'}, status=400)
#     except stripe.error.SignatureVerificationError as e:
#         return JsonResponse({'status': 'error'}, status=400)
    
#     # Handle the event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object'] # Contains a stripe checkout session object
#         # Handle post-payment actions (e.g, marking order as paid)

#     return JsonResponse({'status': 'success'})