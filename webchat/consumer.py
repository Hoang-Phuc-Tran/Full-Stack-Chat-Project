# Import necessary modules from Django and Channels.
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

# Import models from the local module.
from .models import Conversation, Message

# Get the User model defined in the Django project.
User = get_user_model()


# Define a WebSocket consumer for a web chat.
class WebChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None  # Initialize channel ID
        self.user = None  # Initialize user

    def connect(self):
        # Accept the WebSocket connection.
        self.accept()

        # Retrieve the channel ID from the URL route's kwargs.
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]

        # Retrieve a user (for demonstration, using the user with ID 1).
        self.user = User.objects.get(id=1)

        # Add the WebSocket consumer to the corresponding channel group.
        async_to_sync(self.channel_layer.group_add)(self.channel_id, self.channel_name)

    def receive_json(self, content):
        # Extract relevant data from the received JSON content.
        channel_id = self.channel_id
        sender = self.user
        message = content["message"]

        # Get or create a Conversation object associated with the channel.
        conversation, created = Conversation.objects.get_or_create(
            channel_id=channel_id
        )

        # Create a new Message object and associate it with the conversation.
        new_message = Message.objects.create(
            conversation=conversation, sender=sender, content=message
        )

        # Send the new message data to the channel group.
        async_to_sync(self.channel_layer.group_send)(
            self.channel_id,
            {
                "type": "chat.message",
                "new_message": {
                    "id": new_message.id,
                    "sender": new_message.sender.username,
                    "content": new_message.content,
                    "timestamp": new_message.timestamp.isoformat(),
                },
            },
        )

    def chat_message(self, event):
        # Send a JSON message to the WebSocket client.
        self.send_json(event)

    def disconnect(self, close_code):
        # Remove the WebSocket consumer from the channel group upon disconnection.
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_id, self.channel_name
        )
        super().disconnect(close_code)
