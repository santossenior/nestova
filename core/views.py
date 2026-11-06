from django.shortcuts import render

# Create your views here.


def about_page(request):
    context = {
        'page_title': "About Nestova — Nigeria's Most Trusted Real Estate Brokerage",
        'meta_description': (
            "Learn about Nestova, our mission to redefine Nigerian real estate with "
            "verified properties, trusted agents, short lets, and innovative property technology."
        ),
    }
    return render(request, "estate/about.html", context)


def properties_page(request):
    context = {
        'page_title': "Search Properties for Sale & Rent in Nigeria | Nestova",
        'meta_description': (
            "Browse verified properties for sale and rent across Nigeria. Find apartments, "
            "houses, commercial spaces, and land in Lagos, Abuja, Port Harcourt and more."
        ),
    }
    return render(request, "estate/properties.html", context)


def agents(request):
    """Display all verified agents"""
    from agents.models import Agent
    from django.core.paginator import Paginator
    
    # Get all verified agents
    agents_list = Agent.objects.filter(
        is_active=True,
        verification_status='verified'
    ).select_related('user').order_by('-created')
    
    # Pagination
    paginator = Paginator(agents_list, 12)  # 12 agents per page
    page_number = request.GET.get('page')
    agents = paginator.get_page(page_number)
    
    # Get featured agent (first verified agent or None)
    featured_agent = agents_list.first() if agents_list.exists() else None
    
    context = {
        'agents': agents,
        'featured_agent': featured_agent,
        'total_agents': agents_list.count(),
        'page_title': "Verified Real Estate Agents in Nigeria | Nestova Realtors",
        'meta_description': (
            "Connect with verified real estate agents and realtors in Nigeria. "
            "Find experienced professionals in Lagos, Abuja, Port Harcourt, and beyond."
        ),
    }
    
    return render(request, "estate/agents.html", context)


def agents_details(request):
    return render(request, "estate/agent-profile.html")


def service(request):
    context = {
        'page_title': "The Nestova Ecosystem — Brokerage, Businesses, Academy & Tourism",
        'meta_description': (
            "Explore the Nestova Ecosystem — 4 powerful pillars: Brokerage, "
            "Businesses, Academy, and Tourism. One vision. Infinite possibilities."
        ),
    }
    return render(request, "estate/services.html", context)


def service_detail_page(request):
    return render(request, "estate/service-details.html")


def contact(request):
    context = {
        'page_title': "Contact Nestova — Real Estate Inquiries & Office Locations",
        'meta_description': (
            "Get in touch with Nestova. Reach our customer care, property advisory team, "
            "and office locations in Lagos and across Nigeria."
        ),
    }
    return render(request, "estate/contact.html", context)


def properties_details(request):
    return render(request, "estate/property-details.html")


def dashboard_user(request):
    return render(request, "estate/dashboard.html")


def faq(request):
    context = {
        'page_title': "Frequently Asked Questions (FAQ) | Nestova",
        'meta_description': (
            "Find answers to frequently asked questions about buying, renting, "
            "short lets, listing property, agent verification, and payments on Nestova."
        ),
    }
    return render(request, "estate/faq.html", context)


def privacy_policy(request):
    context = {
        'page_title': "Privacy Policy | Nestova",
        'meta_description': (
            "Read Nestova's Privacy Policy. Understand how we collect, use, "
            "and protect your personal data across our real estate platform."
        ),
    }
    return render(request, "estate/privacy.html", context)


def return_policy(request):
    context = {
        'page_title': "Return & Refund Policy | Nestova Shop",
        'meta_description': (
            "Nestova Shop return and refund policy. Return eligible items within 7 days "
            "of delivery. Free return shipping on defective or incorrect items."
        ),
        'structured_data': True,  # Suppress the generic org JSON-LD from seo_meta.html
    }
    return render(request, "shop/return_policy.html", context)
