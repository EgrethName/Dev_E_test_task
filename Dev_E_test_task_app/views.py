from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def api_token_auth_create(request):
    if request.method == "POST":
        pass


@require_http_methods(["GET", "POST"])
def all_users_handler(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass


@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def user_handler(request):
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass
