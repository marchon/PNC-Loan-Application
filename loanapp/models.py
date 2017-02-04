from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
import decimal
import datetime

class Expense(models.Model):
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
	category = models.CharField(max_length=100, default="", null=True)
	amount = models.DecimalField(max_digits=10, default=0.0,decimal_places=2, null=True)
	plan_category = models.CharField(max_length=100, default='0.0', null=True)
	plan_amount = models.DecimalField(max_digits=10, decimal_places=2, default='0.0', null=True)
	def __str__(self):
		return self.category + " : " + str(self.amount)
	def expense_category(self):
		return self.category
	def expense_amount(self):
		return str(self.amount)
	def expense_amount_int(self):
		return self.amount

class Profile(models.Model):
	loan = models.ForeignKey('Loan', on_delete=models.CASCADE, null=True)
	income = models.DecimalField(max_digits=10, decimal_places=2, default='0.0')
	remaining = models.DecimalField(max_digits=10, decimal_places=2, default='0.0')
	def __str__(self):
		return str(self.income)
	def saving(self):
		all_expenses = self.expense_set.all()
		expense_sum = 0
		for e in all_expenses:
			expense_sum += e.amount
		money_left = self.income - expense_sum
		return money_left

class MonthlyPayment(models.Model):
	loan = models.ForeignKey('Loan', on_delete=models.CASCADE, null=True)
	date = models.DateField(auto_now=False)
	remaining_amt = models.DecimalField(max_digits=100, decimal_places=2, null=True)
	interest = models.DecimalField(max_digits=10, decimal_places=5)
	monthly_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	def __str__(self):
		return "Monthly payment is " + self.date + self.remaining_amt + (self.interest / 100) + self.monthly_amt

class LoanManager(models.Manager):
    def create_loan(self, acct, person, purpose):
        new_loan = self.create(acct=acct,person=acct.person_set.filter(name=person).latest('id'),purpose=purpose)
        return new_loan

class Loan(models.Model):
	person = models.ForeignKey('Person',null=True)
	acct = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
	active = models.BooleanField(default=False)
	purpose = models.CharField(max_length=500)
	original_amt = models.DecimalField(max_digits=100, decimal_places=2, default='100.0', null=True)
	down_amt = models.DecimalField(max_digits=100, decimal_places=2, default='0', null=True)
	remaining_amt = models.DecimalField(max_digits=100, decimal_places=2, default='100.0', null=True)
	interest = models.DecimalField(max_digits=10, decimal_places=5, default='2.0', null=True)
	min_monthly_amt = models.DecimalField(max_digits=10, decimal_places=2, default='0.0', null=True)
	monthly_amt = models.DecimalField(max_digits=10, decimal_places=2, default='0.0', null=True)
	objects = LoanManager()
	def __str__(self):
		return str(self.person)
		# + "\nPurpose : " + self.purpose 
		# + "\nRemaining amount : " + self.remaining_amt
		# + "\nInterest : " + self.interest
		# + "\nMonths left : " + str(self.remaining_amt/self.monthly_amt)
	def loan_purpose(self):
		return str(self.purpose);
	def loan_interest(self):
		return str(round(self.interest, 2) / 100)
	def monthly_interest(self):
		return str(round(self.interest / 100, 2))
	def get_absolute_url(self):
		return reverse('loanterms', kwargs={'pk': self.pk})
	def loan_person(self):
		return str((self.person.name))
	def loan_name(self):
		return str((self.person.name)) + "'s " + str(self.purpose)
	def min_amount(self):
		if (round(self.interest / 100) == 1):
			self.min_monthly_amt = 1;
			self.save()
			return 1
		else:
			min_payment = self.original_amt * (self.interest / 100) + decimal.Decimal(0.5)
			self.min_monthly_amt = round(min_payment, 2);
			self.save()
			return round(min_payment, 2)
	def string_monthly_amount(self):
		return str(self.monthly_amt);
	def loan_calculation(self):
		loan_balance = self.original_amt
		monthly_interest = loan_balance * self.interest / 100
		monthly_values = [[round(loan_balance,2), round(monthly_interest, 2), self.monthly_amt, "12/2016"]]
		loan_balance += monthly_interest - self.monthly_amt
		now = datetime.datetime.now()
		months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
		years  = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
		i = 0
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * (self.interest/100)
			month = months[i%12]
			year = years[i//12]
			if (loan_balance + monthly_interest <= self.monthly_amt):
				monthly_values.append([round(loan_balance, 2), round(monthly_interest, 2), round(loan_balance + monthly_interest, 2), str(month) + "/" + str(year)])
				return monthly_values	
			monthly_values.append([round(loan_balance, 2), round(monthly_interest, 2), self.monthly_amt, str(month) + "/" + str(year)])
			loan_balance -= self.monthly_amt + monthly_interest
			i += 1
		return monthly_values
	def total_months(self):
		loan_balance = self.remaining_amt
		monthly_interest = loan_balance * self.interest / 100
		loan_balance += monthly_interest - self.monthly_amt
		i = 0
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * self.interest / 100
			loan_balance -= self.monthly_amt + monthly_interest
			i += 1
		return i + 1
	def total_interest(self):
		loan_balance = self.remaining_amt
		monthly_interest = loan_balance * (self.interest/100)
		total_sum = monthly_interest
		loan_balance += monthly_interest - self.monthly_amt
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * self.interest / 100
			loan_balance -= self.monthly_amt + monthly_interest
			total_sum += monthly_interest
		return round(total_sum, 2)
	def total_cost(self):
		loan_balance = self.remaining_amt
		monthly_interest = loan_balance * (self.interest/100)
		total_sum = monthly_interest
		loan_balance += monthly_interest - self.monthly_amt
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * (self.interest/100)
			loan_balance -= self.monthly_amt + monthly_interest
			total_sum += monthly_interest
		return round(self.original_amt + total_sum, 2)
	def loan_information(self):
		loan_amount = "$" + str(int(self.original_amt)) + " loan"
		loan_interest = str(round(self.interest,2) / 100) + str("% Interest Rate")
		loan_monthly_payment = "$" + str(self.monthly_amt) + " Monthly Payment"
		return loan_amount + ", " + loan_interest + ", " + loan_monthly_payment
	def loan_starting(self):
		loan_balance = self.remaining_amt
		monthly_interest = loan_balance * (self.interest / 100)
		loan_balance -= self.monthly_amt + monthly_interest
		i = 0
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * (self.interest / 100)
			loan_balance -= self.monthly_amt + monthly_interest
			i += 1
		loan_total_months = i + 1
		return [loan_total_months, int(self.original_amt)]
	def loan_paid(self):
		loan_paid_amt = int(self.original_amt) - int(self.remaining_amt)
		loan_paid_months = 0 #self.MonthlyPayment.all.count 
		return [loan_paid_months, loan_paid_amt]
	def loan_remaining(self):
		loan_balance = self.remaining_amt
		monthly_interest = loan_balance * (self.interest / 100)
		loan_balance -= self.monthly_amt + monthly_interest
		i = 0
		while ((loan_balance + self.monthly_amt - monthly_interest) - self.monthly_amt + monthly_interest) > 0:
			monthly_interest = loan_balance * (self.interest / 100)
			loan_balance -= self.monthly_amt + monthly_interest
			i += 1
		loan_total_months = i + 1
		loan_remaining_months = i + 1
		loan_remaining_amount = self.remaining_amt
		return [loan_remaining_months, loan_remaining_amount]

class PersonManager(models.Manager):
    def create_person(self, acct, name):
    	try:
    		return acct.person_set.get(name=name)
    	except Person.DoesNotExist:
    		print("dne error")
    		return self.create(acct=acct,name=name)
    	else:
    		print("other error")

class Person(models.Model):
	acct = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=255)
	objects = PersonManager()
	def __str__(self):
		return self.name

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.user.username

# Function to create family account every time user is created
def createUserAccount(sender, instance, created, **kwargs):
    if created:
       account, created = Account.objects.get_or_create(user=instance)

post_save.connect(createUserAccount, sender=User)


