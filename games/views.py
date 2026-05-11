from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Game, GameLibrary

@login_required
def game_library(request):
    library_entries = GameLibrary.objects.filter(user=request.user).select_related('game__category')
    games = [entry.game for entry in library_entries]
    return render(request, 'games/game_library.html', {'games': games})

@login_required
def game_search(request):
    query = request.GET.get('q', '')
    owned_ids = GameLibrary.objects.filter(user=request.user).values_list('game_id', flat=True)
    games = Game.objects.select_related('category').exclude(id__in=owned_ids)
    if query:
        games = games.filter(name__icontains=query)
    return render(request, 'games/game_search.html', {'games': games, 'owned_ids': owned_ids, 'query': query})

@login_required
def toggle_owned(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    entry, created = GameLibrary.objects.get_or_create(user=request.user, game=game)
    if not created:
        entry.delete()
    return redirect(request.META.get('HTTP_REFERER', 'game_library'))