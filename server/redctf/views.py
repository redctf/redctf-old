from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def admin_panel(request):

    html = "<html><body>This is the admin panel.</body></html>"
    return HttpResponse(html)

    #  TODO  - lock down view to only super users
    #  TODO  - replicate admin thru templating engine or raw JS/HTML
    #  TODO  - update traefik to route accordingly
    #  TODO  - Stretch goal, return non-super user template to discourage further tampering