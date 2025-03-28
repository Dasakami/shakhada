from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('specialist', 'СММщик'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    image = models.ImageField(upload_to='user_images', null=True, blank=True, storage=MediaCloudinaryStorage())
    banner = models.ImageField(upload_to='banners/', blank=True, null=True, storage=MediaCloudinaryStorage())
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_average_rating(self):
        reviews = self.received_reviews.all()
        if reviews.count() > 0:
            total_rating = sum([review.rating for review in reviews])
            return total_rating / reviews.count()
        return 0  # если нет отзывов, возвращаем 0


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('suggestion', 'Предложение'),
        ('complaint', 'Жалоба'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, verbose_name='Тип обращения')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    def __str__(self):
        return f"{self.user.username} — {self.get_feedback_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="works")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="works/images/", storage=MediaCloudinaryStorage(), blank=True, null=True)
    video = models.FileField(upload_to="works/videos/", storage=VideoMediaCloudinaryStorage(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    rating = models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.user.username}"

    class Meta:
        ordering = ['-created_at']



class MaintenanceStatus(models.Model):
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "Технические работы включены" if self.is_active else "Технические работы выключены"

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Техническое обслуживание"
