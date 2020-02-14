from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks

# Create your models here.

class MyblogListingPage(Page):
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
        return context
    
    content_panels = Page.content_panels + [
            FieldPanel("custom_title"),
        ]
    
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
    