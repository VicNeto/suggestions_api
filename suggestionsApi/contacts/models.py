from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_email = models.EmailField(unique=True)
    min_rate = models.CharField(max_length=50)
    age = models.IntegerField()
    score = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['score', 'id']

    def calculate_score(self, q, query_skills, skills):
        rate = 0
        skills = [sk.skill_name for sk in skills]

        # Weight of 30%
        if query_skills:
            total = 0
            skills = (' '.join(skills)).lower()
            for query_skill in query_skills:
                total += 1 if skills.find(query_skill.lower()) >= 0 else 0
                
            rate += (total/len(query_skills)) * 0.3
            
        # weight of 70%
        if q:
            total = 0
            data = f'{self.first_name} {self.last_name} {self.contact_email}'.lower()
            total += data.count(q.lower())
                
            rate += (total/4) * 0.7
            
        self.score = rate
        


class Skill(models.Model):
    contact = models.ManyToManyField(Contact, related_name="verified_skills", related_query_name="skills")
    skill_name = models.CharField(max_length=300)

    class Meta:
        ordering = ['skill_name']

    def __str__(self):
        return self.skill_name
