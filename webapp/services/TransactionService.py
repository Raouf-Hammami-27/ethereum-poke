from webapp.models import Transaction
from webapp.serializers import TransactionSerializer as AS
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TransactionService(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AS.TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(fr=self.request.user)