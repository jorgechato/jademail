from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces import views
from .forms import LoginForm


class LoginView(
        views.AnonymousRequiredMixin,
        generic.FormView):

    form_class = LoginForm
    success_url = reverse_lazy('grid:home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutView(
        views.LoginRequiredMixin,
        generic.RedirectView):

    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
