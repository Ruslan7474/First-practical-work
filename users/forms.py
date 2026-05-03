from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Неверный email или пароль. Проверьте данные и попробуйте снова.",
        "inactive": "Этот аккаунт неактивен. Обратитесь в поддержку.",
    }

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "auth-input", "placeholder": "Введите ваш email", "autocomplete": "email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "auth-input", "placeholder": "Введите ваш пароль", "autocomplete": "current-password"}
        ),
    )


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "auth-input", "placeholder": "Введите ваш email", "autocomplete": "email"}
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "auth-input", "placeholder": "Придумайте пароль", "autocomplete": "new-password"}
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "auth-input", "placeholder": "Повторите пароль", "autocomplete": "new-password"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Регистрация доступна только для адресов @gmail.com.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают.")
        return cleaned

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        return User.objects.create_user(username=email, email=email, password=password)


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "auth-input", "placeholder": "Введите ваш email", "autocomplete": "email"}
        ),
    )
