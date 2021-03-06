from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"