from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Event Management System")

def show_task(request):
    return HttpResponse("This is our Task page")