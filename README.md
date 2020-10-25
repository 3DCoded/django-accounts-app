SETUP: 
1. Install requirements via "pip install -r requirements.txt"

USAGE: 
1. Copy the accounts folder in to the toplevel directory of your django project. 
2. In your settings.py, add "accounts" to the INSTALLED_APPS list. 
3. In your urls.py, add: 
	from django.urls import include
	urlpatterns.append(path("accounts/", include("accounts.urls"))
5. Where to find these new features (URLs): 
	Login: accounts/login/
	Signup: accounts/signup/
	Accounts Edit: accounts/
6. To logout, send a blank POST request to url name "accounts:logout" or url path "accounts/logout/"