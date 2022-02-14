from lzv.content import _
from zope import schema
#from z3c import form
from zope.interface import implementer
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName



# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class ILZVFurtherInformationPortlet(IPortletDataProvider):
    """A portlet wich displays contact information
    """

@implementer(ILZVFurtherInformationPortlet)      
class Assignment(base.Assignment):
    
    title = _(u"Weitere Informationen")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('further_information.pt')


class AddForm(base.NullAddForm):
    #form_fields = form.Fields(ILZVContactPortlet)
    label = _(u"Add FurtherInformation portlet")
    description = _(u"This portlet displays further information to LZV.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self):
        return Assignment()


