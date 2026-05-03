from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from barpy_theatre.i18n import normalize_lang
from .forms import EmailAuthenticationForm, RegistrationForm, StyledPasswordResetForm


class StyledPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset.html"
    email_template_name = "auth/password_reset_email.txt"
    subject_template_name = "auth/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = StyledPasswordResetForm


class StyledPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"


class StyledPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class StyledPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    active_tab = request.GET.get("tab", "phone")
    if active_tab not in {"phone", "email"}:
        active_tab = "phone"

    form = EmailAuthenticationForm(request, data=request.POST or None)
    phone_step = False
    phone_display = ""

    if request.method == "POST":
        mode = request.POST.get("mode", "email")
        if mode == "phone":
            dial_code = request.POST.get("dial_code", "").strip()
            phone_number = request.POST.get("phone", "").strip()
            active_tab = "phone"
            phone_step = bool(phone_number)
            if phone_step:
                phone_display = f"{dial_code} {phone_number}".strip()
            else:
                messages.error(request, "Введите номер телефона.")
        elif mode == "phone_verify":
            active_tab = "phone"
            phone_step = True
            dial_code = request.POST.get("dial_code", "").strip()
            phone_number = request.POST.get("phone", "").strip()
            phone_display = f"{dial_code} {phone_number}".strip()
            messages.info(request, "Проверка кода будет подключена следующим шагом.")
        if mode == "email" and form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next") or "home")
        if mode == "email":
            active_tab = "email"

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
            "active_tab": active_tab,
            "phone_step": phone_step,
            "phone_display": phone_display,
        },
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация успешна.")
        return redirect("home")

    return render(request, "auth/register.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")


def set_language_view(request):
    if request.method != "POST":
        return redirect("home")

    lang = normalize_lang(request.POST.get("lang"))
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    request.session["site_lang"] = lang
    response = redirect(next_url)
    response.set_cookie("site_lang", lang, max_age=31536000)
    return response
