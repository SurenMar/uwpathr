from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Course(models.Model):
    code = models.CharField(max_length=32, unique=True)
    number = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    credits = models.IntegerField()  # e.g. 25 means 0.25 units
    program = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class CourseRequisiteNode(models.Model):
    REQ_KINDS = [('prereq','prereq'), ('coreq','coreq'), ('antireq','antireq')]
    NODE_TYPES = [('group','group'), ('course','course')]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='req_nodes')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    node_type = models.CharField(max_length=8, choices=NODE_TYPES)
    referenced_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    required_count = models.IntegerField(default=0)   # groups: how many children required
    req_kind = models.CharField(max_length=8, choices=REQ_KINDS)
    position = models.IntegerField(default=0)

    class Meta:
      indexes = [
          models.Index(fields=['course', 'requisite_type']),
          models.Index(fields=['required_course']),
      ]

class Specialization(models.Model):
    name = models.CharField(max_length=255)

class RequirementTemplate(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    year = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    archived = models.BooleanField(default=False)

class RequirementTemplateNode(models.Model):
    NODE_TYPES = [('group','group'), ('checkbox','checkbox'), ('depth_chain','depth_chain')]
    template = models.ForeignKey(RequirementTemplate, on_delete=models.CASCADE, related_name='nodes')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    node_type = models.CharField(max_length=16, choices=NODE_TYPES)
    required_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    units_required = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(default=0)

class RequirementNodeAllowedCourse(models.Model):
    node = models.ForeignKey(RequirementTemplateNode, on_delete=models.CASCADE, related_name='allowed_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('node','course')

class DepthChain(models.Model):
    node = models.OneToOneField(RequirementTemplateNode, on_delete=models.CASCADE)

class DepthChainItem(models.Model):
    chain = models.ForeignKey(DepthChain, on_delete=models.CASCADE, related_name='items')
    order_idx = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('chain','order_idx')
        ordering = ['order_idx']

class UserChecklist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user'])]

class UserCourse(models.Model):
    STATUS_CHOICES = [('taken','taken'), ('planned','planned'), ('wishlist','wishlist')]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    term_taken = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        unique_together = ('user','course')
        indexes = [models.Index(fields=['user']), models.Index(fields=['course'])]

class UserChecklistAssignment(models.Model):
    checklist = models.ForeignKey(UserChecklist, on_delete=models.CASCADE)
    node = models.ForeignKey(RequirementTemplateNode, on_delete=models.CASCADE)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('checklist','node','user_course')

class UserPath(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='paths')
    target_course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='targeted_paths')
    root = models.ForeignKey('UserPathNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'target_course')

class UserPathNode(models.Model):
    path = models.ForeignKey(UserPath, on_delete=models.CASCADE, related_name='nodes')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.IntegerField(default=0) # Verify with requisite position
