import django.urls
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.urls import include, path


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:9]
    template = loader.get_template('polls/article.html')
    context = {'latest_question_list': latest_question_list, 'question_id': question_id}
    return render(request, 'polls/article.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

