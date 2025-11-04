from django.db import models

# Root
class UserChecklist(models.Model):
  pass # SHOULD WE STORE ACTIVE SPECIALIZATION HERE INSTEAD AS A BOOL?

# Node
class UserChecklistRequirement(models.Model):
  pass

class UserAdditionalRequirement(models.Model):
  pass

class UserDepthConstrain(models.Model):
  pass