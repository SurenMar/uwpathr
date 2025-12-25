from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from courses.models import Course, CourseRequisiteNode

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ['code', 'number', 'units', 'display_category', 'num_uwflow_ratings']
  search_fields = ['code', 'number']
  list_filter = ['code']

  def display_category(self, obj):
    return ", ".join(obj.category)

  display_category.short_description = "Categories"


@admin.register(CourseRequisiteNode)
class CourseRequisiteNodeAdmin(admin.ModelAdmin):
  list_display = ['requisite_type', 'target_course_name', 'node_type', 'num_children_required', 'leaf_course']
  search_fields = ['target_course__code', 'target_course__number']
  list_filter = ['target_course__code', 'target_course__number']

  def target_course_name(self, obj):
    return str(obj.target_course)

  target_course_name.short_description = "Target Course"
