from django.urls import path
from .views import request_list, request_detail, create_request, edit_request, delete_request, add_comment, client_request_detail, client_request_list, create_client_request, \
    edit_client_request, delete_client_request, edit_comment, delete_comment, add_to_favorites, remove_from_favorites, favorite_requests, add_to_client_favorites, remove_from_client_favorites, \
        add_client_comment, edit_client_comment, delete_client_comment

app_name = 'request'

urlpatterns = [
    path("request_list", request_list, name="request_list"),
    path("<int:request_id>/", request_detail, name="request_detail"),
    path("create/", create_request, name="create_request"),
    path("<int:request_id>/edit/", edit_request, name="edit_request"),
    path("<int:request_id>/delete/", delete_request, name="delete_request"),
    path("<int:request_id>/comment/", add_comment, name="add_comment"),
    path("<int:request_id>/client_comment/", add_client_comment, name="add_client_comment"),
        path("client-requests/", client_request_list, name="client_request_list"),
    path("client-requests/<int:request_id>/", client_request_detail, name="client_request_detail"),
    path("client-requests/create/", create_client_request, name="create_client_request"),
        path("requests/<int:request_id>/edit/", edit_client_request, name="edit_client_request"),  # Редактирование
    path("requests/<int:request_id>/delete/", delete_client_request, name="delete_client_request"),
    path("comment/<int:comment_id>/edit/", edit_client_comment, name="edit_client_comment"),
    path("comment/<int:comment_id>/delete/", delete_client_comment, name="delete_client_comment"),
    path("client_comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("client_comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path('add_to_favorites/<int:request_id>/', add_to_favorites, name='add_to_favorites'),
    path('add_to_client_favorites/<int:request_id>/', add_to_client_favorites, name='add_to_client_favorites'),
    path('remove_from_favorites/<int:request_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('remove_from_client_favorites/<int:request_id>/', remove_from_client_favorites, name='remove_from_client_favorites'),
    path('favorites/', favorite_requests, name='favorite_requests'),
]
