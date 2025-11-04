from django.db import models

class Checklist(models.Model):
  pass

class ChecklistRequirement(models.Model):
  pass

# Is this needed?
class RequirementAllowedCourses(models.Model):
  pass

# Similar to course requisite logic
class AdditionalConstraint(models.Model):
  pass