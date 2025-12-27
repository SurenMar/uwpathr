from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from checklists.models.checklist import (
  Checklist, 
  ChecklistNode, 
  CheckboxAllowedCourses,
)
