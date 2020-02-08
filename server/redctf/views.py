from django.http import HttpResponse

def admin_panel(request):

    html = "<html><body>This is the admin panel.</body></html>"
    return HttpResponse(html)