from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.messages import get_messages
# from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from .models import Account, Person, Profile, Expense, Loan
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import formset_factory, BaseFormSet
from loanapp.forms import *
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Start - login page
def index(request):
	context = RequestContext(request)
	if request.method == "POST":
		form = UserCreateForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user.save()
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
			login(request, user)
			return redirect('dashboard')
		else:
			print("errors")
	else:
		form = UserCreateForm() 
	return render(request, 'loanapp/index.html', {'form': form}, context)

# Handling logins
def login_view(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'loanapp/index.html', {}, context)

# Handling logouts
def logout_view(request):
    logout(request)
    return redirect('index')

# Dashboard
@login_required()
def dashboard(request):
	context = RequestContext(request)
	acct = request.user.account
	help_text = "To get started, just select your teen's name from the dropdown list, or add your child if this is his or her first loan. Then create a note about what the loan will be used for."
	if request.method == "POST":
		form = LoanForm1(data=request.POST)
		if form.is_valid():
			person = (Person.objects.create_person(acct, form.cleaned_data['borrower']))
			person.save()
			new_loan = (Loan.objects.create_loan(acct,form.cleaned_data['borrower'],form.cleaned_data['purpose']))
			new_loan.person = person
			new_loan.save()
			return redirect('make_profile')
		else:
			print("errors")
	#else if request.method == "GET":
	else:
		form = LoanForm1()
	return render(request, 'loanapp/dashboard.html', {'loans' : acct.loan_set.all(), 
			'form': form, 'help_text': help_text}, context)

# Setting up the loan
@login_required()
def make_loan(request):
	acct = request.user.account
	context = RequestContext(request)
	if request.method == "POST":
		current_loan = acct.loan_set.latest('id')
		current_profile = (acct.loan_set.latest('id')).profile_set.latest('id')
		current_expenses = current_profile.expense_set.all()
		l1_form = LoanForm2(request.POST)
		l2_form = LoanForm3(request.POST)
		if l1_form.is_valid() and l2_form.is_valid():
			current_loan.original_amt = l1_form.cleaned_data['original_amt']
			current_loan.remaining_amt = current_loan.original_amt
			current_loan.monthly_amt = l2_form.cleaned_data['monthly_amt']
			current_loan.interest = l1_form.cleaned_data['interest']
			current_loan.down_amt = l1_form.cleaned_data['down_amt']
			current_loan.active = True
			current_loan.save()
			return redirect('loanapp/loan_creation.html')
		else:
			print("errors")
	# else if request.method == "GET":
	else:
		current_profile = (acct.loan_set.latest('id')).profile_set.latest('id')
		current_expenses = current_profile.expense_set.all()
		current_loan = acct.loan_set.latest('id')
		l1_form = LoanForm2(initial={'down_amt': current_loan.down_amt, 'original_amt': current_loan.original_amt, 'interest': round(current_loan.interest, 2)})
		if (current_loan.monthly_amt < current_loan.min_monthly_amt):
			current_loan.monthly_amt = current_loan.min_monthly_amt
			current_loan.save()
		l2_form = LoanForm3(initial={'monthly_amt':current_loan.monthly_amt})
	return render(request, 'loanapp/loan_creation.html', {'profile' : current_profile, 'loan' : acct.loan_set.latest('id'), 
		'loan_form_1' : l1_form, 'loan_form_2': l2_form, 'expenses' : current_expenses}, context)

# Setting up the loan
@login_required()
def revisit_loan(request):
	acct = request.user.account
	context = RequestContext(request)
	if request.method == "POST":
		current_loan = acct.loan_set.latest('id')
		l1_form = LoanForm4(request.POST, instance=current_loan)
		l2_form = LoanForm3(request.POST, instance=current_loan)
		if l1_form.is_valid() and l2_form.is_valid():
			current_loan.original_amt = l1_form.cleaned_data['original_amt']
			current_loan.remaining_amt = current_loan.original_amt
			current_loan.monthly_amt = l2_form.cleaned_data['monthly_amt']
			current_loan.interest = l1_form.cleaned_data['interest']
			current_loan.active = True
			current_loan.save()
			return redirect('loanapp/loan_revisit.html')
		else:
			print("errors")
	# else if request.method == "GET":
	else:
		l1_form = LoanForm4()
		l2_form = LoanForm3()
		current_profile = (acct.loan_set.latest('id')).profile_set.latest('id')
		current_expenses = current_profile.expense_set.all()
	return render(request, 'loanapp/loan_revisit.html', {'profile' : current_profile, 'loan' : acct.loan_set.latest('id'), 
		'loan_form_1' : l1_form, 'loan_form_2': l2_form, 'expenses' : current_expenses}, context)

# Update Loan

class LoanCreate(CreateView):
    model = Loan
    fields = ['name']

class LoanUpdate(UpdateView):
    model = Loan
    fields = ['name']

# Creating a profile
@login_required()
@csrf_protect
def make_profile(request):
	acct = request.user.account
	context = RequestContext(request)
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				print(form.as_table())
				form.empty_permitted = False
	ExpenseFormSet = formset_factory(ExpenseForm, extra=1, formset=RequiredFormSet)
	if request.method == "POST":
		profile_form = ProfileForm(request.POST)
		expense_formset = ExpenseFormSet(request.POST, request.FILES)
		if profile_form.is_valid() and expense_formset.is_valid():
			new_profile = profile_form.save(commit=False)
			new_profile.loan = acct.loan_set.latest('id') 
			new_profile.save()
			for form in expense_formset.forms:
				e = form.save(commit=False)
				e.plan_category = e.category
				e.plan_amount = e.amount
				e.profile = new_profile
				e.save()
			return redirect('make_loan')
		else:
			print("errors")
	else:
		profile_form = ProfileForm()
		expense_formset = ExpenseFormSet()
	c = { 'acct': acct, 
		'messages': messages,
		'profile_form': profile_form,
		'expense_formset' : expense_formset
		}
	# c.update(csrf(request))
	return render(request, 'loanapp/profile_creation.html', c, context)

# Getting names for select2
@login_required()
def users(request):
	q = request.GET.get('q', '')
	people = request.user.account.person_set.filter(name__icontains=q).all()
	opt = sorted((list(map(lambda x: {'text': x.name, 'id': x.id}, people))), key=lambda x: x['text'])
	if len(people.filter(name=q)) == 0:
		opt.append({'text': '%s (new user)' % q, 'id': '%s' % q})
	return JsonResponse(opt, safe=False)

