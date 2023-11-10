from rest_framework import viewsets
from account.serializers import AccountSerializer
from .models import Account
from rest_framework.response import Response
from .schema import user_list_docs
from rest_framework.permissions import IsAuthenticated


class AccountViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]

    @user_list_docs
    def list(self, request):

        user_id = request.query_params.get("user_id")
        queryset = self.queryset.get(id=user_id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data)




