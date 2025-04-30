from django.contrib import admin
from .models import ConversationPair, UnknownQuestion
from .models import SimplifierMapping

@admin.register(ConversationPair)
class ConversationPairAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at')
    search_fields = ('question', 'answer')

@admin.register(UnknownQuestion)
class UnknownQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'timestamp')


@admin.register(SimplifierMapping)
class SimplifierMappingAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'replacement')
