from django.db import models, transaction
from treebeard.mp_tree import MP_Node
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
    indexes = [
      models.Index(fields=['user', 'course_list'])
    ]
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'course'], 
        name='unique_course_per_user'
      )
    ]


class UserCoursePathNode(MP_Node):
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
  prerequisite_node = models.ForeignKey(
    'courses.CoursePrerequisiteNode',
    on_delete=models.CASCADE, 
    related_name='user_paths'
  )

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'target_course'], 
        name='unique_target_course_per_user'
      )
    ]
    indexes = [
      models.Index(fields=['user', 'target_course', 'path']),
      models.Index(fields=['user', 'target_course', 'depth']),
    ]
