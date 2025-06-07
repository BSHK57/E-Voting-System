from django.contrib import admin
from .models import Voting, Vote

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_active')
    actions = ['start_election', 'stop_election']

    def start_election(self, request, queryset):
        queryset.update(is_active=True)
    start_election.short_description = "Start selected elections"

    def stop_election(self, request, queryset):
        queryset.update(is_active=False)
    stop_election.short_description = "Stop selected elections"

admin.site.register(Vote)
