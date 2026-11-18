import io
import zipfile
import textwrap
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse

from .models import Resume, Education, Experience, Skill, Project
from .forms import ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm


# ─── Completion helper ────────────────────────────────────────────────────────

def get_completion(resume):
    """Return an integer 0-100 based on core sections only."""
    if not resume:
        return 0
    steps = [
        bool(resume.full_name and resume.email and resume.phone),
        resume.education.exists(),
        resume.skills.exists(),
    ]
    filled = sum(steps)
    return int((filled / len(steps)) * 100)


# ─── Public views ─────────────────────────────────────────────────────────────

def home(request):
    return render(request, "resume/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Let's build your resume.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "resume/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f"Welcome back, {form.get_user().username}!")
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "resume/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    resume = Resume.objects.filter(user=request.user).first()
    completion = get_completion(resume)
    return render(request, "resume/dashboard.html", {
        "resume": resume,
        "completion": completion,
    })


# ─── Resume (Personal Details) ────────────────────────────────────────────────

@login_required
def resume_create(request):
    resume = Resume.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Personal details saved!")
            if request.POST.get("action") == "continue":
                return redirect("add_education")
            return redirect("dashboard")
    else:
        form = ResumeForm(instance=resume)
    return render(request, "resume/resume_form.html", {"form": form, "resume": resume})


# ─── Education ────────────────────────────────────────────────────────────────

@login_required
def add_education(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.resume = resume
            edu.save()
            messages.success(request, "Education entry added!")
            if request.POST.get("action") == "continue":
                return redirect("add_experience")
            return redirect("add_education")
    else:
        form = EducationForm()
    entries = resume.education.all()
    return render(request, "resume/education_form.html", {
        "form": form, "resume": resume, "entries": entries,
    })


@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, resume__user=request.user)
    edu.delete()
    messages.success(request, "Education entry removed.")
    return redirect("add_education")


@login_required
def edit_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, resume__user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save()
            messages.success(request, "Education entry updated!")
            return redirect("add_education")
    else:
        form = EducationForm(instance=edu)
    return render(request, "resume/edit_education.html", {"form": form})


# ─── Experience ───────────────────────────────────────────────────────────────

@login_required
def add_experience(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.resume = resume
            exp.save()
            messages.success(request, "Experience entry added!")
            if request.POST.get("action") == "continue":
                return redirect("add_skill")
            return redirect("add_experience")
    else:
        form = ExperienceForm()
    entries = resume.experience.all()
    return render(request, "resume/experience_form.html", {
        "form": form, "resume": resume, "entries": entries,
    })


@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, resume__user=request.user)
    exp.delete()
    messages.success(request, "Experience entry removed.")
    return redirect("add_experience")


@login_required
def edit_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, resume__user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience entry updated!")
            return redirect("add_experience")
    else:
        form = ExperienceForm(instance=exp)
    return render(request, "resume/edit_experience.html", {"form": form})


# ─── Skills ───────────────────────────────────────────────────────────────────

@login_required
def add_skill(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            messages.success(request, "Skill added!")
            if request.POST.get("action") == "continue":
                return redirect("add_project")
            return redirect("add_skill")
    else:
        form = SkillForm()
    entries = resume.skills.all()
    return render(request, "resume/skill_form.html", {
        "form": form, "resume": resume, "entries": entries,
    })


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, resume__user=request.user)
    skill.delete()
    messages.success(request, "Skill removed.")
    return redirect("add_skill")


@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, resume__user=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated!")
            return redirect("add_skill")
    else:
        form = SkillForm(instance=skill)
    return render(request, "resume/edit_skill.html", {"form": form})


# ─── Projects ─────────────────────────────────────────────────────────────────

@login_required
def add_project(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.resume = resume
            proj.save()
            messages.success(request, "Project added!")
            if request.POST.get("action") == "continue":
                return redirect("review")
            return redirect("add_project")
    else:
        form = ProjectForm()
    entries = resume.projects.all()
    return render(request, "resume/project_form.html", {
        "form": form, "resume": resume, "entries": entries,
    })


@login_required
def delete_project(request, pk):
    proj = get_object_or_404(Project, pk=pk, resume__user=request.user)
    proj.delete()
    messages.success(request, "Project removed.")
    return redirect("add_project")


@login_required
def edit_project(request, pk):
    proj = get_object_or_404(Project, pk=pk, resume__user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated!")
            return redirect("add_project")
    else:
        form = ProjectForm(instance=proj)
    return render(request, "resume/edit_project.html", {"form": form})


# ─── Review ───────────────────────────────────────────────────────────────────

@login_required
def review(request):
    resume = get_object_or_404(Resume, user=request.user)
    completion = get_completion(resume)
    return render(request, "resume/review.html", {
        "resume": resume,
        "completion": completion,
    })


# ─── Preview ──────────────────────────────────────────────────────────────────

@login_required
def preview(request):
    resume = get_object_or_404(Resume, user=request.user)
    return render(request, "resume/preview.html", {"resume": resume})


# ─── DOCX Export ─────────────────────────────────────────────────────────────

@login_required
def download_docx(request):
    """
    Generate a real .docx file using Python stdlib (zipfile + Open XML).
    No external dependencies required.
    """
    resume = get_object_or_404(Resume, user=request.user)

    def xml_escape(text):
        if not text:
            return ""
        return (str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def para(text, bold=False, size=24, color="000000", space_after=100):
        b_open = "<w:b/>" if bold else ""
        return (
            f'<w:p><w:pPr><w:spacing w:after="{space_after}"/></w:pPr>'
            f'<w:r><w:rPr>{b_open}'
            f'<w:sz w:val="{size}"/><w:color w:val="{color}"/>'
            f'</w:rPr><w:t xml:space="preserve">{xml_escape(text)}</w:t>'
            f'</w:r></w:p>'
        )

    def heading(text, size=32, color="1a1a2e"):
        return (
            f'<w:p><w:pPr>'
            f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="6c63ff"/></w:pBdr>'
            f'<w:spacing w:after="80" w:before="240"/>'
            f'</w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="{size}"/>'
            f'<w:color w:val="{color}"/></w:rPr>'
            f'<w:t>{xml_escape(text)}</w:t></w:r></w:p>'
        )

    def hr():
        return (
            '<w:p><w:pPr>'
            '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="dddddd"/></w:pBdr>'
            '</w:pPr></w:p>'
        )

    # Build document body
    body_parts = []

    # Name header
    body_parts.append(para(resume.full_name, bold=True, size=52, space_after=60))

    # Contact line
    contact_parts = []
    if resume.email:
        contact_parts.append(resume.email)
    if resume.phone:
        contact_parts.append(resume.phone)
    if resume.address:
        contact_parts.append(resume.address)
    if resume.linkedin:
        contact_parts.append(resume.linkedin)
    if resume.github:
        contact_parts.append(resume.github)
    if contact_parts:
        body_parts.append(para(" | ".join(contact_parts), size=20, color="444444", space_after=200))

    # Summary
    if resume.summary:
        body_parts.append(heading("PROFESSIONAL SUMMARY"))
        body_parts.append(para(resume.summary, size=22, space_after=200))

    # Education
    if resume.education.exists():
        body_parts.append(heading("EDUCATION"))
        for edu in resume.education.all():
            title = f"{edu.degree}"
            if edu.field:
                title += f" in {edu.field}"
            body_parts.append(para(title, bold=True, size=24))
            body_parts.append(para(f"{edu.institution}   |   {edu.start_year} – {edu.end_year}",
                                   size=20, color="555555"))
            if edu.grade:
                body_parts.append(para(f"Grade: {edu.grade}", size=20, color="666666"))
            body_parts.append(para("", space_after=120))

    # Experience
    if resume.experience.exists():
        body_parts.append(heading("PROFESSIONAL EXPERIENCE"))
        for exp in resume.experience.all():
            body_parts.append(para(exp.job_title, bold=True, size=24))
            body_parts.append(para(f"{exp.company}   |   {exp.start_date} – {exp.end_date}",
                                   size=20, color="555555"))
            if exp.description:
                for line in exp.description.strip().split("\n"):
                    if line.strip():
                        body_parts.append(para(f"• {line.strip()}", size=22))
            body_parts.append(para("", space_after=120))

    # Projects
    if resume.projects.exists():
        body_parts.append(heading("PROJECTS"))
        for proj in resume.projects.all():
            title = proj.title
            if proj.project_url:
                title += f"  ({proj.project_url})"
            body_parts.append(para(title, bold=True, size=24))
            if proj.technologies:
                body_parts.append(para(f"Technologies: {proj.technologies}", size=20, color="555555"))
            if proj.description:
                body_parts.append(para(proj.description, size=22))
            body_parts.append(para("", space_after=120))

    # Skills
    if resume.skills.exists():
        body_parts.append(heading("SKILLS"))
        skill_text = "  •  ".join(
            f"{s.name} ({s.level})" if s.level else s.name
            for s in resume.skills.all()
        )
        body_parts.append(para(skill_text, size=22))

    body_xml = "\n".join(body_parts)

    # Assemble the docx XML files
    document_xml = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
                    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <w:body>
        {body_xml}
        <w:sectPr>
            <w:pgSz w:w="11906" w:h="16838"/>
            <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080"/>
        </w:sectPr>
        </w:body>
        </w:document>
    """)

    content_types_xml = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
            <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
            <Default Extension="xml" ContentType="application/xml"/>
            <Override PartName="/word/document.xml"
                ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
        </Types>
    """)

    rels_xml = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
            <Relationship Id="rId1"
                Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
                Target="word/document.xml"/>
        </Relationships>
    """)

    word_rels_xml = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
        </Relationships>
    """)

    # Pack into zip buffer
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", rels_xml)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/_rels/document.xml.rels", word_rels_xml)
    buffer.seek(0)

    filename = f"{resume.full_name.replace(' ', '_')}_Resume.docx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response