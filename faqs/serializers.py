from rest_framework import serializers
from django.utils.html import strip_tags
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

    def get_question(self, obj):
        lang = self.context['request'].query_params.get('lang', 'en')
        return strip_tags(obj.get_translation(lang)['question'])

    def get_answer(self, obj):
        lang = self.context['request'].query_params.get('lang', 'en')
        return strip_tags(obj.get_translation(lang)['answer'])