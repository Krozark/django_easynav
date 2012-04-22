from modeltranslation.translator import translator, TranslationOptions
from easynav.models import *

class ItemMenuTranslation(TranslationOptions):
    fields = ('name',)
translator.register(ItemMenu, ItemMenuTranslation)
