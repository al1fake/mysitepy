import datetime
import logging
import asyncio

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.template import loader

from mysite.settings import LOGGING_LEVEL
from .forms import NewUserForm, NewCommentForm
from .models import Question, Comment

logging.basicConfig(filename='comment.log', level=LOGGING_LEVEL)


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
            loop = asyncio.new_event_loop()
            if comment_form.is_valid():
                new_comment = comment_form.save()
                new_comment.save()
                loop.run_until_complete(log_to_file(True, question_id, name))
                # logging.debug('added comment by ' + name + ' on post with id ' + str(question_id) + '[' +
                #               str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()) + ']')
                return redirect('/polls/'+str(question_id))
            else:
                loop.run_until_complete(log_to_file(False, question_id, name))
                # logging.debug('error while creating comment by ' + name + ' on post with id ' + str(question_id) + '['
                # + str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()) + ']')
            loop.close()

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
            return redirect("/polls")
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


async def log_to_file(is_successful, question_id, name):
    if is_successful:
        logging.info('added comment by ' + name + ' on post with id ' + str(question_id) + '[' +
                      str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()) + ']')
    else:
        logging.info('error while creating comment by ' + name + ' on post with id ' + str(question_id) + '[' +
                      str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()) + ']')
