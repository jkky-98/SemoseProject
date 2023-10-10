from django.shortcuts import render, HttpResponse
import random
# Create your views here.
def index(request):
    return HttpResponse("<h1>Random</h1>" + str(random.randint(1, 100)))