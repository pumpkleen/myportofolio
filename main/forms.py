from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, Select

from main.models import Project, Menfess, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "link",
            "image",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "link": "URL Proyek",
            "image": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "masukkan URL proyekmu",
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "masukkan URL gambar proyekmu",
                }
            ),
        }

class ExperienceForm(ModelForm):
    started_at = forms.DateField(
        widget=forms.DateInput(attrs={"type": "month"}),
        input_formats=['%Y-%m'],
        required=False,
        label="Bulan Mulai"
    )
    ended_at = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "month", 
                "title": "Kosongkan jika masih berlangsung"
            }
        ),
        input_formats=['%Y-%m'],
        required=False,
        label="Bulan Selesai"
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "category",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman / Posisi",
            "category": "Kategori",
            "description": "Deskripsi",
            "thumbnail": "URL Thumbnail (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Teaching Assistant of Discrete Mathematics",
                    "maxlength": 255,
                }
            ),
            "category": Select(
                attrs={
                    "style": "padding: 5px; border-radius: 5px;"
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan tugas dan pengalamanmu...",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://link-ke-gambar-kamu.com/image.png",
                }
            ),
        }

        

class MenfessForm(ModelForm):
    class Meta:
        model = Menfess
        fields = ["sender", "message", "image"]