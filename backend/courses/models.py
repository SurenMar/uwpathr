from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


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
  offered_next_term = models.BooleanField(null=True) # Should we have null=True?
  category = ArrayField(
    models.CharField(max_length=32, choices=COURSE_CATEGORIES),
    default=list,
    blank=True
  )

  title = models.TextField()
  description = models.TextField()
  prerequisite_text = models.TextField()
  corequisite_text = models.TextField()
  antirequisite_text = models.TextField()

  num_uwflow_ratings = models.PositiveSmallIntegerField()
  uwflow_liked_rating = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_easy_ratings = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_useful_ratings = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    # TODO Rework for frontend csr
    # Also sorts by code first then number (no need for single column indexes)
    unique_together = ('code', 'number')
    indexes = [GinIndex(fields=['category'])]

  def save(self, *args, **kwargs):
    self.code = self.code.upper()
    self.number = self.number.upper()
    super().save(*args, **kwargs)


class CourseRequisiteNode(models.Model):
  REQUISITE_TYPES = [
    ('pre', 'Prerequisite'),
    ('co', 'Corequisite'),
    ('anti', 'Antirequisite'),
  ]
  NODE_TYPES = [
    ('group', 'Group'),
    ('course', 'Course'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  requisite_type = models.CharField(max_length=16, choices=REQUISITE_TYPES)
  root_course = models.ForeignKey(
    'Course',
    on_delete=models.CASCADE,
    related_name='req_nodes'
  )
  node_type = models.CharField(max_length=8, choices=NODE_TYPES)
  parent = models.ForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )
  leaf_course = models.ForeignKey( # Only if node_type == course
    'Course',
    blank=True,
    null=True,
    on_delete=models.PROTECT,
    related_name='+'
  )
  num_children_required = models.PositiveSmallIntegerField( # Only if node_type == group
    blank=True, 
    default=0
  )
  depth = models.PositiveSmallIntegerField(blank=True, default=0)

  class Meta:
    indexes = [
      # TODO
      # Rework indexes after knowing how csr will work and whats needed by the frontend
      # Ie we might need to send ALL prerequisites to frontend and do logic there for csr, not here
      # This means we'll only need second index
      models.Index(fields=['root_course', 'requisite_type', 'parent']),
      models.Index(fields=['root_course', 'requisite_type']),
      models.Index(fields=['root_course', 'requisite_type', 'depth']),
    ]

