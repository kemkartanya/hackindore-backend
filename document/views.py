from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from .permissions import CanAccessDocument
from .serializers import DocumentSerializer
from .models import Document


# Create your views here.
class DocumentViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):

    permission_action_classes = {
        "retrieve": [CanAccessDocument],
        "create": [IsAuthenticated],
        "update": [CanAccessDocument],
        "partial_update": [CanAccessDocument],
        "delete": [CanAccessDocument],
        "my_documents": [IsAuthenticated],
    }

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    @extend_schema(
        description="Get companies for the authenticated user.",
        responses={200: DocumentSerializer(many=True)},
    )
    @action(detail=False, methods=["GET"], url_path="my_documents")
    def my_documents(self, request):
        user = request.user
        documents = Document.objects.filter(user=user)

        if not documents.exists():
            return Response(
                {"detail": "No documents found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)
