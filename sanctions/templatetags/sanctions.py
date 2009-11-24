from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def labelled(obj, attribute):
    val = unicode(getattr(obj, attribute, ''))
    if not val:
        return ''
    else:
        if val.startswith('http'):
            val = u'<a href="%s">%s</a>' % (val, val)
        return mark_safe(u'<b>%s</b>: %s<br>' % (attribute.capitalize().replace("_", " "), val))