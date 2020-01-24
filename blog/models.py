from django.db import models

# Other imports
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

# Create your models here.
class BlogHomePage(Page):
    """Home page for blog application."""
    template = "blog/blog_home_page.html"    
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
            FieldPanel( 'body' )
        ]
    
class BlogIndexPage(Page):
    """Index of all the blog posts created."""
    templates = "home/blog_index_page"
    
    # Create new field
    subtitle = models.CharField(max_length=255, default="Recent Posts")
    body=RichTextField(blank=True)    
    
    content_panels = Page.content_panels + [
            FieldPanel('subtitle'),
            FieldPanel('body')
        ]
    
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
                              
    
class BlogPage(Page):
    """Page for individual blog posts."""
    date = models.DateField("Post date")
    summary = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
            FieldPanel('date'),
            FieldPanel('summary'),
            FieldPanel('body', classname="full")
        ]
