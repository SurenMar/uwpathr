from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from progress.models.user_checklist import UserChecklist, UserChecklistNode
from progress.models.user_requirements import UserAdditionalConstraint, UserDepthList
from progress.models.user_course import UserCourse, UserCoursePathNode


@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
	list_display = [
		'id', 'user', 'specialization', 'year', 'units_required',
		'taken_course_units', 'planned_course_units', 'original_checklist',
	]
	search_fields = ['user__email', 'user__username', 'specialization__name']


@admin.register(UserChecklistNode)
class UserChecklistNodeAdmin(MPTTModelAdmin):
	list_display = [
		'id', 'requirement_type', 'title', 'units_required', 'units_gathered',
		'completed', 'user', 'target_checklist',
	]
	search_fields = ['title', 'user__email', 'user__username', 'target_checklist__year']


@admin.register(UserAdditionalConstraint)
class UserAdditionalConstraintAdmin(MPTTModelAdmin):
	list_display = [
		'id', 'requirement_type', 'title', 'num_courses_required',
		'num_courses_gathered', 'completed', 'user', 'target_checklist',
	]
	search_fields = ['title', 'user__email', 'user__username', 'target_checklist__year']


@admin.register(UserDepthList)
class UserDepthListAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'target_checklist', 'is_chain', 'num_courses', 'total_units']
	search_fields = ['user__email', 'user__username']
	filter_horizontal = ['courses']


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'course', 'course_list']
	search_fields = ['user__email', 'user__username', 'course__code', 'course__number']
	list_filter = ['course_list']


@admin.register(UserCoursePathNode)
class UserCoursePathNodeAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'target_course', 'prerequisite_node']
	search_fields = ['user__email', 'user__username', 'target_course__course__code', 'target_course__course__number']
