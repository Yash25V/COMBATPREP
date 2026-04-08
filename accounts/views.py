from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from records.models import SoldierProfile, Assessment
from accounts.models import User

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.is_admin():
        context['total_users'] = User.objects.count()
        context['total_soldiers'] = User.objects.filter(role='SOLDIER').count()
        context['total_assessments'] = Assessment.objects.count()
    elif user.is_officer():
        context['total_soldiers'] = User.objects.filter(role='SOLDIER').count()
        context['recent_assessments'] = Assessment.objects.filter(officer=user).order_by('-date_recorded')[:5]
    elif user.is_soldier():
        try:
            profile = user.profile
        except SoldierProfile.DoesNotExist:
            profile = SoldierProfile.objects.create(user=user)
        context['profile'] = profile
        context['assessments'] = user.assessments.order_by('-date_recorded')
        
    return render(request, 'dashboard.html', context)
