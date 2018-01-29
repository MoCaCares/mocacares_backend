import threading
from django.core.mail import EmailMessage

class EmailThread(threading.Thread):  # TODO: move to util.py
    def __init__(self, subject, content, receiver_list):
        self.subject = subject
        self.content = content
        self.receiver_list = receiver_list
        super(EmailThread, self).__init__()

    def run(self):
        # context = {
        #     'team': self.team,
        #     'members': self.team.member_set.all(),
        # }
        # content = render_to_string('form/team_email.html', context)
        email = EmailMessage(
            subject=self.subject,
            body=self.content,
            to=self.receiver_list,
            # cc=['']
        )
        # email.content_subtype = "html"
        email.send(fail_silently=False)

class VerificationCodeInterface():
    pass
