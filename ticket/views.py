from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from .serializers import TicketSerializer
from .models import Ticket, StatusChoices


# Create your views here.
class TicketViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):

    permission_action_classes = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "partial_update": [IsAuthenticated],
        "delete": [IsAuthenticated],
        "my_documents": [IsAuthenticated],
    }

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Get all open tickets for the authenticated user.",
        responses={200: TicketSerializer(many=True)},
    )
    @action(detail=False, methods=["GET"], url_path="my_tickets")
    def my_tickets(self, request):
        user = request.user
        tickets = Ticket.objects.filter(user=user, status=StatusChoices.OPEN)

        if not tickets.exists():
            return Response(
                {"detail": "No tickets found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
