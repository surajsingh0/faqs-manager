from django.db import models
from django.conf import settings

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question[:50]

    def get_translation(self, lang='en'):
        if lang == 'en':
            return {
                'question': self.question,
                'answer': self.answer
            }
        translation = self.translations.filter(language=lang).first()
        if translation:
            return {
                'question': translation.question,
                'answer': translation.answer
            }
        return {
            'question': self.question,
            'answer': self.answer
        }

class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('faq', 'language')
        verbose_name = "FAQ Translation"
        verbose_name_plural = "FAQ Translations"

    def __str__(self):
        return f"{self.faq.question[:30]} [{self.language}]"