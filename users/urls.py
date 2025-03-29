from . import views
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views



app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register' ),
    path('login/', views.login , name='login' ),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/setting/', views.setting, name='setting'),
    path('reviews/<str:username>/', views.reviews_view, name='reviews'),
    path('profile/<str:username>/add-work/', views.add_work, name='add_work'),

        path('password-reset/',
         PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/users/password_change/done/'  # Альтернатива — см. ниже
    ), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),

    path('change_email/', views.change_email, name='change_email'),
    path('change_username/', views.change_username, name='change_username'),
    path('register_done/', views.register_done, name='register_done'),

    
    path('send-feedback/', views.send_feedback, name='send_feedback'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),
    path('maintenance/', views.maintenance_view, name='maintenance'),
    path('toggle-maintenance/', views.toggle_maintenance, name='toggle_maintenance'),
]
