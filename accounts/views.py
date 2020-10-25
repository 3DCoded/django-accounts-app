from django.shortcuts import render, redirect
from django.contrib import auth
from hashlib import sha1
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required

SIGNUP = 'accounts/signup.html'
LOGIN = 'accounts/login.html'
HOME = 'accounts/home.html'

def ispwned(pwd):
    sha = sha1(pwd.encode()).hexdigest().upper()
    pre = sha[:5]
    pwds = urlopen(f'https://api.pwnedpasswords.com/range/{pre}').read().decode().splitlines()
    for pwd in pwds:
        suf, num = pwd.split(':')
        if sha == (pre + suf):
            return int(num)
    return 0

def signup(request):
    if request.method == 'GET':
        return render(request, SIGNUP)
    else:
        username = request.POST['username']
        pwd = request.POST['pwd']
        pwdc = request.POST['pwdc']
        if pwd == pwdc:
            try:
                User.objects.get(username = username)
                return render(request, SIGNUP, {'error': 'Username already taken'})
            except:
                if ispwned(pwd):
                    return render(request, SIGNUP, {'error': 'Password is too common. '})
                user = User.objects.create_user(username, password = pwd)
                user.save()
                auth.login(request, user)
                return redirect('home')
        return render(request, SIGNUP, {'error': 'Passwords given do not match'})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']
        user = auth.authenticate(username = username, password = pwd)
        if user:
            auth.login(request, user)
            if request.POST.get('next'):
                if request.POST['next'].strip():
                    return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, LOGIN, {'error': 'Invalid Credentials'}, status = 401)
    else:
        return render(request, LOGIN)

@login_required
def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            auth.logout(request)
            return redirect('home')
        else:
            return redirect('accounts:login')
    else:
        return redirect('home')

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            method = request.POST.get('method')
            if method:
                if method == 'pwdchange':
                    user = request.user
                    old = request.POST['old']
                    new = request.POST['new']
                    newc = request.POST['newc']
                    if auth.authenticate(username=user.username, password=old):
                        if new == newc:
                            if ispwned(new):
                                return render(request, HOME, {'error': 'Password is too common. '})
                            user.set_password(new)
                            user.save()
                            auth.login(request, auth.authenticate(username=request.user.username, password=new))
                            return render(request, HOME, {'message': 'Password Successfully Changed'})
                        else:
                            return render(request, HOME, {'error': 'Provided Passwords do not match. '})
                    else:
                        return render(request, HOME, {'error': 'Invalid Credentials'})
                elif method == 'delete':
                    request.user.delete()
                    return redirect('home')
                else:
                    return render(request, HOME, {'error': 'Invalid Method'})
            else:
                return render(request, HOME, {'error': 'Missing Method'})
        else:
            return render(request, HOME)
    else:
        return redirect('accounts:login')

