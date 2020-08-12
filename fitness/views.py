from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def fitness_home(request):
    return render(request, 'fitness/fitness.html')
