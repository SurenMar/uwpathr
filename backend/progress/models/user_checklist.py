from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class UserChecklist(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.OneToOneField(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='active_checklist'
  )
  taken_course_credits = models.PositiveSmallIntegerField(blank=True, default=0)
  planned_course_credits = models.PositiveSmallIntegerField(blank=True, default=0)
  specialization = models.ForeignKey(
    'checklists.Specialization',
    on_delete=models.PROTECT,
    related_name='+'
  )
  # TODO Add indexing and ordering for frontend csr


class UserChecklistNode(models.Model):
  pass


class UserAdditionalRequirement(models.Model):
  pass


class UserDepthConstrain(models.Model):
  pass