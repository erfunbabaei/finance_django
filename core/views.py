from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import update_last_login


# ----------------------------
# Register API / View
# ----------------------------
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not first_name:
            return Response({"error": "First name required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not last_name:
            return Response({"error": "Last name required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({"error": "Username required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({"error": "Email required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name=first_name, last_name = last_name, username=username, email=email, password=password
        )

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

# ----------------------------
# Logout API / View
# ----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_api(request):

    response = JsonResponse({"message": "Logged out successfully"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.status_code = 302
    response["Location"] = ""

    return response

# ----------------------------
# Custom JWT Login (sets cookies)
# ----------------------------
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            tokens = response.data

            username_or_email = request.data.get("username") or request.data.get("email")
            user = User.objects.filter(username=username_or_email).first() or \
                   User.objects.filter(email=username_or_email).first()

            if user:
                update_last_login(None, user)

            response.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=3600
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 3600
            )

        return response

# ----------------------------
# Income / Expense ViewSets
# ----------------------------
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ----------------------------
# Dashboard API
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    month = request.GET.get("month")
    year = request.GET.get("year")

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    if month:
        incomes = incomes.filter(date__month=int(month))
        expenses = expenses.filter(date__month=int(month))
    if year:
        incomes = incomes.filter(date__year=int(year))
        expenses = expenses.filter(date__year=int(year))

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    profit = total_income - total_expense

    data = {
        "month": month if month else "all",
        "year": year if year else "all",
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "profit_or_loss": float(profit),
        "incomes": [
            {"title": i.title, "amount": float(i.amount), "date": i.date.strftime("%Y-%m-%d")}
            for i in incomes
        ],
        "expenses": [
            {"title": e.title, "amount": float(e.amount), "date": e.date.strftime("%Y-%m-%d")}
            for e in expenses
        ],
    }

    return Response(data)
