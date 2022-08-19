import sys
from typing import List, Optional
from lzv.content import _
from zope import schema
import plone.api as api
from zope.interface import implementer
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

if sys.version_info <= (3, 7):
    from typing_extensions import TypedDict
else:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from typing import TypedDict

from lzv.content.config import ACADEMICTITLES

class TItem(TypedDict):
    title: str
    url: str
    description: str
    academictitle: str
    email: str
    phone: str
    leadimage: Optional[str]

# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class ILZVContactPortlet(IPortletDataProvider):
    """A portlet wich displays contact information
    """

@implementer(ILZVContactPortlet)      
class Assignment(base.Assignment):
    
    title = _(u"LZV Kontakt")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('lzv_contact.pt')
        
    def get_academictitles(self):
        return {x[0]:x[1] for x in ACADEMICTITLES}


    def contact_data(self) -> List[TItem]:
        query = {
            "portal_type": ['lzv.contact'],
            "UID": "847e818adf7a49ffb4dd8eb6c77b364b"
        }

        items = list()
        for brain in api.content.find(**query):
            obj = brain.getObject()
            items.append({
                'title': brain.Title,
                'url': brain.getURL(),
                'description': brain.Description,
                'academictitle': obj.academictitle,
                'job': obj.job,
                'phone': obj.phone,
                'email': obj.email,
                'image_url': self.get_image_url(obj)
            })

        return items[0]

    @staticmethod
    def get_image_url(obj) -> Optional[str]:
        if getattr(obj, 'image', None):
            return obj.absolute_url() + "/@@images/image"

        return None






class AddForm(base.NullAddForm):
    #form_fields = form.Fields(ILZVContactPortlet)
    label = _(u"Add LZV Contact portlet")
    description = _(u"This portlet displays contact information.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self):
        return Assignment()


