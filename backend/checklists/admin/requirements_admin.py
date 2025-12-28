from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from checklists.models.requirements import (
  Specialization, 
  NonCourseRequirement, 
  AdditionalConstraint,
  AdditionalConstraintAllowedCourses,
)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'description']


@admin.register(NonCourseRequirement)
class NonCourseRequirementAdmin(admin.ModelAdmin):
  list_display = ['id', 'year', 'description', 'checklist']


@admin.register(AdditionalConstraint)
class AdditionalConstraintAdmin(MPTTModelAdmin):
  list_display = ['id', 'requirement_type', 'title', 'num_courses_required', 'target_year', 'target_specialization']
  search_fields = ['target_checklist__specialization', 'target_checklist__year']


@admin.register(AdditionalConstraintAllowedCourses)
class AdditionalConstraintAllowedCoursesAdmin(admin.ModelAdmin):
  list_display = ['id', 'target_requirement_type', 'target_title', 'course_list']
