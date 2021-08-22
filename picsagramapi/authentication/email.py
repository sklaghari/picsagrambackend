from djoser import email
class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'