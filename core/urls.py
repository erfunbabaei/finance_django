from django.urls import path
from .views import CustomLoginView, dashboard_api, logout_api, RegisterAPIView
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, ExpenseViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register_api'),
    path('api/login/', CustomLoginView.as_view(), name='login_api'),  # JWT login
    path('api/logout/', logout_api, name='logout_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path('api/dashboard/', dashboard_api, name='dashboard_api'),
]

urlpatterns += router.urls
