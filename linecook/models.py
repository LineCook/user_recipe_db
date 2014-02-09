from django.db import models
from xmlrpclib import ServerProxy, Error

#this API key is registered to Aaron VerDow and is for testing only
#please do not abuse
rpc_key = 'b3a5dd0d02f7decf260df11dda7dd6b92464d852'

# Create your models here.
class Recipe(models.Model):
	#oven, microwave, etc
	appliance = models.ForeignKey('Appliance')
	food = models.ForeignKey('Food')
	user = models.ForeignKey('User')
	def name(self):
		full_name = self.user.username + ' ' + self.food.name + ' ' + self.appliance.device_type + ' Recipe'
		return full_name

	def get_recipe(self):

		#check if the recipe has any steps associated
		if self.step_set.all():
			recipe = self
		else:
			#check for recipes of the same exact appliance
			for other_recipe in Recipe.objects.filter(appliance = self.appliance, food = self.food):
				if other_recipe.step_set.all():
					recipe = other_recipe
					break
			if not 'recipe' in locals():
				#check for recipes of any appliance of the same type
				for other_recipe in Recipe.objects.filter(appliance__device_type = self.appliance.device_type, food = self.food):
					if other_recipe.step_set.all():
						recipe = other_recipe
						break
				if not 'recipe' in locals():
					recipe = []
		return recipe

	def get_steps(self):
		recipe = self.get_recipe()
		try:
			return recipe.step_set.all()
		except AttributeError:
			return []

	def human_instructions(self):
		output = ''
		recipe = self.get_recipe()
		try:
			for step in recipe.step_set.all():
				if step.mode == 'P':
					output += 'Preheat to ' + str(step.temp) + ' '
				elif step.mode == 'B':
					output += 'bake at ' + str(step.temp) + ' for ' + str(step.time) + ' minutes, '
				else:
					output += step.mode + ' at ' + str(step.temp) + ' for ' + str(step.time) + ' minutes, '

			output += 'by ' + str(recipe.user)
		except AttributeError:
			output = ''
		
		return output
				

	
	def __unicode__(self):
		return self.name()

class Step(models.Model):
	temp = models.IntegerField(blank=True)
	time = models.IntegerField(blank=True)
	#cooking mode
	mode = models.CharField(max_length=20)
	recipe = models.ForeignKey('Recipe')
	
	def __unicode__(self):
		return self.recipe.name() + ' Step'

class User(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	username = models.CharField(max_length=20)
	appliances = models.ManyToManyField('Appliance',blank=True,through='UserAppliance')

	def __unicode__(self):
		return self.username

class Appliance(models.Model):
	#oven, microwave
	device_type = models.CharField(max_length=30)
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=20)
	#full_name = self.brand + " " + self.model

	def __unicode__(self):
		return self.model

class UserAppliance(models.Model):
	user = models.ForeignKey('User')
	appliance = models.ForeignKey('Appliance')

	def __unicode__(self):
		return self.user.username + ' ' + self.appliance.model
	
class Food(models.Model):
	name = models.CharField(max_length=140,blank=True)
	upc = models.CharField(max_length=40)

	def set_name_from_cloud(self):
                s = ServerProxy('http://www.upcdatabase.com/xmlrpc')
                params = { 'rpc_key': rpc_key, 'upc': self.upc }
                response = s.lookup(params)
		if response['status'] == 'success':
			self.name = response['description']
			self.save()
		return

	def __unicode__(self):
		if self.name:	
			return self.name
		else:
			return 'Barcode ' + self.upc

