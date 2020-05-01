from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def manager_required(function=None, redirect_field=REDIRECT_FIELD_NAME, login_url='properties:home'):
    '''
    Decorator for views that check that the logged in user
    is a manager or redirects to login page.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_account_manager,
        login_url=login_url,
        redirect_field_name=redirect_field
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_or_manager_required(function=None, redirect_field=REDIRECT_FIELD_NAME, login_url='properties:home'):
    '''
    Decorator for views that check that the logged in user
    is a staff or redirects to login page.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff or u.is_account_manager,
        login_url=login_url,
        redirect_field_name=redirect_field
    )

    if function:
        return actual_decorator(function)
    return actual_decorator