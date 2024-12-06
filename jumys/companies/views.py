from rest_framework import generics, permissions, status
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsManagerOrAdmin
from users.serializers import UserSerializer
from users.models import CustomUser
from rest_framework.response import Response

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(head_manager=self.request.user)

class AddManagerToCompanyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]
    serializer_class = UserSerializer

    def post(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'detail': 'Company does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if company.head_manager != request.user:
            return Response({'detail': 'You are not the head manager of this company.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = 'manager'
        user.save()
        company.managers.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
