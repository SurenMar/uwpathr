from django.db import models

class Specialization(models.Model):
  name = models.CharField(max_length=255)

class NonCourseRequirement(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
  description = models.TextField()
  checklist = models.ForeignKey(
    'Checklist',
    on_delete=models.CASCADE,
    related_name='non_course_requirements'
  )

# Similar to course requisite logic
class AdditionalConstraint(models.Model):
  pass