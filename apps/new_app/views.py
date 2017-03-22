from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Secret

# Create your views here.
def index(request):
	return render(request, 'new_app/index.html')

def register(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password'].encode('utf-8')
		confirm_password = request.POST['confirm_password'].encode('utf-8')

		validation = User.userManager.validation(first_name, last_name, email, password, confirm_password)
		if validation[0]:
			pwhash = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.userManager.create(first_name=first_name, last_name=last_name, email=email, password=pwhash)
			request.session['userid'] = user.id
			request.session['user'] = user.first_name
			return redirect('/secrets')
		else:
			for msg in validation[1]:
				messages.warning(request, msg)

			return redirect('/')
	else:
		return redirect('/')

def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password'].encode('utf-8')

		user = User.userManager.filter(email=email)
		if len(user) == 1:
			user = user[0]
			hashed = user.password.encode('utf-8')

			if bcrypt.hashpw(password, hashed) == hashed:
				request.session['userid'] = user.id
				request.session['user'] = user.first_name
				return redirect('/secrets')
			else:
				messages.warning(request, 'Unknown email/password combination')
				return redirect('/')
		else:
			messages.warning(request, 'Unknown email/password combination')
			return redirect('/')

def secrets(request):
	# get yourself
	# test self__in=secret.likes.user
	secrets = Secret.secretManager.all().order_by('-created_at')
	user = User.userManager.get(id=request.session['userid'])
	context = {
		'secrets': secrets,
		'user': user
	}
	return render(request, 'new_app/secrets.html', context)

def add(request):
	if request.method == 'POST':
		secret = request.POST['secret']
		validation = Secret.secretManager.validation(secret)
		if validation[0] == False:
			messages.warning(request, validation[1])
			return redirect('/secrets')

		user = User.userManager.get(id=request.session['userid'])
		secret_added = Secret.secretManager.create(content=secret, created_by=user)

		return redirect('/secrets')
	else:
		return redirect('/secrets')

def delete(request, id):
	if id == '':
		return redirect('/secrets')

	secret = Secret.secretManager.get(id=id)
	secret.delete()
	return redirect('/secrets')

def like(request, id):
	if id == '':
		return redirect('/secrets')

	secret = Secret.secretManager.get(id=id)
	user = User.userManager.get(id=request.session['userid'])
	user.secrets.add(secret)
	return redirect('/secrets')

def popular(request):
	secrets = Secret.secretManager.all().order_by('created_at')
	user = User.userManager.get(id=request.session['userid'])
	context = {
		'secrets': secrets,
		'user': user
	}
	return render(request, 'new_app/popular.html', context)
