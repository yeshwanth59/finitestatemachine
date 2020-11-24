from django.shortcuts import render, redirect
from django.http import HttpResponse
from statemachine.models import User, Workflow
from statemachine.forms import SignupForm, LoginForm

# Create your views here.


def home(request):
    workflow = Workflow.objects.all()
    return render(request, "home.html", {"workflow": workflow})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES or None)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            un = MyLoginForm.cleaned_data["email"]
            pw = MyLoginForm.cleaned_data["pwd"]
            print(un)
            print(pw)
            dbuser = User.objects.filter(email=un, pwd=pw)

            if not dbuser:
                return HttpResponse("Login Failed")
            else:
                return redirect("/")
        else:
            form = LoginForm()
        return render(request, "login.html", {"form": form})

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect("/")


def workflowStart(request, workflow_id):
    return render(request, "questions.html")

