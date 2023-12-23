from django.contrib.auth import get_user_model
from django.db import models


class Conversation(models.Model):
    channel_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This will display as "Conversation - [Channel ID]"
        return f"Conversation - {self.channel_id}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="message"
    )
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Optional: Modify this to display messages in a meaningful way
        return f"Message from {self.sender} at {self.timestamp}"
