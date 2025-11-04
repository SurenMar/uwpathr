from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

class Course(models.Model):
  CATAGORY_CHOICES = [
    ('math', 'Math'),
    ('cs', 'CS'),
    ('hum', 'Humanities'),
    ('ss', 'Social Sciences'),
    ('ps', 'Pure Sciences'),
    ('as', 'Applied Sciences'),
    ('comm1', 'Communications List 1'),
    ('comm2', 'Communications List 2')
  ]

  code = models.CharField(max_length=10)
  number = models.CharField(max_length=10)
  title = models.TextField(unique=True)
  description = models.TextField()
  units = models.PositiveSmallIntegerField()
  offered_next_term = models.BooleanField(null=True) # Should we have null=True?
  catagory = ArrayField(
    models.CharField(max_length=32, choices=CATAGORY_CHOICES),
    default=list,
    blank=True
  )

  num_uwflow_ratings = models.PositiveSmallIntegerField()
  uwflow_liked_rating = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_easy_ratings = models.PositiveSmallIntegerField(blank=True, null=True)
  uwflow_useful_ratings = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    # Also sorts by code first then number (no need for single column indexes)
    unique_together = ('code', 'number')
    indexes = [GinIndex(fields=['catagory'])]


class CourseRequisite(models.Model):
  pass
