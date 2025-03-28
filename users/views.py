
from django.shortcuts import render, HttpResponsePermanentRedirect, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserLoginForm, FeedbackForm
from django.urls import reverse
from .models import User, Review
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, WorkForm, ReviewForm
from .models import Work

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # поменяй на свою главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
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
def edit_profile(request, username):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=request.user.username)  # Убедись, что передаёшь username
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})


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
