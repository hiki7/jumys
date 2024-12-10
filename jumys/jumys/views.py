from django.shortcuts import render

def home_view(request):
    """
    Renders the home page.
    """
    return render(request, 'core/home.html', {'title': 'Home'})
