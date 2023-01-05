from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages  # import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, CreateView
from .forms import ResearchOrganizationHTMX
from django.views.generic.edit import FormView
import requests
from .models import Organization


class RegisterAffiliations(LoginRequiredMixin, FormView):
    template_name = 'ror/register_affiliations.html'
    form_class = ResearchOrganizationHTMX

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Organization.objects.get_for_user(
            self.request.user)
        return context

    def form_valid(self, form):
        obj, created = Organization.objects.update_or_create(
            id=form.cleaned_data['id'],
            defaults=form.cleaned_data)

        # if not obj.is_member(self.request.user):
        obj.get_or_add_user(self.request.user)
        # else:
        # self.message_user()

        context = {
            "org": obj,
            "created": created,
        }
        return render(
            self.request, 'ror/components/affiliation.html', context=context)


def about(request):
    context = dict()
    return render(request, 'ror/about.html', context=context)
