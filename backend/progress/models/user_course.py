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
    # TODO Rework indexes for frontend csr
    unique_together = ('user', 'course')

class UserCoursePathNode(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='course_paths'
  )
  target_course = models.ForeignKey(
    'UserCourse',
    on_delete=models.CASCADE,
    related_name='paths'
  )
  requisite_node = models.ForeignKey(
    'courses.CourseRequisiteNode',
    on_delete=models.PROTECT, # Course requisites and paths should be fully updated before any removed courses are deleted
    related_name='+'
  )
  child = models.OneToOneField(
    'self',
    blank=True,
    null=True,
    on_delete=models.SET_NULL,
    related_name='parent'
  )
  depth = models.PositiveSmallIntegerField()

  class Meta:
    # TODO Rework indexes for frontend csr
    unique_together = ('user', 'target_course')
    indexes = [
      models.Index(fields=['user', 'target_course', 'parent']),
      models.Index(fields=['user', 'target_course', 'depth']), # Might not need this
    ]
