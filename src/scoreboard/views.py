from django.shortcuts import render
from django.core.paginator import Paginator
from accounts.models import UserProfileInfo

def scoreboard(request):
    scores      = UserProfileInfo.objects.filter(score__gt=0).select_related().order_by('-score', 'last_submission_date', 'user__username')
    paginator   = Paginator(scores, 20)
    page        = request.GET.get('page')
    scores_p    = paginator.get_page(page)
    return render(request, 'scoreboard/scoreboard.html', {'scores':scores_p})
        
# Create your views here.
