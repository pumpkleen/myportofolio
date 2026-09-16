from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

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
                    "placeholder": "https://mir4na.itch.io/where-do-you-belong",
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=1NOtJJOOoPDyvS-uT9z2Q6T0GBPsldz2-&sz=w1000",
                }
            ),
        }