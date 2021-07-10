from django.shortcuts import render

from . import views

def auth_required(view_function):
    def wrapper(request):
        if request.user.is_authenticated:
            return view_function(request)
        else:
            context_dict = {'error_status': 1,
                        'error_msg': 'You need to login to access this feature',
                        'back_url': '/'}
            return render(request, 'MedBotApp/error.html', context=context_dict)
    return wrapper


def unauth_required(view_function):
    def wrapper(request):
        if request.user.is_authenticated:
            context_dict = {'error_status': 1,
                            # 'error_msg': '1',
                            'back_url': '/'}
            if view_function == views.user_register:
                context_dict['error_msg'] = 'You need to logout first to register'
            elif view_function == views.user_login:
                context_dict['error_msg'] = 'You are already logged in'
            else:
                context_dict['error_msg'] = 'You need to logout first.'
            return render(request, 'MedBotApp/error.html', context=context_dict)
        else:
            return view_function(request)
    return wrapper