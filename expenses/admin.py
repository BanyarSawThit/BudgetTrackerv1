from django.contrib import admin

from .models import Category,Expense, Income

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'category', 'amount', 'created_at']
    list_filter = ['category', 'date']
    search_fields = ['description']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']



@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['date', 'source', 'amount', 'description', 'created_at']
    list_filter = ['date']
    search_fields = ['source', 'description']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']