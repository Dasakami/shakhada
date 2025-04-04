from django.db import models
from django.conf import settings

from users.models import Review  # Импортируем модель Review
from cloudinary_storage.storage import MediaCloudinaryStorage

class Request(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="request_images/", blank=True, null=True, storage=MediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[("active", "Активна"), ("closed", "Закрыта")],
        default="active",
    )
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def get_author_rating(self):
        """ Получаем средний рейтинг автора заявки из отзывов """
        reviews = Review.objects.filter(user=self.author)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0  # Если отзывов нет, рейтинг = 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # По умолчанию сортировка по дате


class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username}"


class ClientRequest(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="client_request_images/", blank=True, null=True, storage=MediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[("active", "Активна"), ("closed", "Закрыта")],
        default="active",
    )
    contact_info = models.CharField(max_length=255, blank=True, null=True)


    def get_author_rating(self):
        """ Получаем средний рейтинг клиента (по отзывам от специалистов) """
        reviews = Review.objects.filter(user=self.author)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0  # Если отзывов нет, рейтинг = 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

class ClientComment(models.Model):
    client_request = models.ForeignKey(ClientRequest, on_delete=models.CASCADE, related_name='client_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clietn_comment_author')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username}"



class FavoriteRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'request')

class FavoriteClientRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_request = models.ForeignKey(ClientRequest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'client_request')

