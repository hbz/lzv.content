# -*- coding: utf-8 -*-
from lzv.content import _
from plone.app.textfield import RichText
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema
from Products.Five import BrowserView

class IService(model.Schema):
    """An lzv service
    """

    details = RichText(
        title=_(u"Detailbeschreibung"),
        description=_("Detailierte Beschreibung des Services.")
    )

@indexer(IService)
def serviceDetailsIndexer(obj):
    return obj.details.raw


class ProjectView(BrowserView):
    """ A lzv service
    """

