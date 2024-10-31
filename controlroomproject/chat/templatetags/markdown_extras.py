from django import template
import markdown as md

register = template.Library()


@register.filter
def markdown_filter(value):
    return md.markdown(value, extensions=["fenced_code", "tables"])
