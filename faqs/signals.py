from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from googletrans import Translator
from .models import FAQ, FAQTranslation
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=FAQ)
def create_translations(sender, instance, created, **kwargs):
    """Create translations for new FAQ entries"""
    if created:
        translator = Translator()
        for lang_code, _ in settings.LANGUAGES:
            if lang_code == 'en':
                continue
            
            try:
                if not instance.translations.filter(language=lang_code).exists():
                    logger.info(f"Creating translation for FAQ {instance.id} in {lang_code}")
                    
                    # Strip HTML tags for translation
                    from django.utils.html import strip_tags
                    clean_question = strip_tags(instance.question)
                    clean_answer = strip_tags(instance.answer)
                    
                    translated_question = translator.translate(
                        clean_question, dest=lang_code
                    ).text
                    translated_answer = translator.translate(
                        clean_answer, dest=lang_code
                    ).text
                    
                    FAQTranslation.objects.create(
                        faq=instance,
                        language=lang_code,
                        question=translated_question,
                        answer=translated_answer
                    )
            except Exception as e:
                logger.error(f"Translation failed for {lang_code}: {str(e)}")

@receiver([post_save, post_delete], sender=FAQ)
@receiver([post_save, post_delete], sender=FAQTranslation)
def invalidate_cache(sender, instance, **kwargs):
    """Invalidate cache when FAQs or translations change"""
    if sender == FAQ:
        for lang_code, _ in settings.LANGUAGES:
            cache_key = f'faqs_{lang_code}'
            cache.delete(cache_key)
    elif sender == FAQTranslation:
        cache_key = f'faqs_{instance.language}'
        cache.delete(cache_key)