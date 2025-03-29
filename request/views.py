from django.shortcuts import render, get_object_or_404, redirect
from .models import Request, Comment
from .forms import RequestForm, CommentForm
from django.contrib.auth.decorators import login_required
from users.models import Review
from django.db.models import Q, Avg
from .models import ClientRequest
from .forms import ClientRequestForm
from notifications.models import Notification



def request_list(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "rating")

    # Получаем заявки
    requests = Request.objects.all()

    # Фильтрация по поисковому запросу
    if query:
        requests = requests.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Добавляем средний рейтинг автора
    requests = requests.annotate(avg_rating=Avg("author__received_reviews__rating"))

    # Сортировка
    if sort_by == "newest":
        requests = requests.order_by("-created_at")
    elif sort_by == "oldest":
        requests = requests.order_by("created_at")
    else:  # Сортировка по рейтингу автора
        requests = requests.order_by("-avg_rating")

    return render(request, "request/request_list.html", {"requests": requests, "query": query})


def request_detail(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    comments = request_obj.comments.all()
    form = CommentForm()  # Создаём экземпляр формы

    # Вычисляем средний рейтинг автора заявки
    from users.models import Review
    reviews = Review.objects.filter(user=request_obj.author)
    author_rating = round(sum(r.rating for r in reviews) / reviews.count(), 1) if reviews.exists() else 0

    return render(request, "request/request_detail.html", {
        "request_obj": request_obj,
        "comments": comments,
        "form": form,  # Передаём форму в контекст!
        "author_rating": author_rating
    })

@login_required
def create_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.author = request.user
            new_request.save()
            return redirect("request:request_list")
    else:
        form = RequestForm()

    return render(request, "request/create_request.html", {"form": form})

@login_required
def edit_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id, author=request.user)

    if request.method == "POST":
        form = RequestForm(request.POST, request.FILES, instance=request_obj)
        if form.is_valid():
            form.save()
            return redirect("request:request_detail", request_id=request_obj.id)
    else:
        form = RequestForm(instance=request_obj)

    return render(request, "request/edit_request.html", {"form": form})


@login_required
def add_comment(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.request = request_obj
            comment.save()

            # Создаём уведомление для автора заявки
            Notification.objects.create(
                recipient=request_obj.author, 
                sender=request.user,
                message=f"{request.user.username} оставил комментарий к вашей заявке."
            )
            return redirect("request:request_detail", request_id=request_id)
    else:
        form = CommentForm()

    return render(request, "request/add_comment.html", {"form": form, "request_obj": request_obj})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("request:request_detail", request_id=comment.request.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, "request/edit_comment.html", {"form": form, "comment": comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        request_id = comment.request.id
        comment.delete()
        return redirect("request:request_detail", request_id=request_id)

    return render(request, "request/delete_comment.html", {"comment": comment})


@login_required
def delete_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id, author=request.user)
    request_obj.delete()
    return redirect("request:request_list")



# Список заявок от клиентов
def client_request_list(request):
    sort_by = request.GET.get("sort_by", "newest")
    search_query = request.GET.get("search", "").strip()  # Получаем запрос поиска
    requests = ClientRequest.objects.all()

    # Фильтрация по поисковому запросу
    if search_query:
        requests = requests.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))


    if sort_by == "newest":
        requests = requests.order_by("-created_at")
    elif sort_by == "oldest":
        requests = requests.order_by("created_at")
    else:  # По умолчанию сортируем по рейтингу автора
        requests = sorted(requests, key=lambda r: r.get_author_rating(), reverse=True)

    return render(request, "request/client_request_list.html", {"requests": requests})

# Детальная страница заявки
def client_request_detail(request, request_id):
    request_obj = get_object_or_404(ClientRequest, id=request_id)
    return render(request, "request/client_request_detail.html", {"request_obj": request_obj})

# Создание заявки
def create_client_request(request):
    if request.method == "POST":
        form = ClientRequestForm(request.POST, request.FILES)
        if form.is_valid():
            client_request = form.save(commit=False)
            client_request.author = request.user
            client_request.save()
            return redirect("request:client_request_list")
    else:
        form = ClientRequestForm()
    return render(request, "request/create_client_request.html", {"form": form})


@login_required
def edit_client_request(request, request_id):
    client_request = get_object_or_404(ClientRequest, id=request_id)

    if request.user != client_request.author:
        return redirect("request:client_request_list")  # Если не автор, перенаправляем

    if request.method == "POST":
        form = ClientRequestForm(request.POST, request.FILES, instance=client_request)
        if form.is_valid():
            form.save()
            return redirect("request:client_request_list")
    else:
        form = ClientRequestForm(instance=client_request)

    return render(request, "request/edit_client_request.html", {"form": form})


from django.contrib import messages

@login_required
def delete_client_request(request, request_id):
    client_request = get_object_or_404(ClientRequest, id=request_id)

    if request.user != client_request.author:
        return redirect("request:client_request_list")

    if request.method == "POST":
        client_request.delete()
        messages.success(request, "Заявка успешно удалена.")
        return redirect("request:client_request_list")

    return render(request, "request/delete_client_request.html", {"client_request": client_request})
