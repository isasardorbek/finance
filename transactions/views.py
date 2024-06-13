from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

def register(request):
    """
    Purpose: Handles user registration functionality.
    Request Method: POST to register a new user and GET to render the registration page.
    Parameters: Username, password.
    Response: Redirects to the dashboard upon successful registration and login, or renders the registration page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    """
    Purpose: Displays the user's dashboard with income and expense transactions.
    Request Method: GET.
    Response: Renders the dashboard page with lists of income and expense transactions.
    """
    incomes = Transaction.objects.filter(user=request.user, transaction_type='income')
    expenses = Transaction.objects.filter(user=request.user, transaction_type='expense')
    return render(request, 'transactions/dashboard.html', {'incomes': incomes, 'expenses': expenses})

@login_required
def add_transaction(request, transaction_type):
    """
    Purpose: Handles adding a new transaction (income or expense) for the user.
    Request Method: POST to save the transaction and GET to render the transaction form.
    Parameters: Transaction details.
    Response: Redirects to the dashboard upon successful transaction creation or renders the transaction form.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = transaction_type
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form, 'transaction_type': transaction_type})

@login_required
def edit_transaction(request, pk):
    """
    Purpose: Handles editing an existing transaction for the user.
    Request Method: POST to update the transaction and GET to render the edit form.
    Parameters: Transaction details.
    Response: Redirects to the dashboard upon successful transaction update or renders the edit form.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    """
    Purpose: Handles deleting an existing transaction for the user.
    Request Method: POST to confirm deletion.
    Parameters: Transaction ID.
    Response: Redirects to the dashboard upon successful transaction deletion or renders the confirmation page.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'transactions/confirm_delete.html', {'transaction': transaction})

def logout_view(request):
    """
    Purpose: Handles user logout.
    Request Method: Any.
    Response: Redirects to the dashboard.
    """
    logout(request)
    return redirect('dashboard')
