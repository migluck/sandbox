"""Flexible page."""
from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from streams import blocks

# Create your models here.
class FlexPage(Page):
    """Flexible page class."""
    
    template = "flex/flex_page.html"
        
    content = StreamField(
        [
                ("title_and_text", blocks.TitleAndTextBlock()),
                ("rich_text", blocks.RichTextBlock()),
                ("simple_text", blocks.SimpleTextBlock()),
        ],
        null=True,
        blank=True
        )
    
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    
    content_panels = Page.content_panels + [
            FieldPanel("subtitle"),
            StreamFieldPanel("content")
        ]
    
    class Meta: # noqa
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
        
                                