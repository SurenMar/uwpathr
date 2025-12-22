from rest_framework import serializers
from .models import Course, CourseRequisiteNode


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
			'offered_next_term', 'category', 'title', 'description', 
			'num_uwflow_ratings', 'uwflow_liked_rating', 'uwflow_easy_ratings', 
			'uwflow_useful_ratings',
		]
		

class CourseRequisiteNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	children = serializers.SerializerMethodField()
	
	class Meta:
		model = CourseRequisiteNode
		fields = [
			'id', 'created_at', 'updated_at',
			'requisite_type', 'target_course', 'node_type',
			'leaf_course', 'num_children_required', 'children',
		]

	def get_children(self, obj):
		# Assumes queryset is prefetched in view
		children = obj.get_children()
		return CourseRequisiteNodeListSerializer(
      children, 
      many=True,
      context=self.context
    ).data
	