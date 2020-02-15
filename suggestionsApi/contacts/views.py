from .serializers import ContactSerializer, SkillSerializer, SuggestionSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Contact, Skill

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SuggestionsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = Contact.objects.all()
    serializer_class = SuggestionSerializer

    def get_queryset(self):
        queryset = Contact.objects.all()
        q = self.request.query_params.get('q', None)
        min_rate = self.request.query_params.get('min_rate', None)
        verified_skills = self.request.query_params.get('verified_skills', None)

        filtered_queryset = Contact.objects.none()
        skills_queryset = Contact.objects.none()
        skills_iter = None

        if min_rate:
            queryset = queryset.filter(min_rate__gte=min_rate)
        
        if verified_skills:
            skills_iter = verified_skills.split('_')
            skills_queryset = Contact.objects.none()

            for skill in skills_iter:
                skills_queryset = skills_queryset | queryset.filter(skills__skill_name__icontains=skill)
        
        if q:
            filtered_queryset = Contact.objects.none()

            filtered_queryset = filtered_queryset | queryset.filter(first_name__icontains=q)
            filtered_queryset = filtered_queryset | queryset.filter(last_name__icontains=q)
            filtered_queryset = filtered_queryset | queryset.filter(contact_email__icontains=q)
            
        queryset = (filtered_queryset | skills_queryset).distinct()

        for contact in queryset:
            contact.calculate_score(q, skills_iter, contact.verified_skills.all())

        return queryset
