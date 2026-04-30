from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CalendarEntry, Participation
from .forms import ParticipationForm


@login_required
def home(request):
    entry = CalendarEntry.objects.filter(status='open').order_by('-created_at').first()
    return render(request, 'planning/home.html', {'entry': entry})


@login_required
def participate(request, entry_id):
    entry = get_object_or_404(CalendarEntry, id=entry_id)
    existing = Participation.objects.filter(user=request.user, calendar_entry=entry).first()

    if request.method == 'POST':
        form = ParticipationForm(request.POST, instance=existing)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.user = request.user
            participation.calendar_entry = entry
            participation.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = ParticipationForm(instance=existing)

    return render(request, 'planning/participate.html', {'form': form, 'entry': entry})
