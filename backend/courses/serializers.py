from rest_framework import serializers
from courses.models import Course, CoursePrerequisiteNode


class CourseListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at', 'code', 'number', 'title',
			'num_uwflow_ratings', 'uwflow_liked_rating', 'uwflow_easy_ratings', 
			'uwflow_useful_ratings',
		]


class CourseDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at', 'code', 'number', 'units', 
			'category', 'corequisites', 'antirequisites',
			'title', 'description', 
			'num_uwflow_ratings', 'uwflow_liked_rating', 'uwflow_easy_ratings', 
			'uwflow_useful_ratings',
		]
		

class CoursePrerequisiteNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	children = serializers.SerializerMethodField()
	
	class Meta:
		model = CoursePrerequisiteNode
		fields = [
			'id', 'created_at', 'updated_at',
			'target_course', 'node_type',
			'leaf_course', 'num_children_required', 'children',
		]

	def get_children(self, obj):
		# Assumes queryset is prefetched in view
		children = obj.get_children()
		return CoursePrerequisiteNodeListSerializer(
      children, 
      many=True,
      context=self.context
    ).data
	