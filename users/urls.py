from . import views
from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register' ),
    path('login/', views.login , name='login' ),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('reviews/<str:username>/', views.reviews_view, name='reviews'),
    path('profile/<str:username>/add-work/', views.add_work, name='add_work'),

    
    path('send-feedback/', views.send_feedback, name='send_feedback'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),
        path('maintenance/', views.maintenance_view, name='maintenance'),
]
