from rest_framework import serializers

from apps.contact.models import ContactInfo, ContactInquiry


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "phone", "subject", "message"]


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ["id", "address", "phone", "email", "working_hours", "map_embed_url"]
