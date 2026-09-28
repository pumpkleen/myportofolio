from django.urls import path
from main.views import (show_main,
                        show_experience,
                        show_projects,
                        show_menfess,
                        create_project, get_projects_json,
                        delete_project, create_menfess, 
                        edit_menfess, delete_menfess, 
                        show_json_menfess, register, 
                        login_user, logout_user,
                        toggle_star,
                        )

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path('menfess/', show_menfess, name='show_menfess'),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path('create-menfess/', create_menfess, name='create_menfess'),
    path('edit-menfess/<uuid:id>/', edit_menfess, name='edit_menfess'),
    path('delete-menfess/<uuid:id>/', delete_menfess, name='delete_menfess'),
    path('json-menfess/', show_json_menfess, name='show_json_menfess'),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
    "projects/<uuid:project_id>/star/",
    toggle_star,
    name="toggle_star",
),
]