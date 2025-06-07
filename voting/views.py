from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Voting, Vote
from accounts.models import CandidateProfile

def home_view(request):
    live_elections = Voting.objects.filter(is_active=True)
    completed_elections = Voting.objects.filter(is_active=False)
    # Get top candidate for live elections
    live_elections_data = []
    for election in live_elections:
        candidates = election.candidates.all()
        votes = Vote.objects.filter(voting=election)
        vote_counts = {candidate: votes.filter(candidate=candidate).count() for candidate in candidates}
        if vote_counts:
            top_candidate = max(vote_counts, key=vote_counts.get)
            top_votes = vote_counts[top_candidate]
        else:
            top_candidate = None
            top_votes = 0
        live_elections_data.append({
            'election': election,
            'top_candidate': top_candidate,
            'top_votes': top_votes
        })
    # Get winner for completed elections
    completed_elections_data = []
    for election in completed_elections:
        candidates = election.candidates.all()
        votes = Vote.objects.filter(voting=election)
        vote_counts = {candidate: votes.filter(candidate=candidate).count() for candidate in candidates}
        if vote_counts:
            winner = max(vote_counts, key=vote_counts.get)
            winner_votes = vote_counts[winner]
        else:
            winner = None
            winner_votes = 0
        completed_elections_data.append({
            'election': election,
            'winner': winner,
            'winner_votes': winner_votes
        })
    return render(request, 'home.html', {
        'live_elections_data': live_elections_data,
        'completed_elections_data': completed_elections_data
    })

@login_required
def available_elections_view(request):
    voted_elections = Vote.objects.filter(voter=request.user)
    voted_election_ids = voted_elections.values_list('voting_id', flat=True)
    elections = Voting.objects.exclude(id__in=voted_election_ids)
    return render(request, 'available_elections.html', {
        'elections': elections,
        'voted_elections': voted_elections
    })

@login_required
def vote_view(request, election_id):
    election = get_object_or_404(Voting, id=election_id, is_active=True)
    candidates = election.candidates.all()
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(CandidateProfile, id=candidate_id)
        # Prevent double voting
        if not Vote.objects.filter(voter=request.user, voting=election).exists():
            Vote.objects.create(voter=request.user, voting=election, candidate=candidate)
        return redirect('available_elections')
    return render(request, 'vote.html', {'election': election, 'candidates': candidates})

@login_required
def results_view(request, election_id):
    election = get_object_or_404(Voting, id=election_id)
    candidates = election.candidates.all()
    votes = Vote.objects.filter(voting=election)
    # Count votes per candidate
    vote_counts = {candidate: votes.filter(candidate=candidate).count() for candidate in candidates}
    total_votes = votes.count()
    is_completed = not election.is_active
    return render(request, 'results.html', {
        'election': election,
        'vote_counts': vote_counts,
        'total_votes': total_votes,
        'is_completed': is_completed
    })
