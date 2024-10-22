from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import DiaryEntry
from .forms import DiaryEntryForm

import logging

logger = logging.getLogger(__name__)


@login_required
def diary(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by("-date")
    return render(request, "diary/diary.html", {"entries": entries})


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
    return render(request, "diary/diary_form.html", {"form": form, "action": "Add"})


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
    return render(request, "diary/diary_form.html", {"form": form, "action": "Edit"})


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
