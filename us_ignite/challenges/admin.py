from django.contrib import admin

from us_ignite.challenges.models import Challenge, Entry, Question


class QuestionInlineAdmin(admin.TabularInline):
    model = Question
    extra = 5


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'start_datetime', 'end_datetime')
    search_fields = ('name', 'slug', 'summary', 'description')
    list_filter = ('status', 'start_datetime', 'end_datetime')
    date_hierarchy = 'start_datetime'
    inlines = [QuestionInlineAdmin]


class EntryAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'application', 'status', 'created', 'modified')
    list_filter = ('challenge__name', 'status')
    date_hierarchy = 'created'
    raw_id_fields = ('application', )


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Entry, EntryAdmin)
