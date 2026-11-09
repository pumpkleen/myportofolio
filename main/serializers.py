from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description",
            "link", "image",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


# Membuat ModelSerializer untuk model bagianmu di main/serializers.py,
# dengan daftar fields yang ditulis eksplisit(bukan "__all__").

class ExperienceSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.ReadOnlyField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names"
        ]
        read_only_fields = ["id"]

    # Memvalidasi input teks di method validate_<field>,
    # termasuk membersihkannya dengan strip_tags seperti clean_<field> pada Tugas 5.

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_category(self, value):
            return strip_tags(value)

    def validate(self, data):
        started_at = data.get('started_at')
        ended_at = data.get('ended_at')

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError({"ended_at": "Tanggal selesai tidak boleh sebelum tanggal mulai."})
            
        return data

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())