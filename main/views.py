from django.shortcuts import render, redirect


def home(request):
    return render(request, 'main/home.html')

def work(request):
    return render(request, 'main/work.html')


def how_it_works(request):
    return render(request, 'main/how_it_works.html')

def faq(request):
    return render(request, 'main/faq.html')


def yandex(request):
    return render(request, 'main/yandex_20c50dbebd35d885.html')

def open_admin(request):
    return redirect('admin:index')  
# Create your views here.

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)

def permission_denied(request, exception):
    return render(request, '403.html', status=403)


from django.shortcuts import redirect

def switch_theme(request):
    next_url = request.GET.get('next', '/')
    response = redirect(next_url)
    current = request.COOKIES.get('theme', 'light')
    new_theme = 'dark' if current == 'light' else 'light'
    response.set_cookie('theme', new_theme)
    return response
