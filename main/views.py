from django.shortcuts import render

from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Mahi",
        "npm": "2506606093",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mastering in kuru kuru. Sometimes do art sometimes code. Currently focused on game development."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Mahi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    context = {
        "name": "Mahi", 
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)