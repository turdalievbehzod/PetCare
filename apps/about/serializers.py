from rest_framework import serializers

from apps.about.models import AboutPage, TeamMember, Testimonial


class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ["id", "uuid", "name", "title", "photo_url", "bio", "order"]

    def get_photo_url(self, obj):
        if obj.photo and obj.photo.file:
            request = self.context.get("request")
            url = obj.photo.file.url
            return request.build_absolute_uri(url) if request else url
        return None


class TeamMemberWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["name", "title", "photo", "bio", "order", "is_active"]


class TestimonialSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ["id", "uuid", "name", "text", "avatar_url", "rating", "order"]

    def get_avatar_url(self, obj):
        if obj.avatar and obj.avatar.file:
            request = self.context.get("request")
            url = obj.avatar.file.url
            return request.build_absolute_uri(url) if request else url
        return None


class TestimonialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["name", "text", "avatar", "rating", "order", "is_active"]


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = [
            "id",
            "uuid",
            "mission_title",
            "mission_content",
            "vision_title",
            "vision_content",
            "commitment_title",
            "commitment_description",
            "stat1_value",
            "stat1_label",
            "stat2_value",
            "stat2_label",
            "years_experience",
            "appointments_count",
        ]


class AboutPageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = [
            "mission_title",
            "mission_content",
            "vision_title",
            "vision_content",
            "commitment_title",
            "commitment_description",
            "stat1_value",
            "stat1_label",
            "stat2_value",
            "stat2_label",
            "years_experience",
            "appointments_count",
            "is_active",
        ]
