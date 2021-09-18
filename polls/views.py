import asyncio
import datetime
import logging
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from mysite.settings import LOGGING_LEVEL
from .forms import NewUserForm, NewCommentForm
from .models import Question, Comment
from .serializers import CommentSerializer

logging.basicConfig(filename='comment.log', level=LOGGING_LEVEL)


class IndexViewSet(TemplateView):
    def get(self, request):
        article_data = Question.objects.order_by('-pub_date')[:9]
        template = loader.get_template('polls/index.html')
        context = {'latest_question_list': article_data}
        return render(request, 'polls/index.html', context)


def index(request):
    # if request.user.is_authenticated:
    #     name = request.user.username
    # else:
    #     name = 'Not Logged In'
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'name']
    # def get(self, request):
    #     articles = Comment.objects.order_by('-id')
    #     serialized = CommentSerializer(articles, many=True)
    #     return Response({'articles': serialized})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id == request.user.id or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotFound('Comment not found')



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
               'comment_form': comment_form, 'name': name, 'userid': request.user.id}
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
