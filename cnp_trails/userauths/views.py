# from django.shortcuts import render,redirect
# from userauths.models import User, Profile
# from userauths.forms import UserRegisterForm
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.utils.crypto import get_random_string
# from userauths.forms import LoginForm
# from django.conf import settings

# # Create your views here.

# def RegisterView(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "You are already logged in.")
#         return redirect("activity:index")

#     form = UserRegisterForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         password = form.cleaned_data.get("password1")
#         user.set_password(password)

#         otp = get_random_string(length=6, allowed_chars='0123456789')
#         user.otp = otp
#         user.save()

#         send_mail(
#         subject='Your OTP for registration',
#         message=f'Hello {user.full_name}, your OTP is {otp}',
#         from_email=None,  # uses DEFAULT_FROM_EMAIL
#         recipient_list=[user.email],
#         fail_silently=False,
#         )

#         messages.info(request, f"An OTP has been sent to {user.email}.")
#         request.session['email'] = user.email  # store email temporarily for OTP verification
#         return redirect("userauths:verify-otp")

#         # user_auth = authenticate(email=user.email, password=password)
#         # login(request, user_auth)

#         # # update profile
#         # profile = user.profile
#         # profile.full_name = form.cleaned_data.get("full_name")
#         # profile.phone = form.cleaned_data.get("phone")
#         # profile.save()

#         # messages.success(request, f"Hey {user.full_name}, your account has been created successfully.")
#         # return redirect("activity:index")

#     context = {"form": form}
#     return render(request, "userauths/sign-up.html", context)

# def verify_otp_view(request):
#     email = request.session.get('email')

#     if not email:
#         messages.error(request, "Session expired. Please register again.")
#         return redirect("userauths:sign-up")

#     if request.method == "POST":
#         entered_otp = request.POST.get("otp")
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, "User not found. Please register again.")
#             return redirect("userauths:sign-up")

#         if user.otp == entered_otp:
#             user.otp = None  # clear OTP once verified
#             user.save()

#             # Update profile info
#             profile = user.profile
#             profile.full_name = user.full_name
#             profile.phone = user.phone
#             profile.save()

#             # Log in user
#             login(request, user)
#             messages.success(request, f"Welcome {user.full_name}, your account is verified and you are now logged in.")
#             return redirect("activity:index")
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")
#             return redirect("userauths:verify-otp")

#     return render(request, "userauths/verify_otp.html")

# def resend_otp_view(request):
#     email = request.session.get('email')

#     if not email:
#         messages.error(request, "Session expired. Please register again.")
#         return redirect("userauths:sign-up")

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         messages.error(request, "User not found. Please register again.")
#         return redirect("userauths:sign-up")

#     # Generate and save new OTP
#     otp = get_random_string(length=6, allowed_chars='0123456789')
#     user.otp = otp
#     user.save()

#     # Send OTP email
#     send_mail(
#         subject='Your OTP for Registration',
#         message=f'Hello {user.full_name}, your OTP is {otp}',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[user.email],
#         fail_silently=False,
#     )

#     messages.success(request, f"A new OTP has been sent to {user.email}.")
#     return redirect("userauths:verify-otp")

# # Login model
# def loginViewTemp(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "You are already logged in")
#         return redirect("activity:index")

#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = form.cleaned_data['user']
#             login(request, user)
#             messages.success(request, "You are Logged In")
#             next_url = request.GET.get("next", "activity:index")
#             return redirect(next_url)
#     else:
#         form = LoginForm()

#     context = {"form": form}
#     return render(request, "userauths/sign-in.html", context)



# # logout views

# def LogoutView(request):
#     logout(request)
#     messages.success(request,"You have been Logged Out")
#     return redirect("userauths:sign-in")
# 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from userauths.models import User, Profile
from userauths.forms import UserRegisterForm, LoginForm
from .forms import UserInfoUpdateForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("activity:index")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        # Temporarily store user data in session (not saving user yet)
        request.session['register_data'] = form.cleaned_data

        email = form.cleaned_data.get("email")
        full_name = form.cleaned_data.get("full_name")

        otp = get_random_string(length=6, allowed_chars='0123456789')
        request.session['otp'] = otp
        request.session['email'] = email

        # Send OTP
        send_mail(
            subject='Your OTP for Registration',
            message=f'Hello {full_name}, your OTP is {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.info(request, f"An OTP has been sent to {email}.")
        return redirect("userauths:verify-otp")

    return render(request, "userauths/sign-up.html", {"form": form})


def verify_otp_view(request):
    email = request.session.get('email')
    otp = request.session.get('otp')
    data = request.session.get('register_data')

    if not all([email, otp, data]):
        messages.error(request, "Session expired. Please register again.")
        return redirect("userauths:sign-up")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if entered_otp == otp:
            # Create actual user only after OTP verification
            user = User(
                username=data["username"],
                email=data["email"],
                full_name=data["full_name"],
                phone=data["phone"],
            )
            user.set_password(data["password1"])
            user.save()

            # Clear OTP session
            for key in ['otp', 'email', 'register_data']:
                if key in request.session:
                    del request.session[key]

            # Create / update profile
            profile = user.profile
            profile.full_name = user.full_name
            profile.phone = user.phone
            profile.save()

            # Log in user
            login(request, user)
            messages.success(request, f"Welcome {user.full_name}, your account has been verified and created successfully.")
            return redirect("activity:index")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("userauths:verify-otp")

    return render(request, "userauths/verify_otp.html")


def resend_otp_view(request):
    email = request.session.get('email')
    otp = get_random_string(length=6, allowed_chars='0123456789')

    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect("userauths:sign-up")

    request.session['otp'] = otp

    send_mail(
        subject='Your OTP for Registration',
        message=f'Your new OTP is {otp}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(request, f"A new OTP has been sent to {email}.")
    return redirect("userauths:verify-otp")


def loginViewTemp(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("activity:index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, "You are Logged In")
            return redirect(request.GET.get("next", "activity:index"))
    else:
        form = LoginForm()

    return render(request, "userauths/sign-in.html", {"form": form})


def LogoutView(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect("userauths:sign-in")


@login_required
def profile_update(request):
    user = request.user
    info_message = None
    password_message = None

    # POST: update profile info
    if request.method == 'POST':
        if 'save_info' in request.POST:
            user_form = UserInfoUpdateForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user=user)

            if user_form.is_valid():
                user_form.save()
                info_message = user_form.success_message
            

        elif 'change_password' in request.POST:
            user_form = UserInfoUpdateForm(instance=user)
            password_form = PasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                password_message = password_form.success_message
           
    else:
        user_form = UserInfoUpdateForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'userauths/profile-update.html', {
        'user_form': user_form,
        'password_form': password_form,
        'info_message': info_message,
        'password_message': password_message,
    })