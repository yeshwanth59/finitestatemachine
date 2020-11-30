from django.shortcuts import render, HttpResponse, redirect
from os import path


def login_required(get_response):

    def middleware(request, workflow_id=None):

        print("Middleware...///")
        user = request.session.get("user")
        if user:
            response = None
            if workflow_id:
                response = get_response(request, workflow_id)
            else:
                response = get_response(request)
            return response
            print(response)
        else:
            print("please Login")
            url = request.path
            print(url)
            #return redirect('/login/')
            return redirect(f'/login?return_url={url}')

    return middleware