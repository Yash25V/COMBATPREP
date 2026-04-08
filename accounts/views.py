from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from records.models import SoldierProfile, Assessment
from accounts.models import User
from .forms import CustomUserCreationForm
import random
import string

@login_required
def dashboard(request):
    user = request.user
    
    if not user.is_email_verified and not user.is_superuser:
        return redirect('verify_email')
        
    context = {}
    
    if user.is_admin():
        context['total_users'] = User.objects.count()
        context['total_soldiers'] = User.objects.filter(role='SOLDIER').count()
        context['total_assessments'] = Assessment.objects.count()
        context['all_soldiers'] = User.objects.filter(role='SOLDIER').order_by('username')
        context['all_officers'] = User.objects.filter(role='OFFICER').order_by('username')
        context['all_assessments'] = Assessment.objects.all().order_by('-date_recorded')
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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = ''.join(random.choices(string.digits, k=6))
            user.verification_code = code
            user.save()
            
            try:
                send_mail(
                    'Your CombatPrep Verification Code',
                    f'Your email verification code is: {code}',
                    settings.EMAIL_HOST_USER or 'noreply@combatprep.com',
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                pass # Just pass for console backend or errors

            login(request, user)
            return redirect('verify_email')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def verify_email(request):
    if request.user.is_email_verified or request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        code = request.POST.get('code')
        if code and code == request.user.verification_code:
            request.user.is_email_verified = True
            request.user.verification_code = None
            request.user.save()
            messages.success(request, 'Email verified successfully! Welcome to your dashboard.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
            
    return render(request, 'registration/verify_email.html')
