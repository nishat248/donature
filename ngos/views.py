from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign, NGODonation
from .forms import CampaignForm, NGODonationForm
from ngos.models import Campaign, CampaignCategory, NGOProfile,NGODonation, CampaignUpdate
from donations.models import User, UserReward
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils import timezone
from django.db.models import Q, Count,F

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from .models import NGODonation
from donations.models import Notification
from django.urls import reverse

@login_required
def create_campaign(request):
    if request.user.user_type != 'ngo':
        messages.error(request, "Only NGOs can create campaigns.")
        return redirect('home')

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.ngo = request.user
            campaign.status = 'pending'  # require admin approval
            campaign.save()
            messages.success(request, "Campaign submitted for admin approval.")
            return redirect('my_campaigns')
    else:
        form = CampaignForm()

    return render(request, "ngos/create_campaign.html", {"form": form})

@login_required
def edit_campaign(request, campaign_id):
    if request.user.user_type != 'ngo':
        messages.error(request, "Only NGOs can edit campaigns.")
        return redirect('home')

    campaign = get_object_or_404(Campaign, id=campaign_id, ngo=request.user)

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            updated_campaign = form.save(commit=False)
            updated_campaign.ngo = request.user  # ensure same ngo
            updated_campaign.status = 'pending'  # আবার approval লাগতে পারে
            updated_campaign.save()
            messages.success(request, "Campaign updated successfully (pending approval).")
            return redirect('my_campaigns')
    else:
        form = CampaignForm(instance=campaign)

    return render(request, "ngos/edit_campaign.html", {"form": form, "campaign": campaign})


@login_required
def delete_campaign(request, campaign_id):
    if request.user.user_type != 'ngo':
        messages.error(request, "Only NGOs can delete campaigns.")
        return redirect('home')

    campaign = get_object_or_404(Campaign, id=campaign_id, ngo=request.user)

    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Campaign deleted successfully.")
        return redirect('my_campaigns')

    return redirect('my_campaigns')




@login_required
def my_campaigns(request):
    if request.user.user_type != 'ngo':
        messages.error(request, "Only NGOs can view their campaigns.")
        return redirect('home')

    campaigns = Campaign.objects.filter(ngo=request.user)
    return render(request, "ngos/my_campaigns.html", {"campaigns": campaigns})








def explore_campaigns(request):
    # Filters
    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category')
    selected_location = request.GET.get('location')
    selected_ngo = request.GET.get('ngo')

    # Only approved, active campaigns that haven't ended yet OR have no end date
    campaigns = Campaign.objects.filter(
        status='approved',
        is_active=True
    ).filter(
        Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True)
    )

    # Apply filters
    if search_query:
        campaigns = campaigns.filter(title__icontains=search_query)
    if selected_category:
        campaigns = campaigns.filter(category__id=selected_category)
    if selected_location:
        campaigns = campaigns.filter(ngo__ngoprofile__city_postal=selected_location)
    if selected_ngo:
        campaigns = campaigns.filter(ngo__id=selected_ngo)

    # Annotate donors count
    campaigns = campaigns.annotate(donors_count=Count('donations'))

    # Calculate progress percent
    for campaign in campaigns:
        campaign.progress_percent = 0
        if campaign.goal_amount and campaign.goal_amount > 0:
            campaign.progress_percent = (campaign.collected_amount / campaign.goal_amount) * 100

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(campaigns, 9)
    page_number = request.GET.get('page')
    campaigns_page = paginator.get_page(page_number)

    # Dropdown filters
    categories = CampaignCategory.objects.all()
    locations = NGOProfile.objects.values_list('city_postal', flat=True).distinct()
    ngos = NGOProfile.objects.filter(user__is_approved=True)

    context = {
        'campaigns': campaigns_page,
        'categories': categories,
        'locations': locations,
        'ngos': ngos,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_location': selected_location,
        'selected_ngo': selected_ngo,
    }

    return render(request, 'ngos/explore_campaigns.html', context)



def campaign_detail(request, campaign_id):
    # Get campaign
    campaign = get_object_or_404(
        Campaign.objects.annotate(
            donors_count=Count('donations'),
            total_raised=Sum('donations__amount')
        ),
        id=campaign_id,
        status='approved',
        is_active=True
    )


    # Calculate fundraising progress
    campaign.progress_percent = 0
    if campaign.goal_amount and campaign.goal_amount > 0:
        raised = campaign.collected_amount or 0  
        campaign.progress_percent = round((raised / campaign.goal_amount) * 100, 2)


    # Donations for this campaign
    donations = NGODonation.objects.filter(campaign=campaign).order_by('-donated_at')

    # Updates for this campaign (optional)
    updates = CampaignUpdate.objects.filter(campaign=campaign).order_by('-created_at')

    context = {
        'campaign': campaign,
        'donations': donations,
        'updates': updates,
    }

    return render(request, 'ngos/campaign_detail.html', context)







@login_required
def donate_to_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, status="approved", is_active=True)

    # Prevent NGO donating to own campaign
    if request.user == campaign.ngo:
        messages.error(request, "⚠️ You cannot donate to your own campaign.")
        return redirect("campaign_detail", campaign_id=campaign.id)

    if request.method == "POST":
        form = NGODonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.campaign = campaign
            donation.donor = request.user
            donation.payer_name = form.cleaned_data['payer_name']
            donation.payment_method = form.cleaned_data['payment_method']
            donation.account_input = form.cleaned_data['account_input']
            donation.is_anonymous = form.cleaned_data['is_anonymous']
            donation.save()


            # add points to user
            user_reward, created = UserReward.objects.get_or_create(user=request.user)
            user_reward.add_points(30)  # 30 points for campaign donation

            # ✅ NGO notification
            Notification.objects.create(
                user=campaign.ngo,
                message=f"{request.user.username} donated ৳{donation.amount} to your campaign '{campaign.title}'",
                link=reverse('campaign_detail', args=[campaign.id])
            )

            messages.success(request, "✅ Thank you for your donation!")
            return redirect("donation_success", donation_id=donation.id)

    else:
        form = NGODonationForm()

    return render(request, "ngos/donate_to_campaign.html", {
        "campaign": campaign,
        "form": form
    })


@login_required
def donation_success(request, donation_id):
    donation = get_object_or_404(NGODonation, id=donation_id, donor=request.user)

    context = {
        "donation": donation
    }
    return render(request, "ngos/donation_success.html", context)





def download_receipt(request, donation_id):
    donation = get_object_or_404(NGODonation, id=donation_id, donor=request.user)

    template = get_template("ngos/receipt_pdf.html")
    html = template.render({"donation": donation})

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="receipt_{donation.id}.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)




@login_required
def add_campaign_update(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Only NGO owner can add updates
    if request.user != campaign.ngo:
        messages.error(request, "You are not authorized to add updates to this campaign.")
        return redirect('campaign_detail', campaign_id=campaign.id)

    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')

        if title and message:
            CampaignUpdate.objects.create(
                campaign=campaign,
                title=title,
                message=message
            )
            messages.success(request, "Update added successfully!")
        else:
            messages.error(request, "Both title and message are required.")

    return redirect('campaign_detail', campaign_id=campaign.id)


@login_required
def ngo_donation_history(request):
    # Only allow NGO users
    if request.user.user_type != 'ngo':
        return render(request, '403.html')  # or redirect with message

    # Get all donations to campaigns of this NGO
    donations = NGODonation.objects.filter(campaign__ngo=request.user).order_by('-donated_at')

    context = {
        'donations': donations,
    }
    return render(request, 'ngos/donation_history.html', context)




