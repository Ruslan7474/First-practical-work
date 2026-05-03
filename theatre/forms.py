from django import forms
from .models import Booking, ShowTime


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("showtime", "customer_name", "phone", "email", "seats")
        widgets = {
            "showtime": forms.Select(attrs={"class": "form-control"}),
            "customer_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+996 ..."}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "name@example.com"}
            ),
            "seats": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, play=None, **kwargs):
        super().__init__(*args, **kwargs)
        showtimes = ShowTime.objects.filter(play=play) if play else ShowTime.objects.none()
        showtimes = showtimes.order_by("starts_at")
        self.fields["showtime"].queryset = showtimes
        self.fields["showtime"].label = "Выберите показ"

    def clean(self):
        cleaned_data = super().clean()
        showtime = cleaned_data.get("showtime")
        seats = cleaned_data.get("seats") or 0
        if showtime and seats > showtime.available_seats:
            self.add_error(
                "seats",
                f"Доступно только {showtime.available_seats} мест на выбранный показ.",
            )
        return cleaned_data
