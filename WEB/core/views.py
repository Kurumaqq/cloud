from django.shortcuts import render

def explorer(request, full_path):
    return render(request, 'main.html', {'path': full_path})

def main(request):
    return render(request, 'main.html')
