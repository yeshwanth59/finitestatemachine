from django.shortcuts import render, HttpResponse, redirect
from statemachine import models


def cantLoginAfterLogin(get_response):
    def middleware(request):
        user = request.session.get("user")
        if user:
            print("ur already logged-in")
            return redirect('/')
        else:
            print("please Login")
            return get_response(request)

    return middleware