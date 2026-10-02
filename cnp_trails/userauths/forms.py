from django import forms
import re
from userauths.models import User, Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation


class UserRegisterForm(forms.ModelForm):
    full_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Full Name",'class':"fullname"}), required=True,error_messages={'required': "Full name cannot be empty."})
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':" Username",'class':"username"}), required=True,error_messages={'required': "Username  cannot be empty."})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email",'class':"email"}) ,error_messages={'required': "Email cannot be empty.",'unique': "This email is already registered. Please use another one."})
    phone= forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Phone No",'class':"phone"}),required=True,error_messages={'required': "Phone Number cannot be empty."})
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':"password1"}),required=True,error_messages={'required': "Password cannot be empty."})
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm_password ",'class':"password2"}),required=True,error_messages={'required': "Confirm Password cannot be empty."})
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""          
            field.help_text = None    

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")


        if not full_name:
            raise forms.ValidationError("Full  name cannot be empty.")

    
        if not all(char.isalpha() or char.isspace() for char in full_name):
            raise forms.ValidationError("Full name must contain only letters.")

        return full_name

    def clean_username(self):
        username = self.cleaned_data.get("username")

    # Check if empty
        if not username:
            raise forms.ValidationError("Username cannot be empty.")

    # Allow only alphanumeric characters (no dots or special symbols)
        if not username.isalnum():
            raise forms.ValidationError("Username must contain only letters and numbers (no special characters).")

    # Check uniqueness

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another one.")

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

    # Check if empty
        if not email:
            raise forms.ValidationError("Email cannot be empty.")

    # Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

    # Check uniqueness
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use another one.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

    # Check if empty
        if not phone:
            raise forms.ValidationError("Phone number cannot be empty.")

    # Allow only digits and must be 10 digits long
        if not re.fullmatch(r"\d{10}", phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number (digits only).")

    # Check uniqueness
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")

        return phone

    def clean_password1(self):
       
        password1 = self.cleaned_data.get("password1")
        

    # Check if passwords are empty
        if not password1:
            raise forms.ValidationError(" password fields are required.")

    # Check if passwords match
        

    # Check password strength
        errors = []

        if len(password1) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", password1):
            errors.append("a uppercase letter")
        if not re.search(r"[0-9]", password1):
            errors.append("a number")
        if not re.search(r"[@$!%*?&]", password1):
            errors.append("a special character (@, $, !, %, *, ?, &)")
    
        if errors:
            raise forms.ValidationError("Password must contain " + ", ".join(errors) + ".")
     

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
         raise forms.ValidationError("Passwords do not match.")
        return password2



    
    class Meta:
        model=User
        fields=['full_name','username','email','phone','password1','password2']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True,error_messages={'required': "Email cannot be empty."})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True,error_messages={'required': "Password cannot be empty."})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User with this email does not exist.")

            user_auth = authenticate(email=email, password=password)
            if not user_auth:
                raise forms.ValidationError("Incorrect email or password.")

            # Attach user object to form for use in view
            cleaned_data['user'] = user_auth

        return cleaned_data
    

# UPDATE FORMS

from django import forms
from userauths.models import User

class UserInfoUpdateForm(forms.ModelForm):
    success_message = ""
    error_message = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""
            field.help_text = None
            field.required = True  # make all fields required

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'fullname','placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'email','placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'phone','placeholder': 'Phone Number'}),
       }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional
        for field in self.fields.values():
            field.required = False

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")


        if not full_name:
            raise forms.ValidationError("Full  name can't be empty.")

    
        if not all(char.isalpha() or char.isspace() for char in full_name):
            raise forms.ValidationError("Full name must contain only letters.")

        return full_name
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

    # Check if empty
        if not email:
            raise forms.ValidationError("Email cannot be empty.")

    # Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

    # Check uniqueness
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already registered with another account.")

        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

    # Check if empty
        if not phone:
            raise forms.ValidationError("Phone number cannot be empty.")

    # Allow only digits and must be 10 digits long
        if not re.fullmatch(r"\d{10}", phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number (digits only).")

    # Check uniqueness
        if User.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This phone number is already registered with another account.")

        return phone

    

    def save(self, commit=True):
        try:
            instance = super().save(commit=commit)
            self.success_message = "Profile information updated successfully."
            return instance
        except Exception:
            self.error_message = "An unexpected error occurred while updating your profile."
            return None



class PasswordChangeForm(forms.Form):
    success_message = ""
    error_message = ""

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'old_password', 'placeholder': 'Current Password'}),required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'new_password1', 'placeholder': 'New Password'}),required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'new_password2', 'placeholder': 'Confirm New Password'}),required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    # def is_valid(self):
    #     valid = super().is_valid()
    #     if not valid:
    #         self.error_message = "Please fill all password fields correctly."
    #     return valid

    def clean_old_password(self):
        old_password=self.cleaned_data.get("old_password")

        if not old_password:
            raise forms.ValidationError("Please, give your current password")
        
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your current password is incorrect.")
        
        return old_password
    
    def clean_new_password1(self):

        new_password1=self.cleaned_data.get("new_password1")

        if not new_password1:
            raise forms.ValidationError("Please, give your new password")
        
        errors = []

        if len(new_password1) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", new_password1):
            errors.append("a uppercase letter")
        if not re.search(r"[0-9]", new_password1):
            errors.append("a number")
        if not re.search(r"[@$!%*?&]", new_password1):
            errors.append("a special character (@, $, !, %, *, ?, &)")
    
        if errors:
            raise forms.ValidationError("Password must contain " + ", ".join(errors) + ".")
        
        return new_password1
    

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
         raise forms.ValidationError("Passwords do not match.")
        return new_password2



    

    def save(self):
        new_password = self.cleaned_data.get("new_password1")
        self.user.set_password(new_password)
        self.user.save()
        self.success_message = "Password changed successfully."