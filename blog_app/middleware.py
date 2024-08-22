from django.shortcuts import redirect
from django.urls import reverse

class EnsureProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('user_login')
        response = self.get_response(request)
        return response