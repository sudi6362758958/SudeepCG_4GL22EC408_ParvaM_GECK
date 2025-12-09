# accounts/middleware.py
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect


class AutoLogoutMiddleware:
    """
    Role-based auto logout:
      - Admin (is_superuser): 20 minutes
      - Owner (is_staff but not superuser): 30 minutes
      - Normal user: 40 minutes

    👉 If you want SAME timeout (e.g. 20 min) for admin & owner, just
       change the values in get_timeout_for_user().
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_timeout_for_user(self, user) -> int:
        """Return timeout in seconds based on user role."""
        if user.is_superuser:
            return 20 * 60  # Admin: 20 minutes
        if user.is_staff:
            return 1 * 60  # Owner: 30 minutes
        return 1 * 60      # Other users: 40 minutes

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            timeout = self.get_timeout_for_user(user)
            now_ts = timezone.now().timestamp()
            last_activity = request.session.get("last_activity")

            if last_activity is not None:
                elapsed = now_ts - float(last_activity)
                if elapsed > timeout:
                    # Session expired for this role
                    logout(request)
                    # change 'login' to your login URL name if different
                    return redirect("accounts:login")


            # Update session info for JS & next requests
            request.session["last_activity"] = now_ts
            request.session["session_timeout"] = timeout

        response = self.get_response(request)
        return response
