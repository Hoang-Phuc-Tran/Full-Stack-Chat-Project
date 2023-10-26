# Import necessary modules from Django.
from django.contrib.auth import get_user_model
from django.db import models


# Define a Django model for Conversations.
class Conversation(models.Model):
    # Field to store a unique channel identifier.
    channel_id = models.CharField(max_length=255)
    # Field to store the creation timestamp of the conversation.
    created_at = models.DateTimeField(auto_now_add=True)


# Define a Django model for Messages.
class Message(models.Model):
    # Relationship field to associate a message with a Conversation.
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="message"
    )
    # Relationship field to associate a message with a sender (User).
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Field to store the content of the message.
    content = models.TextField()
    # Field to store the timestamp when the message was created.
    timestamp = models.DateTimeField(auto_now_add=True)
