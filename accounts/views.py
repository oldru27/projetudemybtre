from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.


def register(request):
  # Get form value
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
  # Check if password match
    if password == password2:
      # Check usernam
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is taken')
          return redirect('register')
        else:
          user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name, password=password, email=email)
          #Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are logged')
          # return redirect('index')
          user.save() #fait doublon avec create_user
          messages.success(request, 'You now registered and you can now log')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')

  else:
    return render(request, 'account/register.html')

def login(request):
  if request.method == 'POST':
    #Login USER
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are loggedin')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'account/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('index')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request, 'account/dashboard.html', context)