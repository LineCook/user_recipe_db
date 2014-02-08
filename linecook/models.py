from django.db import models

# Create your models here.
class Recipe(models.Model):
	#oven, microwave, etc
	appliance = models.ForeignKey('Appliance')
	food = models.ForeignKey('Food')
	user = models.ForeignKey('User')
	#name = self.food.name + " " + self.appliance.device_type + " Recipe"
	
	#def __unicode__(self):
		#return self.name

class Step(models.Model):
	temp = models.IntegerField(blank=True)
	time = models.IntegerField(blank=True)
	#cooking mode
	mode = models.CharField(max_length=20)
	recipe = models.ForeignKey('Recipe')

class User(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	username = models.CharField(max_length=20)
	appliances = models.ManyToManyField('Appliance')

	def __unicode__(self):
		return self.username

class Appliance(models.Model):
	#oven, microwave
	device_type = models.CharField(max_length=30)
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=20)
	#full_name = self.brand + " " + self.model

	#def __unicode__(self):
		#return self.full_name
	
class Food(models.Model):
	name = models.CharField(max_length=40)
	upc = models.CharField(max_length=12)

	def __unicode__(self):
		return self.name
