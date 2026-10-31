"""
Sitemaps for SEO - Helps search engines (Google, Bing, Copilot) discover and index all content.
Complies with Bing Webmaster Guidelines and Google Search Essentials.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from property.models import Property, Developer
from shop.models import Product
from blogs.models import Post
from bookings.models import Apartment
from agents.models import Agent
from valpaint.models import ValpaintProduct


class PropertySitemap(Sitemap):
    """Sitemap for verified property listings"""
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Property.objects.filter(is_active=True).select_related('city', 'state')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at

    def location(self, obj):
        return f'/property/details/{obj.slug}/'


class DeveloperSitemap(Sitemap):
    """Sitemap for real estate developer profiles and portfolios"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Developer.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at

    def location(self, obj):
        return f'/developers/{obj.slug}/'


class ApartmentSitemap(Sitemap):
    """Sitemap for short let apartments"""
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Apartment.objects.filter(status='available')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at

    def location(self, obj):
        return f'/bookings/apartment/{obj.slug}/'


class AgentSitemap(Sitemap):
    """Sitemap for verified real estate agents"""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Agent.objects.filter(is_active=True, verification_status='verified')

    def lastmod(self, obj):
        return obj.updated if hasattr(obj, 'updated') and obj.updated else obj.created

    def location(self, obj):
        return f'/agents/{obj.slug}/'


class ProductSitemap(Sitemap):
    """Sitemap for shop products"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_available=True).select_related('category')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at

    def location(self, obj):
        return f'/shop/product/{obj.slug}/'


class ValpaintProductSitemap(Sitemap):
    """Sitemap for Valpaint decorative paint products"""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ValpaintProduct.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at

    def location(self, obj):
        return f'/valpaint/products/{obj.slug}/'


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published').select_related('author', 'category')

    def lastmod(self, obj):
        return obj.updated if hasattr(obj, 'updated') and obj.updated else obj.publish

    def location(self, obj):
        return f'/blog/details/{obj.publish.year}/{obj.publish.month}/{obj.publish.day}/{obj.slug}/'


class StaticPagesSitemap(Sitemap):
    """Sitemap for all core public and ecosystem pages"""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'faq',
            'privacy_policy',
            'properties',
            'developers_list',
            'agents',
            'agents:agent_search',
            'post_list',
            'shop:product_list',
            'apartment_list',
            'listings:pricing',
            'valpaint_home',
            '/valpaint/products/',
            'services:all_services',
            'services:brokerage',
            'services:businesses',
            'services:academy',
            'services:tourism',
            'services:interior_design_request',
            'events:all-events',
        ]

    def location(self, item):
        if item.startswith('/'):
            return item
        return reverse(item)
