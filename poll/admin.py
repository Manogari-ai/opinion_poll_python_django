from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Vote

admin.site.register(Question)
admin.site.register(Choice)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice')
    list_filter = ('question', 'choice', 'user')
    search_fields = ('user__username', 'question__question_text')
