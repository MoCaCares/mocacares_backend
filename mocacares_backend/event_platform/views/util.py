import threading
from django.core.mail import EmailMessage
from django.core.mail import send_mail


class EmailThread(threading.Thread):  # TODO: move to util.py
    def __init__(self, subject, content, receiver_list):
        self.subject = subject
        self.content = content
        self.receiver_list = receiver_list
        super(EmailThread, self).__init__()

    def run(self):
        send_mail(
            self.subject, 
            self.content, 
            'noreply@mocacares.com',
            self.receiver_list, 
            fail_silently=False
        )
        # context = {
        #     'team': self.team,
        #     'members': self.team.member_set.all(),
        # }
        # content = render_to_string('form/team_email.html', context)
        # email = EmailMessage(
            # subject=self.subject,
            # body=self.content,
            # to=self.receiver_list,
            # cc=['']
        # )
        # email.content_subtype = "html"
        # email.send(fail_silently=False)

def validate_user_type(user_type):
    return user_type == '1' or user_type == '2'


def validate_email_format(email):
    return True


def validate_password_format(password):
    return len(password) >= 6
