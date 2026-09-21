from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.forms import ProjectForm
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Project
from .models import Menfess
from .forms import MenfessForm

def show_main(request):
    menfess_entries = Menfess.objects.all().order_by('-created_at')
    form = MenfessForm()
    context = {
        "name": "Mahi",
        "npm": "2506606093",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mastering in kuru kuru. Sometimes do art sometimes code. Currently focused on game development."
        ),
        "menfess_entries": menfess_entries,
        "form": form,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Mahi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Mahi",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Mahi",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def show_menfess(request):
    menfess_entries = Menfess.objects.all().order_by('-created_at')
    form = MenfessForm()
    context = {
        "name": "Mahi",
        "menfess_entries": menfess_entries,
        "form": form,
    }
    return render(request, "menfess.html", context)

def create_menfess(request):
    form = MenfessForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Menfess baru berhasil dikirim!")
        return redirect("main:show_menfess")
    
    context = {
        "name": "Mahi",
        "form": form,
    }
    return render(request, "create_menfess.html", context)


def edit_menfess(request, id):
    menfess = get_object_or_404(Menfess, pk=id)
    form = MenfessForm(request.POST or None, request.FILES or None, instance=menfess)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Menfess berhasil diubah!")
        return redirect("main:show_menfess")
    
    context = {
        "name": "Mahi",
        "form": form,
    }
    return render(request, "edit_menfess.html", context)


def delete_menfess(request, id):
    menfess = get_object_or_404(Menfess, pk=id)

    if request.method == "POST":
        menfess.delete()
        messages.success(request, "Menfess berhasil dihapus!")
        return redirect("main:show_menfess")
    
    return redirect("main:show_menfess")

def show_json_menfess(request):
    data = Menfess.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


