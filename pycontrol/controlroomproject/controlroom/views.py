from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

from .models import DiaryEntry, Transaction
from .forms import DiaryEntryForm, TransactionForm


# Create your views here.
def home(request):
    return render(request, "home.html", {})


@login_required
def diary(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by("-date")
    return render(request, "diary.html", {"entries": entries})


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
    return render(request, "finance.html", context)


@login_required
def movies(request):
    context = {
        "plex_token": settings.PLEX_TOKEN,
        "plex_url": settings.PLEX_URL,
    }
    return render(request, "moviecollection.html", context)


@login_required
def tv(request):
    context = {
        "plex_token": settings.PLEX_TOKEN,
        "plex_url": settings.PLEX_URL,
    }
    return render(request, "tv.html", context)


@login_required
def add_entry(request):
    if request.method == "POST":
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("diary")
    else:
        form = DiaryEntryForm()
    return render(request, "diary_form.html", {"form": form, "action": "Add"})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("diary")
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, "diary_form.html", {"form": form, "action": "Edit"})


@login_required
def delete_entry(request, entry_id):
    logger.info(f"Attempting to delete entry with id: {entry_id}")
    try:
        entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
        if request.method == "POST":
            logger.info(f"Deleting entry: {entry}")
            entry.delete()
            logger.info("Entry deleted successfully")
            return redirect("diary")
        else:
            logger.warning(
                f"Delete request for entry {entry_id} was not a POST request"
            )
    except Exception as e:
        logger.error(f"Error deleting entry {entry_id}: {str(e)}")
        return HttpResponse(f"Error deleting entry: {str(e)}", status=500)

    return redirect("diary")


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
            return redirect(
                "finance"
            )  # Redirect to the finance page or wherever you want
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "edit_transaction.html", {"form": form})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "POST":
        transaction.delete()
        return redirect("finance")  # Redirect after deletion

    return render(request, "delete_transaction.html", {"transaction": transaction})
