from django.shortcuts import render

# Create your views here.
def rules_list(request):
    return render(request, 'rules_list.html')
