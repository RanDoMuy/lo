"""
URL configuration for CitiClone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bank import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.Index, name="index"),
    path('signup/', views.user_signup, name="signup"),
    path('dashboard', views.Dashboard, name="dashboard"),
    path('deposit', views.Deposit, name="deposit"),
    path('payment', views.Payment, name="payment"),
    path('history', views.History, name="history"),

    path('get-users-by-account/', views.get_users_by_account_number, name='get_users_by_account'),
    path('cards', views.Cards, name="cards"),
    path('loan', views.Loan, name="loan"),
    path('profile', views.Profile, name="profile"),
    path('settings', views.Settings, name="settings"),
    path('logout', views.Logout, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'bank.views.handler404'
