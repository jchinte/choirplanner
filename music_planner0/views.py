from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/generic_form.html"
    
    def get_success_url(self):
        return reverse('login_view')

class AdminUserUpdateView(UpdateView):
    model = User
    slug_field = 'username'
    form_class=UserChangeForm
    template_name = "registration/generic_form.html"

    @method_decorator(permission_required('auth.change_user'))
    def dispatch(self, *args, **kwargs):
        return super(AdminUserUpdateView, self).dispatch(*args, **kwargs)
    
class UserDetailView(DetailView):
    model = User
    tempate_name = "registration/user.html"
    slug_field = 'username'
