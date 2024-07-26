from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        response = dict()

        if request.data.get("user"):
            user_serializer = UserSerializer(
                request.user, data=request.data.get("user"), partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()
                response["user"] = user_serializer.data
            else:
                return Response(
                    {"success": False, "message": user_serializer.errors},
                    status=400,
                )

        if len(response) == 0:
            return Response(
                {"success": False, "message": "No input provided"}, status=400
            )

        return Response(response)


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not request.user.check_password(old_password):
            return Response({"error": "Incorrect password."}, status=400)
        request.user.set_password(new_password)
        request.user.save()
        return Response(status=204)