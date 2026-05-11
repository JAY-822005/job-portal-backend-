"""
Utility functions for the Job Portal API.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_email(subject, recipient_email, template_name, context):
    """
    Send email using Django's email backend.
    
    Args:
        subject (str): Email subject
        recipient_email (str): Recipient email address
        template_name (str): Template file name
        context (dict): Template context
    """
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            'from@example.com',
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False


def generate_unique_slug(model, name):
    """
    Generate a unique slug from a given name.
    
    Args:
        model: Django model class
        name (str): Name to convert to slug
        
    Returns:
        str: Unique slug
    """
    from django.utils.text import slugify
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug
