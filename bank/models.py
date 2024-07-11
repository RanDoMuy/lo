from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
import random, string


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



ACCOUNT_TYPE = [
    ('Savings Account', 'Savings Account'),
    ('Current Account', 'Current Account')
]

GENDER= [
    ('Male', 'Male'),
    ('Female', 'Female'),
]
 
TITLE= [
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Ms.', 'Ms.'),
    ('Dr.', 'Dr.')
]

TRANSACTION= [
    ('Deposit', 'Deposit'),
    ('Transfer', 'Transfer')
]

TRANSACTION_STATUS= [
    ('PENDING', 'PENDING'),
    ('SUCCESS', 'SUCCESS')
]

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    title= models.CharField("Title", choices=TITLE, max_length=10, null=True, blank=True)
    first_name = models.CharField("First Name", max_length= 50, null=True, blank=True)
    middle_name = models.CharField("Middle Name", max_length= 50, null=True, blank=True)
    last_name = models.CharField("Last Name", max_length= 50, null=True, blank=True)
    full_name = models.CharField("Full Name", max_length= 50, null=True, blank=True)
    number= models.CharField("Phone Number", max_length=20, null=True, blank=True)
    birth_date= models.DateField("Date Of Birth", auto_now=False, auto_now_add=False, null=True, blank=True)
    gender=models.CharField("Gender", choices=GENDER, max_length=50, null=True, blank=True)
    passwd=models.CharField("Passwd", max_length=50, null=True, blank=True)

    # CLIENT LOCATION INFO
    country = models.CharField("Country", max_length= 50, null=True, blank=True)


    # CLIENT CONFI INFO
    #ssn, ni, sin
    ssn= models.CharField("SSN", max_length= 50, null=True, blank=True)

    # CLIENT ACCOUNT INFO
    reward_balance= models.IntegerField("Reward Balance", default=0, validators=[MaxValueValidator(9999999999)])
    loan_balance= models.IntegerField("Loan Balance", default=0, validators=[MaxValueValidator(9999999999)])
    account_type= models.CharField("Account Type", choices=ACCOUNT_TYPE, max_length=50, null=True, blank=True)
    account_number= models.CharField("Account Number", max_length=50, null=True, blank=True)
    account_balance= models.IntegerField("Account Balance", default=0, validators=[MaxValueValidator(9999999999)])
    transaction_pin= models.CharField("Transaction PIn", max_length=4, null=True, blank=True)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def generate_account_number(self):
        characters = string.digits
        code_length = 10
        self.account_number = ''.join(random.choice(characters) for _ in range(code_length))

    def save(self, *args, **kwargs):
        self.full_name = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))
        if not self.account_number:
            self.generate_account_number()
        super().save(*args, **kwargs)



class Debit_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.IntegerField("Debit Amount", validators=[MaxValueValidator(9999999999)], null=True, blank=True)
    timestamp= models.DateTimeField("Date", auto_now_add=False)
    note = models.TextField("Debit Note", max_length= 50, null=True, blank=True, )
    beneficiary= models.CharField("Beneficiary", max_length= 50, null=True, blank=True)

    def __str__(self):
        return self.user.email
    

class Credit_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.IntegerField("Credit Amount", validators=[MaxValueValidator(9999999999)], null=True, blank=True,)
    timestamp= models.DateTimeField("Date", auto_now_add=False)
    note = models.TextField("Credit Note", max_length= 50, null=True, blank=True,)
    sender= models.CharField("Sender", max_length= 50, null=True, blank=True,)

    def __str__(self):
        return self.user.email
    

class Deposit_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.IntegerField("Deposit Amount", validators=[MaxValueValidator(9999999999)], null=True, blank=True,)
    timestamp= models.DateTimeField("Date", auto_now_add=False)
    status= models.CharField("Deposit Status", default="PENDING", choices=TRANSACTION_STATUS, max_length= 50, null=True, blank=True,)
    method= models.CharField("Deposit Method", default= "BITCOIN", max_length= 50, null=True, blank=True,)

    def __str__(self):
        return self.user.email
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField("Notification", max_length= 50, null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Notification for {self.user.email} - {"Read" if self.is_read else "Unread"}'
