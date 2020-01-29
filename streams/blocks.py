"""Streamfields live in here."""
from wagtail.admin import blocks

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