from asyncio import events
from django.db import models

# Create your models here.


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Composit 22"),
        # message:
        email_plaintext_message,
        # from:
        "sailokesh.gorantla@ecell-iitkgp.org",
        # to:
        [reset_password_token.user.email]
    )


# 0. postsreg db - Lokesh
# 1. class Events: modal - Jay
# reset_password_link - Aditya
# confirmation mail - Abhyuday
# verification link - Abhyuday
# 5. rest api - Lokesh
# 6. scores leaderboard for events
