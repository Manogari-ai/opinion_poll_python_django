from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from .models import Question, Choice, Vote

admin.site.register(Question)
admin.site.register(Choice)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

    list_display = ('user', 'question', 'choice')
    list_filter = ('question', 'choice', 'user')
    search_fields = ('user__username', 'question__question_text')

    change_list_template = "admin/vote_chart.html"

    def changelist_view(self, request, extra_context=None):

        from django.db.models import Count

        results = Choice.objects.annotate(total_votes=Count('vote'))

        labels = []
        votes = []

        for r in results:
            labels.append(r.choice_text)
            votes.append(r.total_votes)

        extra_context = extra_context or {}
        extra_context["labels"] = labels
        extra_context["votes"] = votes

        return super().changelist_view(request, extra_context=extra_context)
    

   # ✅ Custom User Admin with Chart
class CustomUserAdmin(UserAdmin):

    change_list_template = "admin/user_chart.html"

    def changelist_view(self, request, extra_context=None):

        # 📊 Votes per user
        data = (
            Vote.objects
            .values('user__username')
            .annotate(total=Count('id'))
        )

        users = []
        votes = []

        for d in data:
            users.append(d['user__username'])
            votes.append(d['total'])

        extra_context = extra_context or {}
        extra_context['users'] = users
        extra_context['votes'] = votes

        return super().changelist_view(request, extra_context=extra_context)


# ❗ IMPORTANT: unregister first
admin.site.unregister(User)

# ✅ register again with custom admin
admin.site.register(User, CustomUserAdmin)