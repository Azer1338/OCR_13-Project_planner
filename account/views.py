from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from document.models import ContributorDeliverable
from project.models import ContributorProject
from .admin import ProjectPlannerUserCreationForm


@login_required(login_url="/accounts/logIn/")
def my_account_view(request):
    """
    Display user's information.
    :param request:
    :return:
    """

    return render(request, 'accounts/myAccount.html')


@login_required(login_url="/accounts/logIn/")
def my_contribution_view(request):
    """
    Display user's information.
    :param request:
    :return:
    """
    # Gather project information related to user
    projects = ContributorProject.objects. \
        filter(projectPlannerUser=request.user.id)
    deliverables = ContributorDeliverable.objects. \
        filter(projectPlannerUser=request.user.id) \
        .order_by('deliverable__dueDate')

    # Generate a context
    context = {
        'projects': projects,
        'deliverables': deliverables,
    }

    return render(request, 'accounts/myContribution.html', context)


def sign_up_view(request):
    """
    Sign Up as a new member
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ProjectPlannerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log in the user
            accounts_user = form.save()
            login(request, accounts_user)

            # Message
            messages.success(request, 'Welcome!')

            return redirect('project:index')
        else:
            # Message
            messages.warning(request, 'Some fields are not correct!')
    else:
        form = ProjectPlannerUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/signUp.html', context)


def log_in_view(request):
    """
    Return Log in page
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user
            user = form.get_user()
            login(request, user)

            # Message
            messages.success(request, 'Welcome back!')

            # Reroute the user to the previous page after log in
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                pass

                return redirect('project:index')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/logIn.html', {'form': form})


@login_required(login_url="/accounts/logIn/")
def log_out_view(request):
    logout(request)
    template = loader.get_template('project/index.html')

    # Message
    messages.success(request, 'Bye bye!')

    return HttpResponse(template.render(request=request))