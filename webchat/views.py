# Import necessary modules from the rest_framework library.
from rest_framework import viewsets
from rest_framework.response import Response

# Import models, schemas, and serializers from the local module.
from .models import Conversation
from .schemas import list_message_docs
from .serializers import MessageSerializer


# Define a ViewSet for handling messages.
class MessageViewSet(viewsets.ViewSet):
    # Apply the 'list_message_docs' decorator to document the 'list' method.
    @list_message_docs
    def list(self, request):
        # Retrieve the 'channel_id' from the query parameters of the request.
        channel_id = request.query_params.get("channel_id")

        try:
            # Attempt to retrieve a Conversation object based on the 'channel_id'.
            conversation = Conversation.objects.get(channel_id=channel_id)
            # Retrieve all messages associated with the Conversation.
            messages = conversation.message.all()
            # Serialize the messages using the 'MessageSerializer'.
            serializer = MessageSerializer(messages, many=True)
            # Return a Response with the serialized message data.
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            # If the Conversation does not exist, return an empty Response.
            return Response([])
