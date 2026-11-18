from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("resume/", views.resume_create, name="resume_create"),

    path("education/", views.add_education, name="add_education"),
    path("education/edit/<int:pk>/", views.edit_education, name="edit_education"),
    path("education/delete/<int:pk>/", views.delete_education, name="delete_education"),

    path("experience/", views.add_experience, name="add_experience"),
    path("experience/edit/<int:pk>/", views.edit_experience, name="edit_experience"),
    path("experience/delete/<int:pk>/", views.delete_experience, name="delete_experience"),

    path("skill/", views.add_skill, name="add_skill"),
    path("skill/edit/<int:pk>/", views.edit_skill, name="edit_skill"),
    path("skill/delete/<int:pk>/", views.delete_skill, name="delete_skill"),

    path("project/", views.add_project, name="add_project"),
    path("project/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("project/delete/<int:pk>/", views.delete_project, name="delete_project"),

    path("review/", views.review, name="review"),
    path("preview/", views.preview, name="preview"),
    path("download/docx/", views.download_docx, name="download_docx"),
]