# matching/ranking.py

from django.db import transaction
from applications.models import Application

def update_job_rankings(job):
    """
    Recalculate ranks for all applications belonging to a specific job.
    Highest match_score gets Rank 1.
    If scores are equal, earlier applied_at gets priority.
    """
    # Fetch all applications for the job, ordered by score (desc) and date (asc)
    applications = Application.objects.filter(
        job=job
    ).order_by(
        '-match_score',
        'applied_at'
    )

    if not applications.exists():
        return

    # Using atomic transaction to prevent partial updates and race conditions
    with transaction.atomic():
        current_rank = 1
        previous_score = None
        same_rank_count = 0

        for app in applications:
            # Handle equal scores: give them same rank, or sequential?
            # Standard ranking: 1, 2, 2, 4 (if two have same score)
            # Or dense ranking: 1, 2, 2, 3
            # Let's use standard ranking for now.
            if previous_score is not None and app.match_score == previous_score:
                same_rank_count += 1
            else:
                # Update current rank based on how many same scores we had
                current_rank += same_rank_count
                same_rank_count = 1
                previous_score = app.match_score

            # If the rank has changed, update it.
            # Using current_rank directly as dense rank 
            # Wait, if we want dense rank (1, 2, 3 instead of 1, 2, 2, 4), we do:
            # if previous_score is not None and app.match_score != previous_score:
            #     current_rank += 1
            
            # Since the user requested 1, 2, 3, 4 sequentially, let's just do 1 to N.
            pass

    # Actually, the simplest is 1 to N based on the order.
    with transaction.atomic():
        rank = 1
        for app in applications:
            if app.rank != rank:
                app.rank = rank
                app.save(update_fields=['rank', 'updated_at'])
            rank += 1
