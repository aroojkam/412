## formdata/views.py 
## get the form to display as "main" web page for this app:

from django.shortcuts import render

# Create your views here.

def form(request):
    '''Show the web page with the form.'''

    template_name = "formdata/form.html"
    return render(request, template_name)

## edit formdata/views.py: add submit function

def submit(request):
    '''Process the form submission, and generate a result.'''

    template_name = "formdata/confirmation.html"

    # read the form data into python variables:
    if request.POST:

        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color':  favorite_color,
            
        }

    return render(request, template_name, context=context) 