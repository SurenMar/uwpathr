# Generated migration to convert selected_course from Course to UserCourse
from django.db import migrations, models
import django.db.models.deletion


def convert_course_to_usercourse(apps, schema_editor):
    """
    Convert selected_course from Course FK to UserCourse FK.
    For each UserChecklistNode with a selected_course (Course), 
    find or create the corresponding UserCourse and update the reference.
    """
    UserChecklistNode = apps.get_model('progress', 'UserChecklistNode')
    UserCourse = apps.get_model('progress', 'UserCourse')
    UserChecklist = apps.get_model('progress', 'UserChecklist')
    
    # Get all nodes that have a selected course (without select_related since it's now an IntegerField)
    nodes_with_course = UserChecklistNode.objects.filter(
        selected_course__isnull=False
    )
    
    for node in nodes_with_course:
        course_id = node.selected_course  # This is currently a Course ID (stored as integer)
        # Get the user from the target checklist
        target_checklist = UserChecklist.objects.get(pk=node.target_checklist_id)
        user = target_checklist.user
        
        # Find or create the UserCourse for this course and user
        user_course, created = UserCourse.objects.get_or_create(
            user=user,
            course_id=course_id,
            defaults={'course_list': 'taken'}
        )
        
        # Update the node to point to the UserCourse ID instead of Course ID
        node.selected_course = user_course.id
        node.save(update_fields=['selected_course'])


def reverse_conversion(apps, schema_editor):
    """
    Reverse: Convert UserCourse FK back to Course FK.
    For each UserChecklistNode with a selected_course (UserCourse),
    update to point to the Course instead.
    """
    UserChecklistNode = apps.get_model('progress', 'UserChecklistNode')
    
    nodes_with_usercourse = UserChecklistNode.objects.filter(
        selected_course__isnull=False
    ).select_related('selected_course__course')
    
    for node in nodes_with_usercourse:
        # Get the Course ID from the UserCourse
        course_id = node.selected_course.course_id
        
        # Update to point to Course ID instead
        UserChecklistNode.objects.filter(pk=node.pk).update(
            selected_course_id=course_id
        )


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0008_alter_userchecklistnode_selected_course'),
    ]

    operations = [
        # First, remove the foreign key constraint temporarily
        migrations.AlterField(
            model_name='userchecklistnode',
            name='selected_course',
            field=models.IntegerField(blank=True, null=True),
        ),
        # Then do the data migration
        migrations.RunPython(
            convert_course_to_usercourse,
            reverse_conversion
        ),
    ]
