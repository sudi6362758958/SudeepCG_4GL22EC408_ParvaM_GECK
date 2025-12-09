# accounts/context_processors.py

def session_info(request):
    """
    Expose session timeout & last activity timestamp to templates
    for showing countdown and warning popup.
    """
    return {
        "session_timeout": request.session.get("session_timeout", 0),
        "session_last_activity": request.session.get("last_activity", 0),
    }

def current_business(request):
    """
    Keep this to satisfy the context processor reference:
    'accounts.context_processors.current_business'

    It provides 'business' and 'dashboard_url' to all templates.

    If your views already pass 'business' in the context,
    that will override this value where needed.
    """
    # If some middleware or view has set request.business, use it;
    # otherwise just return None so templates don't break.
    business = getattr(request, "business", None)

    return {
        "business": business,
        "dashboard_url": None,  # you can compute a real URL later if needed
    }

