from django.shortcuts import render


def HomePageView(request):
    return render(request, 'base.html')