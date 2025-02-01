from django.contrib import admin
from django.utils.html import strip_tags
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.conf import settings
from googletrans import Translator
from django import forms
from .models import FAQ, FAQTranslation

class FAQAdminForm(forms.ModelForm):
    question = forms.CharField(widget=CKEditorUploadingWidget())
    answer = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = FAQ
        fields = '__all__'

class FAQTranslationInline(admin.StackedInline):
    model = FAQTranslation
    extra = 0
    fields = ['language', 'question', 'answer']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    inlines = [FAQTranslationInline]
    list_display = ['truncated_question', 'created_at', 'updated_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at', 'updated_at']

    def truncated_question(self, obj):
        return strip_tags(obj.question)[:50] + '...' if len(strip_tags(obj.question)) > 50 else strip_tags(obj.question)
    truncated_question.short_description = 'Question'

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            try:
                translator = Translator()
                clean_question = strip_tags(obj.question)
                clean_answer = strip_tags(obj.answer)

                for lang_code, _ in settings.LANGUAGES:
                    if lang_code == 'en':
                        continue

                    try:
                        if not FAQTranslation.objects.filter(faq=obj, language=lang_code).exists():
                            translated_question = translator.translate(clean_question, dest=lang_code).text
                            translated_answer = translator.translate(clean_answer, dest=lang_code).text

                            FAQTranslation.objects.create(
                                faq=obj,
                                language=lang_code,
                                question=translated_question,
                                answer=translated_answer
                            )
                    except Exception as e:
                        self.message_user(
                            request,
                            f"Translation failed for {lang_code}: {str(e)}",
                            level='ERROR'
                        )
            except Exception as e:
                self.message_user(
                    request,
                    f"Translation initialization failed: {str(e)}",
                    level='ERROR'
                )