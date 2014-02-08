from django.shortcuts import render
from linecook.models import Appliance, Food, Recipe, Step, User

# Create your views here.
def index(request):
        user_list = User.objects.all()
        context = {'user_list': user_list}
        return render(request, 'linecook/index.html', context)

