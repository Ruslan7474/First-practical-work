from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Booking, HomeShowcaseItem, Play, SeatReservation, ShowcaseCategory, ShowTime


class PlayAdminForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = "__all__"

    def clean_description(self):
        value = self.cleaned_data.get("description", "")
        text = strip_tags(value or "").replace("\xa0", " ").replace("&nbsp;", " ").strip()
        if not text:
            raise ValidationError("Добавьте описание спектакля, оно не может быть пустым.")
        return value


class ShowTimeInline(admin.TabularInline):
    model = ShowTime
    extra = 1
    fields = ("starts_at", "hall", "price")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    form = PlayAdminForm
    list_display = ("title", "categories_label", "duration_minutes", "age_limit", "created_at")
    list_filter = ("categories", "age_limit", "created_at")
    search_fields = ("title", "categories__name", "cast", "director")
    filter_horizontal = ("categories",)
    inlines = (ShowTimeInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    ("poster", "poster_url"),
                    "categories",
                    ("duration_minutes", "age_limit"),
                    ("director", "hall"),
                    "cast",
                    "premiere_date",
                )
            },
        ),
    )


@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ("play", "starts_at", "hall", "price")
    list_filter = ("hall", "starts_at")
    search_fields = ("play__title", "play__categories__name")
    autocomplete_fields = ("play",)
    fields = ("play", "starts_at", "hall", "price")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "showtime", "seats", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer_name", "phone", "email")


@admin.register(SeatReservation)
class SeatReservationAdmin(admin.ModelAdmin):
    list_display = ("showtime", "row_number", "seat_number", "created_at")
    list_filter = ("showtime", "created_at")
    search_fields = ("showtime__play__title",)


@admin.register(HomeShowcaseItem)
class HomeShowcaseItemAdmin(admin.ModelAdmin):
    list_display = ("play", "display_date", "order", "is_active", "created_at")
    list_filter = ("is_active", "display_date", "created_at")
    list_editable = ("order", "is_active")
    search_fields = ("play__title", "play__categories__name")
    autocomplete_fields = ("play",)
    filter_horizontal = ("categories",)
    fields = ("play", ("image", "image_url"), "categories", "display_date", "order", "is_active")


@admin.register(ShowcaseCategory)
class ShowcaseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name",)
