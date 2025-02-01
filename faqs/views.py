from rest_framework import viewsets
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        cache_key = f'faqs_{lang}'
        
        if not cache.get(cache_key):
            queryset = FAQ.objects.prefetch_related('translations').all()
            cache.set(cache_key, queryset, timeout=900)
        
        return cache.get(cache_key)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context