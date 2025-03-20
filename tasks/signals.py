from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Event

@receiver(post_save, sender=Event)
def notify_participants_on_event_creation(sender, instance, created, **kwargs):
    if created:
        participants = instance.participants.all() 
        assigned_email = [p.email for p in participants]

        if assigned_email:
            try:
                send_mail(
                    "New Event Created",
                    f"Dear Participant,\n\nA new event '{instance.name}' has been created.\n\n"
                    f"📍 Location: {instance.location}\n"
                    f"📅 Date: {instance.date}\n"
                    f"⏰ Time: {instance.time}\n\n"
                    "Regards,\nEvent Team",
                    settings.EMAIL_HOST_USER,
                    assigned_email,
                    fail_silently=False
                )
                
            except Exception as e:
                print(f"❌ Error sending email: {e}")
        else:
            print("⚠️ No participants found to send email.")


@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_addition(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        participants = instance.participants.filter(pk__in=pk_set)

        for participant in participants:
            assigned_email = [p.email for p in participants]

            if participant:
                try:
                    send_mail(
                        "You have been added to an event",
                        f"Dear Participant,\n\nYou have been added to the event '{instance.name}'.\n\n"
                        f"📍 Location: {instance.location}\n"
                        f"📅 Date: {instance.date}\n"
                        f"⏰ Time: {instance.time}\n\n"
                        "Regards,\nEvent Team",
                        settings.EMAIL_HOST_USER,
                        assigned_email,
                        fail_silently=False
                    )
                    print(f"Notification email sent successfully to: {assigned_email}")
                except Exception as e:
                    print(f"❌ Error sending email: {e}")
            else:
                print("No participants found to notify.")


@receiver(post_delete, sender=Event)
def delete_event(sender, instance, **kwargs):
    print(f"Event '{instance.name}' deleted successfully!")