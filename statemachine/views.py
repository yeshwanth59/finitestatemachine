from django.shortcuts import render, redirect
from django.http import HttpResponse
from statemachine.models import User, Workflow, State, Question, Option
from statemachine.forms import SignupForm, LoginForm
import json
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
            user = User.objects.get(email=un)
            dbuser = User.objects.filter(email=un, pwd=pw)
            if pw:
                temp = {}
                temp['name'] = user.name
                request.session['user'] = temp
                print(user.__dict__)

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


def workflow_start(request, workflow_id):
    state = State.objects.filter(workflow_id=workflow_id).filter(initial_state=True).first()
    if state:
        populate_state(state)

    return render(request, "questions.html", {"state": state})


def populate_state(state):
    questions = state.questions.all()
    for q in questions:
        options = q.options.all()
        setattr(q, 'option_set', options)
    setattr(state, 'question_set', questions)


def workflow_submit(request, workflow_id):
    print(request.POST)
    user_response = request.POST.get('response')
    state_id = request.POST.get('state_id')
    state = State.objects.filter(id=state_id).first()
    next_state = None
    print(user_response)
    print(state.next_states.all())
    for s in state.next_states.all():

        if s.validate(user_response):
            populate_state(s)
            next_state = s
            break
    return render(request, "questions.html", {"state": next_state})
