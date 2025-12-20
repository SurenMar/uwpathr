from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at',
			'code', 'number', 'units', 'offered_next_term', 'category',
			'title', 'description', 'num_uwflow_ratings', 'uwflow_liked_rating', 
			'uwflow_easy_ratings', 'uwflow_useful_ratings',
		]
		read_only_fields = ['id', 'created_at', 'updated_at']
