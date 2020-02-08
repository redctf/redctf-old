from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def admin_panel(request):

    html = "<html><body>This is the admin panel.</body></html>"
    return HttpResponse(html)