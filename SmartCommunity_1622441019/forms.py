import logging
from django import forms
from django.forms import ModelForm
from django.contrib.auth import hashers


from SmartCommunity_1622441019.models import User_1622441019, Provider_1622441019, Admin_1622441019


class AddInfo(ModelForm):
    class Meta:
        model = Provider_1622441019
        fields = '__all__'
        widgets = {
                'emailAddress': forms.EmailInput(attrs={'placeholder': 'Enter a valid e-mail.'}),
                'name': forms.TextInput(attrs={'placeholder': 'Enter a valid provider name.'}),
                'address': forms.TextInput(attrs={'placeholder': 'Enter a valid address.'}),
                'phoneNumber': forms.TextInput(attrs={'placeholder': 'Enter a valid phone number.'}),
                'providerPrice': forms.TextInput(attrs={'placeholder': 'Enter a valid price.'}),
            }
        labels = {
                'emailAddress': 'E-mail address',
                'name': 'Provider name',
                'phoneNumber': 'Phone number',
                'providerType': 'Provider type',
            }


class CreateAdmin(ModelForm):
    confirm = forms.CharField(label='Confirm password',
                              widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password...'}))

    class Meta:
        model = Admin_1622441019
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Choose a password...'}),
            'firstName': forms.TextInput(attrs={'placeholder': 'Enter your given name...'}),
            'lastName': forms.TextInput(attrs={'placeholder': 'Enter your surname...'}),
            'emailAddress': forms.EmailInput(attrs={'placeholder': 'Enter a valid e-mail....'})
        }
        labels = {
            'emailAddress': 'E-mail address',
            'firstName': 'First name',
            'lastName': 'Last name',
        }

    def clean(self):
        cleanedData = super(CreateAdmin, self).clean()
        password = cleanedData.get("password")
        confirm = cleanedData.get("confirm")
        logging.debug("Cleaned")
        if password != confirm:
            raise forms.ValidationError("Your passwords don't match.")

        if Admin_1622441019.objects.filter(emailaddress__iexact=cleanedData.get("emailAddress")).exists():
            raise forms.ValidationError("Username taken")


class AdminModel(ModelForm):
    class Meta:
        model = Admin_1622441019
        fields = ['emailAddress', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password...'}),
            'emailAddress': forms.TextInput(attrs={'placeholder': 'Enter your username...'}),
            }
        labels = {
                'emailAddress': 'E-mail address',
            }

    def clean(self):
        cleanedData = super(AdminModel, self).clean()
        cUsername = cleanedData.get("emailAddress")
        try:
            admin = Admin_1622441019.objects.get(emailaddress__iexact=cUsername)
            if hashers.check_password(cleanedData.get("password"), admin.password):
                logging.debug("test")
            else:
                raise forms.ValidationError("Username or password incorrect")
        except User_1622441019.DoesNotExist:
            raise forms.ValidationError("Username or password incorrect")


class LoginModel(ModelForm):
    rememberMe = forms.BooleanField(label="Remember me", required=False)

    class Meta:
        model = User_1622441019
        fields = ['emailAddress', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password...'}),
            'emailAddress': forms.TextInput(attrs={'placeholder': 'Enter your username...'}),
            }
        labels = {
                'emailAddress': 'E-mail address',
            }

    def clean(self):
        cleanedData = super(LoginModel, self).clean()
        cUsername = cleanedData.get("emailAddress")
        try:
            user = User_1622441019.objects.get(emailAddress__iexact=cUsername)
            if hashers.check_password(cleanedData.get("password"), user.password):
                logging.debug(cleanedData.get("rememberMe"))
            else:
                raise forms.ValidationError("Username or password incorrect")
        except User_1622441019.DoesNotExist:
            raise forms.ValidationError("Username or password incorrect")


class RegisterForm(ModelForm):
    confirm = forms.CharField(label='Confirm password',
                              widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password...'}))

    class Meta:
        model = User_1622441019
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Choose a password...'}),
            'firstName': forms.TextInput(attrs={'placeholder': 'Enter your given name...'}),
            'lastName': forms.TextInput(attrs={'placeholder': 'Enter your surname...'}),
            'emailAddress': forms.EmailInput(attrs={'placeholder': 'Enter a valid e-mail....'})
        }
        labels = {
            'emailAddress': 'E-mail address',
            'firstName': 'First name',
            'lastName': 'Last name',
            'userType': 'User type',
        }

    def clean(self):
        cleanedData = super(RegisterForm, self).clean()
        password = cleanedData.get("password")
        confirm = cleanedData.get("confirm")
        logging.debug("Cleaned")
        if password != confirm:
            raise forms.ValidationError("Your passwords don't match.")

        if User_1622441019.objects.filter(emailAddress__iexact=cleanedData.get("emailAddress")).exists():
            raise forms.ValidationError("Username taken")


class EditProfile(forms.Form):
    firstName = forms.CharField(label='Update user first name.',
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your new first name...'}))
    lastName = forms.CharField(label='Update user last name.',
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your new last name...'}))
    password = forms.CharField(label='New password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password...'}))
    confirm = forms.CharField(label='Confirm new password',
                              widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your new password...'}))

    def clean(self):
        cleanedData = super(EditProfile, self).clean()
        password = cleanedData.get("password")
        confirm = cleanedData.get("confirm")
        logging.debug("Cleaned")
        if password != confirm:
            raise forms.ValidationError("Your passwords don't match.")


class SearchForm(forms.Form):
    Name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    Type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Service Type'}))

    def clean(self):
        cleanedData = super(SearchForm, self).clean()
        Name = cleanedData.get("Name")
        Type = cleanedData.get("Type")

        if not Name and not Type:
            raise forms.ValidationError("You need to enter something to search for a provider")

        try:
            Provider_1622441019.objects.get(name=Name)
        except Provider_1622441019.DoesNotExist:
            try:
                Provider_1622441019.objects.filter(locationtype=Type)[:1].get()
            except Provider_1622441019.DoesNotExist:
                raise forms.ValidationError("No locations match your search")
