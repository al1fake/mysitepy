import django.urls
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Comment
from django.template import loader
from django.urls import include, path
from .forms import NewUserForm, NewCommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout

def index(request):
    # if request.user.is_authenticated:
    #     name = request.user.username
    # else:
    #     name = 'Not Logged In'
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    if request.user.is_authenticated:
        name = request.user.username
        comment_form = NewCommentForm()

        if request.method == 'POST':
            comment_form = NewCommentForm(data=request.POST)

            if comment_form.is_valid():
                new_comment = comment_form.save()
                new_comment.save()
                return redirect('/polls/'+str(question_id))
            print(request.user.username)
            print(comment_form.errors.as_data())

    else:
        comment_form = 1
        name = 0
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    comments = Comment.objects.filter(post_id=question_id).order_by('-id')

    template = loader.get_template('polls/article.html')
    context = {'latest_question_list': latest_question_list, 'question_id': question_id, 'comments': comments,
               'comment_form': comment_form, 'name': name}
    return render(request, 'polls/article.html', context)


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="polls/reg.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/polls")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="polls/login.html", context={"login_form": form})


def success(request):
    template = loader.get_template('polls/success.html')
    print(request.POST.get('login', None))
    request.POST.get('email', None)
    request.POST.get('password', None)
    return render(request, 'polls/success.html')


def logout_view(request):
    logout(request)
    return redirect("/polls")
