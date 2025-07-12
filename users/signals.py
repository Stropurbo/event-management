# from django.db.models.signals import post_save, m2m_changed, post_delete
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.models import Group
# from django.contrib.auth.tokens import default_token_generator
# from users.models import CustomUser
# from django.contrib.auth import get_user_model
# from django.db import transaction
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.urls import reverse
# User = get_user_model()


# @receiver(post_save, sender=User)
# def send_activation_mail(sender, instance, created, **kwargs):
#     if created:
#         def send_mail_on_commit():
#             token = default_token_generator.make_token(instance)
#             uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))            

#             activation_path = reverse('activate_user', kwargs={'uidb64': uidb64, 'token': token})
#             activation_url = f"{settings.BACKEND_URL}{activation_path}"

#             subject = "Activate Your Account"
#             message = f'Hello {instance.username}, \n\nPlease activate your account by clicking this link:\n\n{activation_url}\n\nThank You!'
#             recipient_list = [instance.email]

#             try:
#                 send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#             except Exception as e:
#                 print(f"Failed to send activation email to {instance.email}: {str(e)}")

#         transaction.on_commit(send_mail_on_commit)


# # @receiver(post_save, sender=User)
# # def assign_role(sender, instance, created, **kwargs):
# #     if created:
# #         user_group, created = Group.objects.get_or_create(name='User')
# #         instance.groups.add(user_group)

# # @receiver(post_save, sender=User)
# # def create_or_update_profile(sender, instance, created, **kwargs):
# #     if not hasattr(instance, 'userprofile'):
# #             CustomUser.objects.create(user=instance) 