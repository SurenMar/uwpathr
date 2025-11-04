from django.db import models
from django.conf import settings

class UserCourse(models.Model):
  COURSE_LIST_TYPES = [
    ('taken', 'Taken'),
    ('planned', 'Planned'),
    ('wishlist', 'Wishlist'), # Might change name later
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='courses'
  )
  course = models.ForeignKey(
    'courses.Course',
    on_delete=models.CASCADE, # Might change later
    related_name='+'
  )
  course_list = models.CharField(max_length=16, choices=COURSE_LIST_TYPES)

  class Meta:
    # TODO Rework for frontend csr
    unique_together = ('user', 'course')

class UserCoursePath(models.Model):
  pass

class UserCoursePathNode(models.Model):
  pass