from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User, Deposit_History, Debit_History, Credit_History
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_debit_receipt_mail(email, user_name, amount, account_balance):
    subject = 'Debit Transaction Receipt'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        'user_name': user_name,
        'amount': amount,
        'account_balance': account_balance
    }
    
    text_content = f'Your account has been debited with {amount}. Your current balance is {account_balance}.'
    html_content = render_to_string('debit_receipt_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_credit_receipt_mail(email, user_name, amount, account_balance):
    subject = 'Credit Transaction Receipt'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        'user_name': user_name,
        'amount': amount,
        'account_balance': account_balance
    }
    
    text_content = f'Your account has been credited with {amount}. Your current balance is {account_balance}.'
    html_content = render_to_string('credit_receipt_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def handler404(request, exception):
    return HttpResponseRedirect('index')


def Index(request):
    if request.method== "POST":
        email = request.POST['email']
        password = request.POST['password']
        user= authenticate(request, email=email, password=password)
    
        if user is not None: 
            login(request, user)
            return redirect("dashboard")         
        else:
            error_message= "Invalid Username or Password"
            return render(request, "index.html", {"error_message":error_message})
    return render(request, 'index.html')


def user_signup(request):
    if request.method== "POST" and 'pass-image' in request.FILES:
        account_type= request.POST["acct_type"]
        gender= request.POST["gender"]
        title= request.POST["title"]
        birth_date= request.POST["birth_date"]
        first_name= request.POST["first_name"]
        middle_name= request.POST["middle_name"]
        last_name= request.POST["last_name"]
        email= request.POST["email"]
        number= request.POST["number"]
        country= request.POST["country"]
        password= request.POST["password"]
        password2= request.POST["password2"]
        ssn= request.POST["ssn"]
        transaction_pin= request.POST["pin"]
        try:
            if password2==password:
                user = User.objects.create_user(transaction_pin=transaction_pin, account_type=account_type, ssn=ssn, title=title, birth_date=birth_date, gender=gender, first_name=first_name, middle_name=middle_name, last_name=last_name, email=email, password=password, passwd= password2, number= number, country=country)
                user.save()
                user = authenticate(request, email=email, password=password)
                login(request, user)
                return redirect("dashboard")   
            else:
                error_message= "Passwords do not match"
                return render(request, "signup.html", {"error_message":error_message})
        except:
            redirect("index")
    return render(request, 'signup.html')


@login_required(login_url='/')
def Dashboard(request):
    user = request.user
    return render(request, "dashboard.html", {'user': user})



@login_required(login_url='/')
def Deposit(request):
    user = request.user
    if request.method == 'POST':
        amount = request.POST['amount']
        deposit = Deposit_History(user=request.user, amount=amount)
        deposit.save()
        return redirect("confirmd", amount=amount)
    return render(request, "deposit.html", {'user': user})


@login_required(login_url='/')
def Payment(request):
    user = request.user
    if request.method=="POST":
        acctnum = request.POST['acct-num']
        amt = request.POST['amount']
        pin= request.POST['pin']

        if user.transaction_pin == pin:
            amount= int(amt)

            if amount <= user.account_balance:
                debit = Debit_History(user=request.user, amount=amount)
                debit.save()
                
                ben = User.objects.get(account_number=acctnum)
                ben.account_balance += amount
                ben.save()

                benC= Credit_History(user=ben, amount=amount)
                benC.save()

                user.account_balance -= amount
                user.save()

                send_debit_receipt_mail(user.email, user.full_name, amount, user.account_balance)
                send_credit_receipt_mail(ben.email, ben.full_name, amount, ben.account_balance)

                return redirect("dashboard")
            else:
                message="Insufficient balance"
                return render(request, 'payment.html', {'user': user, 'message':message})
        else:
            message="Incorrect Transaction Pin"
            return render(request, 'payment.html', {'user': user, 'message': message})
    

    return render(request, 'payment.html', {'user': user})


@login_required(login_url='/')
def History(request):
    user = request.user

    debit_history = Debit_History.objects.filter(user=request.user).order_by('-timestamp')
    credit_history = Credit_History.objects.filter(user=request.user).order_by('-timestamp')
    deposit_history = Deposit_History.objects.filter(user=request.user).order_by('-timestamp')

    combined_history = list(debit_history) + list(credit_history) + list(deposit_history)
    for transaction in combined_history:
        if isinstance(transaction, Debit_History):
            transaction.type = 'Debit'
        elif isinstance(transaction, Credit_History):
            transaction.type = 'Credit'
        elif isinstance(transaction, Deposit_History):
            transaction.type = 'Deposit'

    combined_history.sort(key=lambda x: x.timestamp, reverse=True)

    context = {
        'user': user,
        'combined_history': combined_history
    }

    return render(request, 'history.html', context)


@login_required(login_url='/')
def Cards(request):
    user = request.user
    return render(request, 'cards.html', {'user': user})


@login_required(login_url='/')
def Loan(request):
    user = request.user
    return render(request, 'loan.html', {'user': user})


@login_required(login_url='/')
def Profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required(login_url='/')
def Settings(request):
    user = request.user
    return render(request, 'settings.html', {'user': user})


@login_required(login_url='/')
def Logout(request):
    logout(request)
    return redirect("index")



@csrf_exempt
def get_users_by_account_number(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        if account_number:
            users = User.objects.filter(account_number=account_number)
            users_data = list(users.values('id', 'full_name', 'email'))  # Adjust fields as necessary
            return JsonResponse({'users': users_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)