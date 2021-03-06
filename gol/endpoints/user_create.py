from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.views.decorators.csrf import csrf_exempt
import csv

"""
Get data from ntrophy db with this request:
SELECT user_login, display_name, user_email FROM `wp_ntrophy_users`
Do not forget to filter output.
"""


@login_required
@require_http_methods(['POST'])
@permission_required('add_user', 'change_user')
@csrf_exempt
def user_create(request, *args, **kwargs):
    body = request.body.decode('utf-8')
    users = []
    for line in csv.reader(body.split('\n')):
        login, teamname, email = line

        u = User(
            username=login,
            first_name=teamname,
            email=email,
            is_active=True,
        )
        u.pwd = (User.objects.make_random_password(), )
        u.set_password(u.pwd[0])
        users.append(u)

    User.objects.bulk_create(users)

    mails = [
        ('[N-trophy 2020] Logika: přístupové údaje',
         'Přístupové údaje k webu https://logika.ntrophy.cz/ pro tým %s '
         'jsou:\n\n  * login: %s\n  * heslo: %s\n\nS pozdravem,\n'
         'tým logiky N-trophy' %
            (user.first_name, user.username, user.pwd[0]),
         'logika@ntrophy.cz',
         [user.email])
        for user in users
    ]
    send_mass_mail(
        mails,
        fail_silently=True
    )

    return JsonResponse(
        {user.username: user.pwd[0] for user in users}
    )
