from .models import Contact, Skill
from rest_framework import serializers


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['skill_name']


class ContactSerializer(serializers.ModelSerializer):
    verified_skills = serializers.SlugRelatedField(
        many=True, 
        slug_field="skill_name", 
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'contact_email', 'min_rate', 'age', 'verified_skills']


class SuggestionSerializer(serializers.ModelSerializer):
    verified_skills = serializers.SlugRelatedField(
        many=True, 
        slug_field="skill_name", 
        queryset=Skill.objects.all()
    )
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'contact_email', 'min_rate', 'age', 'verified_skills', 'score']



