from django.db import models
from django.conf import settings

class UserCourse(models.Model):
  COURSE_LIST_CHOICES = [
    ('t', 'Taken'),
    ('p', 'Planned'),
    ('w', 'Wishlist') # Might change name later
  ]

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
  course_list = models.CharField(max_length=10, choices=COURSE_LIST_CHOICES)

  class Meta:
    unique_together = ('user', 'course')

class UserCoursePath(models.Model):
  pass

class UserCoursePathNode(models.Model):
  pass