from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from checklists.models.checklist import (
  Checklist, 
  ChecklistNode, 
  CheckboxAllowedCourses,
)


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
  list_display = ['id', 'year', 'units_required', 'specialization']


@admin.register(ChecklistNode)
class ChecklistNodeAdmin(MPTTModelAdmin):
  list_display = ['id', 'requirement_type', 'title', 'units_required', 'target_year', 'target_specialization']
  search_fields = ['target_checklist__specialization', 'target_checklist__year']


@admin.register(CheckboxAllowedCourses)
class CheckboxAllowedCoursesAdmin(admin.ModelAdmin):
  list_display = ['id', 'target_requirement_type', 'target_title', 'course_list']
  search_fields = ['courses__code', 'courses__number']
  autocomplete_fields = ['courses']

