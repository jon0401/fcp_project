from django.shortcuts import render, get_object_or_404,redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login,logout
from django.views.generic import View
import warnings
from django.core.urlresolvers import reverse,resolve
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.shortcuts import resolve_url
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .form import MemberForm,UpdateForm, MemberDetailForm
from .models import Member
from django.core.urlresolvers import reverse_lazy

def logout_view(request):
    logout(request)
    return redirect('home')

class UserFormView(View):
    form_class = MemberForm
    form_class2 = MemberDetailForm
    template_name = 'users/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        form.prefix = 'form'
        form2 = self.form_class2(None)
        form2.prefix = 'form2'
        return render(request, self.template_name,{'form': form, 'form2': form2})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, prefix = 'form')
        form2 = self.form_class2(request.POST, request.FILES, prefix='form2')

        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            memberUser = form2.save(commit=False)

            member = Member()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            member.avatar = form2.cleaned_data['avatar']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            member = Member(user=user, display_name=username, avatar= member.avatar)
            member.save()

            if user is not None:
                if user.is_active:

                    login(request,user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form, 'form2': form2})

class UserUpdate(UpdateView):
    form_class = UpdateForm
    model = Member

    def get_queryset(self):
        return Member.objects.all()

    def get_object(self, queryset=None):
        return self.request.user.member

    success_url = reverse_lazy('home')


def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('users:password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                    RemovedInDjango20Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
        'current_app': (resolve(request.path).app_name),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)

def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('users:password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
        'current_app': (resolve(request.path).app_name),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)