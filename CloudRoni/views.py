from django.shortcuts import render
from django.http import HttpResponse
 
def foo(request):
 return HttpResponse("Hello World!")
