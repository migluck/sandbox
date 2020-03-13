from django.db import models
from django.shortcuts import render
from django import forms
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import InlinePanel
from streams import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.templatetags.wagtailadmin_tags import allow_unicode_slugs

 #############################################
 # ORDERABLE
 #############################################
# Create your models here.
class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors"""
    
    page = ParentalKey("myblog.MyblogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "myblog.MyBlogAuthor",
        on_delete=models.CASCADE
        )

    panels = [
            SnippetChooserPanel("author")
        ]


 #############################################
 # SNIPPET
 #############################################
class MyBlogAuthor(models.Model):
    """Blog author for snippets."""
    
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
        )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image"
        ),
        MultiFieldPanel(                
            [
                    FieldPanel("website")
            ],
            heading="Links"    
        )
    ]
    
    def __str__(self):
        """String wrapper of this class."""
        return self.name
    
    class Meta: # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"
        
register_snippet(MyBlogAuthor)

class MyBlogCategory(models.Model):
    """Blog category for a snippet"""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(
            verbose_name="slug",
            allow_unicode=True,
            max_length=255,
            help_text="A slug to identify posts by this category"
        )
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
        ]

    def __str__(self):
        return self.name

    class Meta: # noqa
        verbose_name = "My Blog Category"
        verbose_name_plural = "My Blog Categories"
        ordering=["name"]
        
register_snippet(MyBlogCategory)
                
 #############################################
 # PAGES
 #############################################

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
        context["categories"] = MyBlogCategory.objects.all()
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
    
    def get_sitemap_urls(self, request):
#         Uncomment to have no sitemap for this page        
#         return []
        sitemap = super().get_sitemap_urls(request)        
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9
            }
        )
        return sitemap
    
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
    
    categories = ParentalManyToManyField("myblog.MyBlogCategory", blank=True)
    
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
            MultiFieldPanel(
                [
                        InlinePanel("blog_authors", label="Author", min_num=1, max_num=5)
                ],
                heading="Author(s)"
            ),
            MultiFieldPanel(
                [
                    FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
                ],
                heading="categories"                                    
            ),
            StreamFieldPanel("content"), 
        ]
    