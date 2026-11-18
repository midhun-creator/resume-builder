from django import forms
from .models import Resume, Education, Experience, Skill, Project


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ["user"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. John Smith"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "your@email.com"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "+1 234 567 8900"
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "City, Country"
            }),
            "summary": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "A brief professional summary highlighting your key strengths and goals..."
            }),
            "linkedin": forms.URLInput(attrs={
                "class": "form-control", "placeholder": "https://linkedin.com/in/yourprofile"
            }),
            "github": forms.URLInput(attrs={
                "class": "form-control", "placeholder": "https://github.com/yourusername"
            }),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["resume"]
        widgets = {
            "institution": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "University / College name"
            }),
            "degree": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Bachelor of Science"
            }),
            "field": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Computer Science"
            }),
            "start_year": forms.NumberInput(attrs={
                "class": "form-control", "placeholder": "2020"
            }),
            "end_year": forms.NumberInput(attrs={
                "class": "form-control", "placeholder": "2024"
            }),
            "grade": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. 3.8 GPA / First Class"
            }),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ["resume"]
        widgets = {
            "company": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Company or Organisation name"
            }),
            "job_title": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Software Developer"
            }),
            "start_date": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Jun 2022"
            }),
            "end_date": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Present"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Describe your key responsibilities and achievements..."
            }),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ["resume"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Python"
            }),
            "level": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Advanced"
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["resume"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Project name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "What the project does, your role, and what you achieved..."
            }),
            "technologies": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "e.g. Django, React, PostgreSQL"
            }),
            "project_url": forms.URLInput(attrs={
                "class": "form-control", "placeholder": "https://github.com/... (optional)"
            }),
        }