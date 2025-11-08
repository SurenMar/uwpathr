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
    # TODO Rework indexes and ordering for frontend csr
    indexes = [
      models.Index(fields=['user', 'course_list'])
    ]
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'course'], 
        name='unique_course_per_user'
      )
    ]

  # Change total_units or num_courses in corrosponding UserDepthList fields
  @transaction.atomic # Strong guarantee
  def delete(self, *args, **kwargs):
    depth_lists = list(self.depth_lists.all())
    for depth_list in depth_lists:
      depth_list.num_courses -= 1
      depth_list.total_units -= self.course.units
      depth_list.save()
    super().delete(*args, **kwargs)


class UserCoursePathNode(MP_Node):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='course_paths' # TODO We might not need this reverse relationship
  )
  target_course = models.ForeignKey(
    'UserCourse',
    on_delete=models.CASCADE,
    related_name='paths'
  )
  requisite_node = models.ForeignKey(
    'courses.CourseRequisiteNode',
    on_delete=models.PROTECT, # Course requisites and paths will be fully updated before any removed courses are deleted
    related_name='+'
  )

  class Meta:
    # TODO Rework indexes and ordering for frontend csr
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'target_course'], 
        name='unique_target_course_per_user'
      )
    ]
    indexes = [
      models.Index(fields=['user', 'target_course', 'parent']),
      models.Index(fields=['user', 'target_course', 'depth']), # Might not need this
    ]
