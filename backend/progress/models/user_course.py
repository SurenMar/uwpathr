from django.db import models, transaction
from django.db.models import Q
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
  prereqs_met = models.BooleanField(blank=True, null=True)

  class Meta:
    indexes = [
      models.Index(fields=['user', 'course_list'])
    ]
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'course'], 
        name='unique_course_per_user'
      ),
      models.CheckConstraint(
        check=(
          ~Q(course_list='taken') | Q(prereqs_met__isnull=True)
        ),
        name='taken_courses_have_null_prereqs_met'
      )
    ]

  def __str__(self):
    return str(self.course)


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
  prerequisite_node = models.ForeignKey(
    'courses.CoursePrerequisiteNode',
    on_delete=models.CASCADE, 
    related_name='user_paths'
  )
  parent = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    related_name='children',
    null=True,
    blank=True,
    db_index=True
  )
  branch_completed = models.BooleanField(default=False)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'target_course'],
        condition=models.Q(parent__isnull=True),
        name='unique_root_per_user_course'
      )
    ]
    indexes = [
      models.Index(fields=['user', 'target_course', 'parent'])
    ]
