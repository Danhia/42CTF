from authlib.integrations.django_client import OAuth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.defaults import bad_request
from django.urls import reverse
from django.shortcuts import redirect
import os

oauth = OAuth()

oauth.register(
    name='discord',
    client_id=os.getenv('OAUTH2_DISCORD_CLIENT_ID'),
    client_secret=os.getenv('OAUTH2_DISCORD_CLIENT_SECRET'),
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize',
    client_kwargs={'scope': 'identify'},
    api_base_url='https://discord.com/api/'
)

@login_required
@require_POST
def connect(request):
    if request.user.userprofileinfo.discord_id:
        return bad_request(request, "Already connected")
    redirect_uri = reverse('accounts:connections-connect-discord-authorize')
    redirect_uri = request.build_absolute_uri(redirect_uri)
    print(redirect_uri)
    return oauth.discord.authorize_redirect(request, redirect_uri)

@login_required
def authorize(request):
    if request.user.userprofileinfo.discord_id:
        return bad_request(request, "Already connected")
    token = oauth.discord.authorize_access_token(request)
    response = oauth.discord.get('users/@me', token=token)
    response = response.json()
    discord_id = response['id']
    request.user.userprofileinfo.discord_id = discord_id
    request.user.userprofileinfo.save()
    return redirect('accounts:edit')

@login_required
@require_POST
def disconnect(request):
    if not request.user.userprofileinfo.discord_id:
        return bad_request(request, "Already disconnected")
    request.user.userprofileinfo.discord_id = None
    request.user.userprofileinfo.save()
    return redirect('accounts:edit')
