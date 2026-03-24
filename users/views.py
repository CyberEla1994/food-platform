from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm, UserRegisterForm, ProfileForm


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile_filled = user.first_name or user.last_name or user.phone
    show_edit_form = request.GET.get("edit") == "1"

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=user)

    show_form = not profile_filled or show_edit_form

    return render(request, "users/profile.html", {
        "form": form,
        "profile_filled": profile_filled,
        "show_form": show_form,
    })


@login_required
def avatar_delete(request):
    user = request.user
    if user.avatar:
        user.avatar.delete(save=True)
    return redirect("users:profile")


class PasswordChangeViewCustom(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change_form.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")