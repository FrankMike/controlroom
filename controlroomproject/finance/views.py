from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Transaction
from .forms import TransactionForm


@login_required
def finance(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")[:10]
    total_incomes = (
        Transaction.objects.filter(
            user=request.user, transaction_type="income"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    total_expenses = (
        Transaction.objects.filter(
            user=request.user, transaction_type="expense"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    balance = total_incomes - total_expenses

    context = {
        "transactions": transactions,
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "balance": balance,
    }
    return render(request, "finance/finance.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        Transaction.objects.create(
            user=request.user,
            description=request.POST["description"],
            amount=request.POST["amount"],
            transaction_type=request.POST["transaction_type"],
        )
    return redirect("finance")


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("finance")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "finance/edit_transaction.html", {"form": form})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "POST":
        transaction.delete()
        return redirect("finance")

    return render(
        request, "finance/delete_transaction.html", {"transaction": transaction}
    )
