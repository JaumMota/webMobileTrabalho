# filepath: /home/jaum-mota/webMobileTrabalho/TodayHabits/habito/templatetags/habito_extras.py
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Permite o acesso a chaves de dicionário em templates.
    Uso: {{ meu_dicionario|get_item:minha_chave }}
    """
    return dictionary.get(key)