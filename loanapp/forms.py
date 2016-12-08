from loanapp.models import Account, Profile, Loan, Expense, Person
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from easy_select2 import *

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['profile', 'plan_category', 'plan_amount']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = ''
        self.fields['amount'].label = ''

class ExpenseForm2(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['profile', 'category', 'amount']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['plan_category'].label = ''
        self.fields['plan_amount'].label = ''

# Modified choice field
class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

# Initial loan creation on dashboard
class LoanForm1(forms.ModelForm):
    borrower = ChoiceFieldNoValidation()
    class Meta:
        model = Loan
        fields = ['borrower','purpose']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['borrower'].label = "Teen"
        self.fields['borrower'].widget.attrs['placeholder'] = "First Name"
        self.fields['purpose'].label = "Item"
        self.fields['purpose'].widget.attrs['placeholder'] = "e.g. tickets,trip,clothes,phone,etc."
        self.fields['purpose'].widget.attrs['style'] = 'width:70%;'


class LoanForm2(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['original_amt','down_amt', 'interest']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['original_amt'].label = "Cost"
        self.fields['original_amt'].widget.attrs['style'] = 'width:70%;'
        self.fields['interest'].initial = self.fields['interest']
        self.fields['interest'].widget.attrs['style'] = 'width:70%;'
        self.fields['down_amt'].widget.attrs['style'] = 'width:70%;'
class LoanForm3(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['monthly_amt']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['monthly_amt'].label = ""
        self.fields['monthly_amt'].widget.attrs['style'] = 'width:90%;'

class LoanForm4(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['interest']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['interest'].label = "Change Interest Rate"
        self.fields['interest'].widget.attrs['style'] = 'width:70%;'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['loan', 'remaining']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['income'].label = "Monthly Income"

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''
            self.fields[fieldname].widget.attrs['style'] = 'width:70%;'
            self.fields['username'].widget.attrs['placeholder'] = 'Create Username'
            self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return userx


