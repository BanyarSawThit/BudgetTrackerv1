from datetime import datetime, timedelta
from django.db.models import Sum, Count

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ExpenseForm
from .models import Expense, Category

def home(request):
    """Main page, quick expenses entry"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    today = datetime.now().date()
    today_expenses = Expense.objects.filter(date=today)
    today_total = today_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'form': form,
        'today_expenses': today_expenses,
        'today_total': today_total,
        'today_date': today,
    }

    return render(request, 'expenses/home.html', context)


def expense_history(request):
    """View expense history with monthly summary"""
    # Get month from query params, default to current month
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    # Calculate date range for the month
    first_day = datetime(year, month, 1).date()
    if month == 12:
        last_day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1).date() - timedelta(days=1)

    # Get expenses for the month
    expenses = Expense.objects.filter(date__gte=first_day, date__lte=last_day)

    # Category breakdown
    category_summary = expenses.values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')

    # Add display names for categories
    for item in category_summary:
        item['category_display'] = dict(Category.CATEGORY_CHOICES)[item['category']]

    # Daily breakdown
    daily_expenses = expenses.values('date').annotate(
        total=Sum('amount')
    ).order_by('-date')

    # Total for the month
    month_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Navigation dates
    prev_month = first_day - timedelta(days=1)
    if month == 12:
        next_month = datetime(year + 1, 1, 1).date()
    else:
        next_month = datetime(year, month + 1, 1).date()

    context = {
        'expenses': expenses,
        'category_summary': category_summary,
        'daily_expenses': daily_expenses,
        'month_total': month_total,
        'current_month': first_day,
        'prev_month': prev_month,
        'next_month': next_month,
        'year': year,
        'month': month,
    }
    return render(request, 'expenses/history.html', context)


def expense_edit(request, pk):
    """Edit an expense"""
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('history')
    else:
        form = ExpenseForm(instance=expense)

    context = {
        'form': form,
        'expense': expense,
        'is_edit': True,
    }
    return render(request, 'expenses/edit.html', context)


def expense_delete(request, pk):
    """Delete an expense"""
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        expense.delete()
        return redirect('history')

    context = {
        'expense': expense,
    }
    return render(request, 'expenses/delete.html', context)


def daily_detail(request, date_str):
    """View all expenses for a specific day"""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return redirect('history')

    expenses = Expense.objects.filter(date=date)
    daily_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Category breakdown for the day
    category_summary = expenses.values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    )

    for item in category_summary:
        item['category_display'] = dict(Category.CATEGORY_CHOICES)[item['category']]

    context = {
        'date': date,
        'expenses': expenses,
        'daily_total': daily_total,
        'category_summary': category_summary,
    }
    return render(request, 'expenses/daily_detail.html', context)
