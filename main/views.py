from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from main.forms import ProjectForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from main.models import Experience, Project
from .models import Menfess
from .forms import MenfessForm, ExperienceForm
import datetime

def show_main(request):
    menfess_entries = Menfess.objects.all().order_by('-created_at')
    form = MenfessForm()
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
            "name": "Mahi",
            "npm": "2506606093",
            "study_program": "S1 Sistem Informasi",
            "bio": (
                "Mastering in kuru kuru. Sometimes do art sometimes code. Currently focused on game development."
            ),
        "menfess_entries": menfess_entries,
        "form": form,
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        'name': "Mahi",
        'form': ExperienceForm(), 
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Mahi",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

# def show_projects(request):
#     json_response = get_projects_json(request)

#     projects = serializers.deserialize(
#         "json",
#         json_response.content.decode("utf-8"),
#     )
#     projects = [project.object for project in projects]
#     title_query = request.GET.get("title", "").strip()

#     if title_query:
#         projects = [project for project in projects if title_query.lower() in project.title.lower()]

#     is_editor = False
#     if request.user.is_authenticated:
#         is_editor = request.user.groups.filter(name='Editor').exists()

#     context = {
#         "name": "Mahi",
#         "project_list": projects,
#         'is_editor': is_editor,
#         "title_query": title_query,
#     }
#     return render(request, "projects.html", context)

@login_required(login_url="/login/")  # Tambahkan baris ini
def create_project(request):
    # Dua baris berikut yang ditambahkan pada langkah ini.
    # Cek apakah akun yang sedang login adalah superuser (admin/kamu);
    # kalau bukan, hentikan permintaannya dengan 403.
    if not request.user.is_superuser:
        raise PermissionDenied

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

    data = []
    for project in projects:
        image_url = ""
        if hasattr(project, 'image') and project.image:
            try:
                image_url = project.image.url
            except Exception:
                image_url = str(project.image)

        real_star_count = 0
        real_is_starred = False
        stargazer_names = ""

        real_star_count = 0
        real_is_starred = False
        stargazer_names = ""

        if hasattr(project, 'starred_by'):
            real_star_count = project.starred_by.count()
            
            if request.user.is_authenticated:
                real_is_starred = project.starred_by.filter(id=request.user.id).exists()
                
            stargazers = project.starred_by.all()[:3]
            stargazer_names = ", ".join([u.username for u in stargazers])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "link": getattr(project, 'link', ""),
                "image": image_url,
                "star_count": real_star_count,
                "is_starred": real_is_starred,
                "starred_by_names": stargazer_names,
            }
        })
    return JsonResponse(data, safe=False)

# def get_projects_json(request):
#     title_query = request.GET.get("title", "").strip()
#     projects = Project.objects.prefetch_related('starred_by').all()

#     if title_query:
#         projects = projects.filter(title__icontains=title_query)

#     # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
#     data = []
#     for project in projects:
#         starred_users = project.starred_by.all()
#         is_starred = request.user in starred_users if request.user.is_authenticated else False
#         starred_by_names = ", ".join([u.username for u in starred_users])

#         data.append({
#             "pk": str(project.id),
#             "fields": {
#                 "title": project.title,
#                 "description": project.description,
#                 "tech_stack": project.tech_stack,
#                 "project_url": project.project_url,
#                 "project_image_url": project.project_image_url,
#                 "star_count": starred_users.count(),
#                 "is_starred": is_starred,
#                 "starred_by_names": starred_by_names,
#             }
#         })

#     return JsonResponse(data, safe=False)


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by('-started_at')
    
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.get_category_display(), 
                "thumbnail": exp.thumbnail if exp.thumbnail else "",
                "started_at": exp.started_at.strftime("%b %Y") if exp.started_at else "Unknown",
                "ended_at": exp.ended_at.strftime("%b %Y") if exp.ended_at else "Present",
                "is_ongoing": exp.is_ongoing
            }
        })
    return JsonResponse(data, safe=False)

@require_POST
def add_experience_ajax(request):
    # Cek hak akses (Superuser / Editor)
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya admin/pemilik yang dapat menambahkan pengalaman."},
            status=403,
        )
    
    # Masukkan data POST ke dalam form
    form = ExperienceForm(request.POST)
    
    # Validasi form (termasuk anti-XSS strip_tags di forms.py kalau sudah kamu buat)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )
    
    # Jika gagal validasi, kirim pesan error spesifik
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")  # Tambahkan baris ini
def delete_project(request, project_id):
    # Dua baris berikut yang ditambahkan pada langkah ini.
    # Cek apakah akun yang sedang login adalah superuser (admin/kamu);
    # kalau bukan, hentikan permintaannya dengan 403.
    if not request.user.is_superuser:
        raise PermissionDenied

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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Mahi",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Mahi",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)
    
    is_editor = request.user.groups.filter(name='Editor').exists()
    
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None, instance=project)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_projects')
        
    context = {'form': form, 'project': project}
    return render(request, "projects_form.html", context)

def check_admin_or_editor(user):
    return user.is_superuser or user.groups.filter(name='Editor').exists()

@login_required
@user_passes_test(lambda u: u.is_superuser) # Hanya admin yang bisa nambah
def create_experience(request):
    form = ExperienceForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_experience')
    return render(request, "experience_form.html", {'form': form})

@login_required
@user_passes_test(check_admin_or_editor) # Admin & Editor bisa edit
def edit_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, request.FILES or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_experience')
    return render(request, "experience_form.html", {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser) # Hanya admin yang bisa hapus
def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    return redirect('main:show_experience')


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)