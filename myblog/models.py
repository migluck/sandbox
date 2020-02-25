from django.db import models
from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from streams import blocks

# Create your models here.

class MyblogListingPage(RoutablePageMixin, Page):
    """"List all the MyBlog Detail Pages"""
    
    template = "myblog/myblog_listing_page.html"
    
    custom_title = models.CharField(
                                max_length=100, 
                                blank=False, 
                                null=False, 
                                help_text="Overwrites default title")
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = MyblogDetailPage.objects.live().public()
        context["regular_context_var"] = "Hello world 123123"
        context["special_link"] = self.reverse_subpage('latest_posts')
        return context
    
    content_panels = Page.content_panels + [
            FieldPanel("custom_title"),
        ]
    
    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = self.get_context(request, *args, **kwargs)
        context["latest_posts"] = MyblogDetailPage.objects.live().public()[:1]        
        return render(request, "myblog/latest_posts.html", context)
    
class MyblogDetailPage(Page):
    """Blog detail page"""
    
    template = "myblog/myblog_detail_page.html"
    
    custom_title = models.CharField(
            max_length=100,
            blank=False,
            null=False,
            help_text="Overwrites default title"        
        )
    
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,        
        on_delete=models.SET_NULL,
        related_name="+"
        )
    
    content = StreamField(
        [
                ("title_and_text", blocks.TitleAndTextBlock()),
                ("rich_text", blocks.RichTextBlock()),
                ("simple_text", blocks.SimpleTextBlock()),
                ("cards", blocks.CardBlock()),
                ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
        )
    
    content_panels = Page.content_panels + [
            FieldPanel("custom_title"),
            ImageChooserPanel("blog_image"),
            StreamFieldPanel("content")
        ]
    