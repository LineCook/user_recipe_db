from django.shortcuts import render
from linecook.models import Appliance, Food, Recipe, Step, User, UserAppliance
from django.http import HttpResponse

# Create your views here.
def index(request):
        user_list = User.objects.all()
        context = {'user_list': user_list}
        return render(request, 'linecook/index.html', context)

def user_detail(request, user_name):
        user = User.objects.get(username=user_name)
        context = {'user': user}
        return render(request, 'linecook/user_detail.html', context)

def recipe_detail(request, user_name, recipe_id):
	recipe = Recipe.objects.get(id=recipe_id)
        user = User.objects.get(username=user_name)
	if request.method == "POST":
		if request.POST['action'] == 'delete':
			recipe.step_set.order_by('id').reverse()[0].delete()
		else:
			step = Step(recipe = recipe, temp = request.POST['temp'], time = request.POST['time'], mode = request.POST['mode'])
			step.save()
        context = {'user': user, 'recipe': recipe}
        return render(request, 'linecook/recipe_detail.html', context)
	

def scan(request, app_id, upc):
	userappliance = UserAppliance.objects.get(id=app_id)
	appliance = userappliance.appliance
	user = userappliance.user
	try:
		food = Food.objects.get(upc=upc)
	except Food.DoesNotExist:
		food = Food(upc=upc)
		food.save()
		food.set_name_from_cloud()
	#create a user recipe no matter what so we know the user has scanned this food
	try:
		user_recipe = Recipe.objects.get(user = user, appliance = appliance, food = food)
	except Recipe.DoesNotExist:
		user_recipe = Recipe(user = user, appliance = appliance, food = food)
		user_recipe.save()

	steps = user_recipe.get_steps()
	output = ''
	for step in steps:
		output += step.mode + str(step.temp) + "T" + str(step.time) + ":"

	if output == '':
		output = "recipe not found"

	return HttpResponse(output)
