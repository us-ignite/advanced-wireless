from django.contrib import admin

from us_ignite.challenges.models import Challenge, Entry, EntryAnswer, Question


class QuestionInlineAdmin(admin.TabularInline):
    model = Question
    extra = 5


class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'status', 'is_external',
        'start_datetime', 'end_datetime')
    search_fields = ('name', 'slug', 'summary', 'description')
    list_filter = ('status', 'is_external', 'start_datetime', 'end_datetime')
    date_hierarchy = 'start_datetime'
    inlines = [QuestionInlineAdmin]


class EntryAnswerAdminInstance(admin.TabularInline):
    extra = 0
    model = EntryAnswer


class EntryAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'application', 'status', 'created', 'modified')
    list_filter = ('challenge__name', 'status')
    date_hierarchy = 'created'
    raw_id_fields = ('application', )
    inlines = [EntryAnswerAdminInstance, ]


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Entry, EntryAdmin)
