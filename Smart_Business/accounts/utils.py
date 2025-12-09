# accounts/utils.py

from django.conf import settings
from django.core.mail import send_mail


def send_business_status_email(business, action, admin_user=None):
    """
    Send email notification to the registered owner/user when a business is
    approved, rejected, or deleted.

    :param business: Business instance (must have .name and .owner.email or .owner_email)
    :param action: 'approved', 'rejected', or 'deleted'
    :param admin_user: request.user who performed the action (admin/superuser)
    """

    # Who should the owner contact for credentials / queries?
    contact_email = (
        getattr(admin_user, "email", None)
        if admin_user and getattr(admin_user, "email", None)
        else getattr(settings, "DEFAULT_FROM_EMAIL", None)
    )

    # Determine recipient email (owner/registered user)
    recipient = getattr(business, "owner_email", None) or getattr(
        getattr(business, "owner", None), "email", None
    )

    if not recipient:
        # No email available, nothing to send
        return

    subject = ""
    message = ""

    if action == "approved":
        subject = f"Business Approved: {business.name}"
        message = (
            f"Dear Owner,\n\n"
            f"Your business '{business.name}' has been APPROVED.\n\n"
            f"For business login credentials, please contact the admin "
            f"or the email: {contact_email}.\n\n"
            f"Regards,\n"
            f"Admin Team"
        )

    elif action == "rejected":
        subject = f"Business Rejected: {business.name}"
        message = (
            f"Dear Owner,\n\n"
            f"Your request for registering the business '{business.name}' "
            f"has been REJECTED.\n\n"
            f"Reason: Terms indicating a financial obligation is expected to own the Business.\n\n"
            f"If you have any questions, please contact {contact_email}.\n\n"
            f"Regards,\n"
            f"Admin Team"
        )

    elif action == "deleted":
        subject = f"Business Removed: {business.name}"
        message = (
            f"Dear Owner,\n\n"
            f"Your business '{business.name}' has been REMOVED from our system.\n\n"
            f"Reason: Overlong due payment and technical concerns.\n\n"
            f"For further clarification, please contact {contact_email}.\n\n"
            f"Regards,\n"
            f"Admin Team"
        )

    else:
        # Unknown action, do nothing
        return

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", None),
        [recipient],
        fail_silently=False,
    )
