from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test
from django.template import loader


from .forms import CreateChallenge

@xframe_options_exempt
def _form_view(request, template_name='admin.html', form_class=CreateChallenge):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = form_class()
    return render(request, template_name, {'form': form})

@xframe_options_exempt
def basic(request):
    return _form_view(request)











# @user_passes_test(lambda u: u.is_superuser)
# @xframe_options_exempt
# def admin_panel(request):



#     html = """
#     <html>
#     	<body>This is the admin panel.

#     		<button onclick=""/>

#     	</body>
#     </html>
#     """
#     return HttpResponse(html)

#     #  TODO  - lock down view to only super users
#     #  TODO  - replicate admin thru templating engine or raw JS/HTML
#     #  TODO  - update traefik to route accordingly
#     #  TODO  - Stretch goal, return non-super user template to discourage further tampering
