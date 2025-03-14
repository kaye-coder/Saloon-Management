from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def landing_page(request):
    """
    This view renders the landing page.
    It requires the user to be logged in.
    """
    return render(request, 'landing/index.html')
