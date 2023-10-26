# Import necessary modules and classes from drf_spectacular library.
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Import the serializer used for the response.
from .serializer import ServerSerializer

# Define a documentation decorator for the server list endpoint.
server_list_docs = extend_schema(
    # Specify the expected response format using ServerSerializer for multiple items.
    responses=ServerSerializer(many=True),
    # Define query parameters for the endpoint.
    parameters=[
        # Define a query parameter 'category' of type string.
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of servers to retrieve",
        ),
        # Define a query parameter 'qty' of type integer.
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of servers to retrieve",
        ),
        # Define a query parameter 'by_user' of type boolean.
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers by the current authenticated user (True/False)",
        ),
        # Define a query parameter 'with_num_members' of type boolean.
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of members for each server in the response",
        ),
        # Define a query parameter 'by_serverid' of type integer.
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Include server by id",
        ),
    ],
)
