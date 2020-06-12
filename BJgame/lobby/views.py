from django.shortcuts import render, redirect


def render_lobby(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return render(request, "lobby.html")

def howto(request):
    return render(request, 'howto.html')

def services(request):
    return render(request, 'services.html')

def strategy(request):
    return render(request, 'strategy.html')

def other(request):
    return render(request, 'other.html')