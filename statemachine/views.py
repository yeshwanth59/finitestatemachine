from django.db.models.options import Options
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from statemachine.models import User, Workflow, State, Question, Option, UserState
from statemachine.forms import SignupForm, LoginForm, ProfileForm
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


def profile(request):
    user = User.objects.all().first()
    return render(request, "profile.html", {"user": user})


def profile_update(request):
    user = User.objects.all().first()
    if request.method == "POST":
        name = request.POST['name']
        mobileNo = request.POST['mobileNo']
        email = request.POST['email']
        pwd = request.POST['pwd']
        address = request.POST['address']
        user.name = name
        user.mobileNo = mobileNo
        user.email = email
        user.pwd = pwd
        user.address = address
        user.save()
        return redirect("/")
    return render(request, "profile_update.html", {"user": user})


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
            temp['mobileNo'] = user.mobileNo
            temp['email'] = user.email
            temp['pwd'] = user.pwd
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
    user_state_obj = UserState.objects.filter(state_id=state_id).filter(user_id=user.get("id")).order_by("-id").first()
    pre_state_id = user_state_obj.pre_state_id
    user_state_obj = UserState.objects.filter(state_id=pre_state_id).filter(user_id=user.get("id")).order_by("-id").first()
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

    current_state = State.objects.filter(id=state_id).first()
    user_state = UserState.objects.filter(state_id=current_state.id).filter(user_id=user.get('id')).order_by("-id").first()
    user_state.option_id = option_id
    user_state.save()

    next_state = None

    response = Option.objects.filter(id=option_id).first().value
    print(response)

    for s in current_state.next_states.all():
        print(s.name)

        if s.validate(response):
            print("validate"+s.name)
            UserState(state=s, pre_state_id=state_id, workflow_id=workflow_id, user_id=user.get("id")).save()
            populate_state(s)
            next_state = s
            break

    return render(request, "questions.html", {"state": next_state})


def review(request, workflow_id):
    user = request.session.get("user")
    user_states = UserState.objects.filter(user_id=user.get("id")).filter(workflow_id=workflow_id).order_by('id').all()
    final_list = list()
    for us in user_states:
        state = us.state
        if us.option_id:
            question = Question.objects.get(state_id=us.state.id)
            option = Option.objects.get(id=us.option_id)
            setattr(us, 'question_text', question.question_text)
            setattr(us, 'answer', option.value)
            final_list.append(us)
    try:
        return render(request, "review.html", {"responses": final_list, "state": state})
    except:
        return HttpResponse("""<html><body><h3 style="color:red;" align="center">"no review available"</h3></body>
            </html>""")



def doctor(request, workflow_id):
    user = request.session.get("user")
    user_states = UserState.objects.filter(user_id=user.get("id")).filter(workflow_id=workflow_id).order_by('id').all()
    final_list = list()
    for us in user_states:
        state = us.state
        if us.option_id:
            question = Question.objects.get(state_id=us.state.id)
            option = Option.objects.get(id=us.option_id)
            setattr(us, 'question_text', question.question_text)
            setattr(us, 'answer', option.value)
            final_list.append(us)

    return render(request, "doctor.html", {"user": user, "responses": final_list, "state": state})




