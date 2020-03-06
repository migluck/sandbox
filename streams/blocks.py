"""Streamfields live in here."""
from wagtail.admin import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text block."""
    
    title = blocks.CharBlock(required=True, help_text='Add your title.')    
    text = blocks.TextBlock(required=True, help_text='Add additional text.')
    
    class Meta: # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichTextBlock(blocks.RichTextBlock):
    """Rich text block with all features"""
    
    class Meta: # noqa
        template = "streams/rich_text_block.html"
        icon = "edit"
        label = "Rich Text"

class SimpleTextBlock(blocks.RichTextBlock):
    """Rich text block with limited features"""
    
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):                
        super().__init__(**kwargs)    
        self.features = [
            "bold",
            "italic",
            "link"
            ]
    
    class Meta: # noqa
        template = "streams/rich_text_block.html"
        icon = "edit"
        label = "Simple Text"
        
        
class CardBlock(blocks.StructBlock):
    """Cards with image, text, and buttons."""
    title = blocks.CharBlock(required=True, help_text="Add your title.")
    cards = blocks.ListBlock(
            blocks.StructBlock(
                    [("image", ImageChooserBlock(required=True, help_text="Add your title.")),
                     ("title", blocks.CharBlock(required=True, max_length=40)),
                     ("text", blocks.TextBlock(required=True, max_length=200)),
                     ("button_page", blocks.PageChooserBlock(required=False)),
                     ("button_url", blocks.URLBlock(required=False, help_text="If button_page selected use that first."))                                              
                     ]
                )
        )
    
    class Meta: # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Block Cards"      

class CTABlock(blocks.StructBlock):
    """A simple call to action section."""
    title = blocks.CharBlock(required=True, max_length=60)
    text = RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=40)
     
    class Meta: # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"

class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls"""
    def URL(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")
    
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

class ButtonBlock(blocks.StructBlock):
    """An internal or external URL"""
    button_text =  blocks.CharBlock(required=True, max_length=60)
    button_page = blocks.PageChooserBlock(required=False, help_text="Use this internal URL if exists")
    button_url = blocks.URLBlock(required=False, help_text="Use this external URL if no internal URL assigned")
        
    class Meta: # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"  
        value_class = LinkStructValue      