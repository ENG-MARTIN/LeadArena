import africastalking
from django.conf import settings
import phonenumbers
from django.contrib.auth import get_user_model

User = get_user_model()

africastalking.initialize(
    settings.AFRICASTALKING_USERNAME,
    settings.AFRICASTALKING_API_KEY
)

voice = africastalking.Voice


import re
from datetime import datetime

def format_phone_to_e164(phone_number):
    if not phone_number:
        return None
    
    cleaned = re.sub(r'[^\d+]', '', str(phone_number).strip())
    
    if cleaned.startswith('0'):
        return f"+256{cleaned[1:]}"
    
    if cleaned.startswith('256') and not cleaned.startswith('+'):
        return f"+{cleaned}"
        
    if cleaned.startswith('+256') and len(cleaned) >= 13:
        return cleaned

    return None


def log_activity(user, action, description='', request=None, related_object_type='', related_object_id=None, metadata=None):
    """
    Helper function to log user activity.
    
    Usage:
        log_activity(request.user, 'lead_created', 'Created lead for John Doe', request, 'Lead', lead.id)
    """
    from .models import Activity
    
    ip_address = None
    user_agent = ''
    
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    
    Activity.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        related_object_type=related_object_type,
        related_object_id=related_object_id,
        metadata=metadata
    )