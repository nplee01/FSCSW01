from django import template
from django.conf import settings

register = template.Library()

####################################################################
# Tag to get application name, used in base_site.html.
# Usage : {% get_app_name %}
class AppNameNode(template.Node):

    def __init__(self):
        pass

    def render(self, context):
        return settings.APP_NAME
        
@register.tag
def get_app_name(parser, token):

    token_list = token.split_contents()
    # We expect 1 elements : tag_name only
    if len(token_list) != 1:
        raise template.TemplateSyntaxError(("get_app_name tag expects no params"))
    else:
        return AppNameNode()
 
