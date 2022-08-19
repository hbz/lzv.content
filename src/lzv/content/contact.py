# -*- coding: utf-8 -*-
from lzv.content import _
from plone.supermodel.directives import fieldset
from plone.app.textfield import RichText
from plone.indexer import indexer
from plone.schema import Email
from plone.supermodel import model
from plone.namedfile.field import NamedImage
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five import BrowserView
from lzv.content.config import ACADEMICTITLES

items = [SimpleTerm(value=key, title=value) for (key, value) in ACADEMICTITLES]
choice_academictitles = SimpleVocabulary(items)


class IContact(model.Schema):
    """A contact person"""

    job = schema.TextLine(
        title=_(u"Tätigkeit"),
        description=_("Tätigkeit.")
    )
    academictitle = schema.Choice(
        title=_(u"Akademischer Titel"),
        description=_("Akademischer Titel."),
        vocabulary=choice_academictitles,
        required=False
    )

    email = Email(
        title=_(u"Email"),
        description=_("Email.")
    )

    phone = schema.ASCIILine(
        title=_(u"Telefon"),
        description=_("Telefon."),
        required=False
    )

    image = NamedImage(
        title=_(u"Bild"),
        description=_("Bild."),
        required=False
    )

@indexer(IContact)
def contactEmailIndexer(obj):
    return obj.email



#class JobView(BrowserView):
#    """A contact"""



