from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from statemachine.models import User, Workflow, State, Question, Option, UserState
from statemachine.forms import SignupForm, LoginForm
from os import path
import json


# Create your views here.


def office(request):
    workflow = Workflow.objects.all()
    return render(request, "office.html", {"workflow": workflow})


def home(request):
    return render(request, "home.html")


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


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "login.html")

    def post(self, request):
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            un = MyLoginForm.cleaned_data["email"]
            pw = MyLoginForm.cleaned_data["pwd"]
            print(un)
            print(pw)
            user = User.objects.get(email=un, pwd=pw)
            dbuser = User.objects.filter(email=un, pwd=pw)

            temp = {}
            temp['name'] = user.name
            temp['id'] = user.id
            request.session['user'] = temp
            print(user.__dict__)
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                return redirect("/signup")

            if not dbuser:
                return HttpResponse("Login Failed")

            else:
                return redirect("/office")
        else:
            form = LoginForm()
        return render(request, "login.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect("/")


# def workflow_start(request, workflow_id):
#     user = request.session.get("user")
#     user_state = User.objects.get(user_id=user.id).first()
#     if user_state:
#         state = user_state.save()
#     else:
#         state = State.objects.filter(workflow_id=workflow_id).filter(initial_state=True).first()
#
#     if state:
#         populate_state(state)
#
#     return render(request, "questions.html", {"state": state})


def workflow_start(request, workflow_id):
    user = request.session.get("user")
    print(user)
    user_state_obj = UserState.objects.filter(workflow_id=workflow_id).filter(user_id=user.get("id")).order_by('-id').first()
    if user_state_obj:
        state = user_state_obj.state
        print(state)
    else:
        state = State.objects.filter(workflow_id=workflow_id).filter(initial_state=True).first()
        UserState(state=state, workflow_id=workflow_id, user_id=user.get("id")).save()

    populate_state(state)


    return render(request, "questions.html", {"state": state})


def populate_state(state):
    questions = state.questions.all()
    for q in questions:
        options = q.options.all()
        setattr(q, 'option_set', options)
    setattr(state, 'question_set', questions)


def previous(request, state_id):
    user = request.session.get("user")
    user_state_obj = UserState.objects.filter(state_id=state_id).filter(user_id=user.get("id")).first()
    pre_state_id = user_state_obj.pre_state_id
    state = State.objects.filter(id=pre_state_id).first()
    option_id = user_state_obj.option_id
    print(option_id)


    populate_state(state)

    return render(request, "questions.html", {"state": state, "option_id": option_id})


def workflow_submit(request, workflow_id):
    user = request.session.get("user")
    print(request.POST)
    option_id = request.POST.get('response')
    state_id = request.POST.get('state_id')
    state = State.objects.filter(id=state_id).first()
    s1 = state.questions.get(id=state_id)
    print(s1.question_text)
    next_state = None
    # print(user_response)
    print(state.next_states.all())
    response = Option.objects.filter(id=option_id).first().value
    print(response)
    for s in state.next_states.all():

        if s.validate(response):
            UserState(state=s, pre_state_id=state_id, workflow_id=workflow_id, user_id=user.get("id"), option_id=option_id).save()
            populate_state(s)
            next_state = s
            break

    return render(request, "questions.html", {"state": next_state})


def review(request, workflow_id):
    user = request.session.get("user")
    user_states = UserState.objects.filter(user_id=user.get("id")).filter(workflow_id=workflow_id).order_by('id').all()
    for us in user_states:
        question = us.state.questions.get(id=us.state.id)
        print(question)
        option = question.options.get(id=us.option_id)
        print(option)



    return render(request, "review.html", {"question": question})





