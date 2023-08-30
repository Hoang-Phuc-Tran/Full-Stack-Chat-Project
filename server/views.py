from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from django.db.models import Count
from .models import Server
from .serializer import ServerSerializer
from .schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        A viewset for handling operations related to the Server model.

        This viewset provides functionality to retrieve a list of Server objects
        with various filtering options, such as filtering by category, user,
        server ID, and including the number of members.

        Attributes:
            queryset (QuerySet): The default queryset including all Server objects.

        Methods:
            list(request): Handles the list request for Server objects.

        Example:
            To retrieve a list of servers filtered by category and limited to 10
            results, make a GET request with query parameters:
            /servers/?category=gaming&qty=10

        Parameters:
            request (Request): The HTTP request object containing the following
                query parameters:

                - category (str): Filter servers by category.

                - qty (int): Limit the number of results.

                - by_user (bool): Filter servers by the requesting user (if true).

                - by_serverid (str): Filter servers by server ID.

                - with_num_members (bool): Include the number of members (if true).
        """
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            if by_user and request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(detail="Server value error")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        return Response(serializer.data)
