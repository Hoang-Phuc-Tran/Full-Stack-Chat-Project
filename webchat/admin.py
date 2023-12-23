from django.contrib import admin
from .models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('id', 'field1', 'field2')  # Replace 'field1', 'field2' with actual field names


admin.site.register(Conversation)
admin.site.register(Message)
