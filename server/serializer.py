# Import necessary modules and classes from the rest_framework library.
from rest_framework import serializers

# Import models from the local module.
from .models import Server, Channel, Category


# Define a serializer for the Category model.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Define a serializer for the Channel model.
class ChanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


# Define a serializer for the Server model.
class ServerSerializer(serializers.ModelSerializer):
    # Add a custom SerializerMethodField to calculate 'num_members'.
    num_members = serializers.SerializerMethodField()
    # Serialize the related 'channel_server' field using ChanelSerializer.
    channel_server = ChanelSerializer(many=True)
    # Serialize the 'category' field as a string representation.
    category = serializers.StringRelatedField()

    class Meta:
        model = Server
        # Exclude 'member' field from serialization.
        exclude = ("member",)

    # Custom method to get 'num_members' for the Server instance.
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    # Override the to_representation method to remove 'num_members' field if not needed.
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
