
from django.shortcuts import render, HttpResponsePermanentRedirect, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserLoginForm, FeedbackForm, UserEmailChangeForm, UserUsernameChangeForm
from django.urls import reverse
from .models import User, Review
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import  WorkForm, ReviewForm, UserProfileForm
from .models import Work, MaintenanceStatus
from django.contrib.auth import update_session_auth_hash 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.backends import ModelBackend

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Явно указываем backend
            login(request, user)
            return redirect('users:register_done')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponsePermanentRedirect('/')
    else:
        form = UserLoginForm()
    context = {'form':form}
    return render(request, 'users/login.html', context)



def logout(request):
    auth.logout(request)
    return HttpResponsePermanentRedirect(reverse('home'))



@login_required
def setting(request, username):
    user = request.user  # просто текущий пользователь

    if request.method == 'POST':
        form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            # Сохраняем профиль пользователя
            user_profile = form.save(commit=False)

            # Обработка смены пароля
            old_pass = request.POST.get('old_pass')
            new_pass = request.POST.get('new_pass')
            confirm_pass = request.POST.get('confirm_new_pass')

            if old_pass and new_pass and confirm_pass:
                if new_pass == confirm_pass:
                    if user.check_password(old_pass):
                        user.set_password(new_pass)
                        user.save()
                        update_session_auth_hash(request, user)  # чтобы не выкинуло из аккаунта
                        messages.success(request, 'Пароль успешно обновлён!')
                    else:
                        messages.error(request, 'Неверный старый пароль.')
                else:
                    messages.error(request, 'Новый пароль и подтверждение не совпадают.')

            # Обновление роли пользователя
            role = request.POST.get('role')
            if role and role != user_profile.role:
                user_profile.role = role

            user_profile.save()  # сохраняем изменения

            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile', username=request.user.username)
        else:
            print("Form errors:", form.errors)
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'users/setting.html', context)


@login_required
def add_work(request, username):
    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.user = request.user
            work.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form = WorkForm()

    return render(request, 'users/add_work.html', {'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    reviews = user.received_reviews.all()
    average_rating = user.get_average_rating()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.user = user
            review.save()
            return redirect('users:profile', username=user.username)
    else:
        form = ReviewForm()

    return render(request, 'users/profile.html', {
        'user': user,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': form
    })


@login_required
def reviews_view(request, username):
    user = get_object_or_404(User, username=username)
    reviews = user.received_reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.user = user
            review.save()
            return redirect('users:reviews', username=user.username)
    else:
        form = ReviewForm()

    return render(request, 'users/reviews.html', {
        'user': user,
        'reviews': reviews,
        'review_form': form,
    })

@login_required
def send_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('users:feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'users/send_feedback.html', {'form': form})

def feedback_success(request):
    return render(request, 'users/feedback_success.html')

def maintenance_view(request):
    return render(request, 'users/maintenance.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_maintenance(request):
    status, created = MaintenanceStatus.objects.get_or_create(id=1)
    status.is_active = not status.is_active
    status.save()
    return redirect('users:profile')  # замените на имя вашего профиля


@login_required
def change_email(request):
    if request.method == 'POST':
        form = UserEmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('users:profile', username=user.username)  # или куда тебе нужно
    else:
        form = UserEmailChangeForm(instance=request.user)

    return render(request, 'users/change_email.html', {'form': form})


@login_required
def change_username(request):
    if request.method == 'POST':
        form = UserUsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('users:profile', username=user.username)  # Передаём username
    else:
        form = UserUsernameChangeForm(instance=request.user)

    return render(request, 'users/change_username.html', {'form': form})




def register_done(request):
    return render(request, 'users/register_done.html')
