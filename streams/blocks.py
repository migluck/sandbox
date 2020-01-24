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
