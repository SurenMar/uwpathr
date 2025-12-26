from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from mptt.models import MPTTModel, TreeForeignKey


class Course(models.Model):
  COURSE_CATEGORIES = [
    ('math', 'Math'),
    ('cs', 'CS'),
    ('hum', 'Humanities'),
    ('ss', 'Social Sciences'),
    ('ps', 'Pure Sciences'),
    ('as', 'Applied Sciences'),
    ('comm1', 'Communications List 1'),
    ('comm2', 'Communications List 2'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  code = models.CharField(max_length=8)
  number = models.CharField(max_length=8)
  units = models.PositiveSmallIntegerField()
  category = ArrayField(
    models.CharField(max_length=32, choices=COURSE_CATEGORIES),
    default=list,
    blank=True,
  )
  corequisites = ArrayField(
    models.CharField(max_length=16),
    default=list,
    blank=True,
  )
  antirequisites = ArrayField(
    models.CharField(max_length=16),
    default=list,
    blank=True,
  )
  title = models.TextField()
  description = models.TextField()
  num_uwflow_ratings = models.PositiveSmallIntegerField()
  uwflow_liked_rating = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_easy_ratings = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_useful_ratings = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    # Also sorts by code first then number (no need for seperate composite index)
    unique_together = ('code', 'number')
    indexes = [GinIndex(fields=['category'])]

  def save(self, *args, **kwargs):
    self.code = self.code.upper()
    self.number = self.number.upper()
    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.code}{self.number}"


class CoursePrerequisiteNode(MPTTModel):
  NODE_TYPES = [
    ('group', 'Group'),
    ('course', 'Course'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  target_course = models.ForeignKey(
    'Course',
    on_delete=models.CASCADE,
    related_name='prerequisite_nodes'
  )
  node_type = models.CharField(max_length=8, choices=NODE_TYPES)
  parent = TreeForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )
  leaf_course = models.ForeignKey(
    'Course',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='+'
  )
  num_children_required = models.PositiveSmallIntegerField(blank=True, null=True)
  
  class Meta:
    indexes = [
      models.Index(fields=['target_course', 'parent'])
    ]
    constraints = [
      models.CheckConstraint(
        check=(
          (Q(node_type='course') &
           Q(leaf_course__isnull=False) & 
           Q(num_children_required__isnull=True)) 
           |
          (Q(node_type='group') & 
           Q(leaf_course__isnull=True) & 
           Q(num_children_required__isnull=False))
        ),
        name='courses_are_leafs_and_groups_are_nodes'
      ),
    ]
  
  class MPTTMeta:
    order_insertion_by = ['leaf_course']


