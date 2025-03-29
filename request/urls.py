from django.urls import path
from .views import request_list, request_detail, create_request, edit_request, delete_request, add_comment, client_request_detail, client_request_list, create_client_request, \
    edit_client_request, delete_client_request, edit_comment, delete_comment

app_name = 'request'

urlpatterns = [
    path("request_list", request_list, name="request_list"),
    path("<int:request_id>/", request_detail, name="request_detail"),
    path("create/", create_request, name="create_request"),
    path("<int:request_id>/edit/", edit_request, name="edit_request"),
    path("<int:request_id>/delete/", delete_request, name="delete_request"),
    path("<int:request_id>/comment/", add_comment, name="add_comment"),
        path("client-requests/", client_request_list, name="client_request_list"),
    path("client-requests/<int:request_id>/", client_request_detail, name="client_request_detail"),
    path("client-requests/create/", create_client_request, name="create_client_request"),
        path("requests/<int:request_id>/edit/", edit_client_request, name="edit_client_request"),  # Редактирование
    path("requests/<int:request_id>/delete/", delete_client_request, name="delete_client_request"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
]
