from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey


class UserChecklist(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
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


class UserAdditionalConstraints(models.Model):
  pass


class UserDepthList(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='depth_lists' # TODO We might not need this reverse relationship
  )
  courses = models.ManyToManyField(
    'progress.UserCourse', 
    related_name='depth_lists'
  )
  is_chain = models.BooleanField()
  total_units = models.PositiveSmallIntegerField(blank=True, null=True)
  num_courses = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    constraints = [
      models.CheckConstraint(
        check=(
          (Q(is_chain=True) & 
           Q(num_courses__isnull=False) & 
           Q(total_credits__isnull=True))
           |
          (Q(is_chain=False) & 
           Q(num_courses__isnull=True) & 
           Q(total_credits__isnull=False))
        )
      ),
    ]
