from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CalendarEntry, Participation
from .forms import ParticipationForm
from collections import Counter
from games.models import GameCategory
from locations.models import Location
from django.utils.dateparse import parse_datetime


@login_required
def home(request):
    entry = CalendarEntry.objects.filter(status='open').order_by('-created_at').first()
    participation = None
    participations = []
    if entry:
        participation = Participation.objects.filter(user=request.user, calendar_entry=entry).first()
        participations = Participation.objects.filter(calendar_entry=entry).select_related('user')
    return render(request, 'planning/home.html', {'entry': entry, 'participation': participation, 'participations': participations})


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

@login_required
def entry_list(request):
    entries = CalendarEntry.objects.order_by('-date')
    return render(request, 'planning/entry_list.html', {'entries': entries})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def evaluate(request, entry_id):
    entry = get_object_or_404(CalendarEntry, id=entry_id)
    participations = Participation.objects.filter(calendar_entry=entry).select_related('user')

    available_count = participations.filter(available=True).count()
    cant_count = participations.filter(available=False).count()
    hosts = participations.filter(can_host=True).select_related('user')

    alt_dates = participations.exclude(alternative_date=None).values_list('alternative_date', flat=True)
    alt_counts = Counter(alt_dates)

    category_ids = []
    for p in participations:
        category_ids.extend(p.game_categories.values_list('id', flat=True))
    category_counts = Counter(category_ids)
    categories = [(GameCategory.objects.get(id=cid), count) for cid, count in category_counts.most_common()]

    if request.method == 'POST' and request.POST.get('action') == 'confirm':
        date = parse_datetime(request.POST.get('date'))
        location_id = request.POST.get('location_id')
        if date:
            entry.date = date
            entry.status = 'confirmed'
            if location_id:
                entry.location = Location.objects.filter(id=location_id).first()
            entry.save()
        return redirect('entry_list')

    return render(request, 'planning/evaluate.html', {
        'entry': entry,
        'participations': participations,
        'available_count': available_count,
        'cant_count': cant_count,
        'hosts': hosts,
        'alt_counts': alt_counts,
        'categories': categories,
    })

@login_required
@user_passes_test(is_staff)
def send_reminder(request, entry_id):
    entry = get_object_or_404(CalendarEntry, id=entry_id)
    # Placeholder for sending reminders, e.g. via push notifications or email
    return redirect('evaluate', entry_id=entry.id)
