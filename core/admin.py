from django.contrib import admin
from .models import Income, Expense

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'user')

    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
