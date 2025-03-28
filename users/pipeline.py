def save_vk_extra_data(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # Имя, фамилия, email
    user.first_name = response.get('first_name', '')
    user.last_name = response.get('last_name', '')
    user.email = response.get('email', '')

    # Генерация username, если вдруг пустой
    if not user.username:
        user.username = f"vk_{response.get('id')}"

    # Обрезка username, если его длина превышает лимит
    if len(user.username) > 150:  # Обрезаем до 150 символов
        user.username = user.username[:150]

    # Обновление custom_id с уникальным ID от VK
    user.custom_id = str(response.get('id', ''))

    # Обрезка custom_id, если его длина превышает лимит
    if len(user.custom_id) > 300:  # Ограничиваем до 300 символов (если нужно)
        user.custom_id = user.custom_id[:300]

    # Аватарка (если есть фото)
    photo_url = response.get('photo_max_orig')
    if photo_url:
        user.image = photo_url  # Cloudinary сам примет ссылку как путь, это ок

    # Никнейм (если добавил поле nickname в модель)
    if hasattr(user, 'nickname'):
        user.nickname = f"vk_{response.get('id')}"

    try:
        # Сохранение данных
        user.save()
    except Exception as e:
        # Логирование ошибки или дополнительная обработка
        print(f"Ошибка при сохранении пользователя: {e}")
