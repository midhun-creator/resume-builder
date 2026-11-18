from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    summary = models.TextField()

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class Education(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="education"
    )

    institution = models.CharField(max_length=150)
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    grade = models.CharField(max_length=50)

    def __str__(self):
        return self.degree


class Experience(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="experience"
    )

    company = models.CharField(max_length=150)
    job_title = models.CharField(max_length=100)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.job_title


class Skill(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    project_url = models.URLField(blank=True)

    def __str__(self):
        return self.title