import sys

from typing import List, Optional

import plone.api as api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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


class ContactsView(BrowserView):
    template = ViewPageTemplateFile("templates/contacts.pt")

    def __call__(self):
        return self.template(self)

    def get_academictitles(self):
        """Return a dict of acad. titles with abbreviations as keys."""

        return {x[0]:x[1] for x in ACADEMICTITLES}
        
    def _chunkify(self, items, chunk_size=2):
        """Return a list as chunks of given size."""

        chunked_list = list()
        for i in range(0, len(items), chunk_size):
            chunked_list.append(items[i:i + chunk_size])
        return chunked_list

    def get_items(self) -> List[TItem]:
        query = {
            "path": '/'.join(self.context.getPhysicalPath()),
            "depth": 1,
            "sort_on": 'getObjPositionInParent',
            "portal_type": ['lzv.contact']
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
        
        return self._chunkify(items, 2)

    @staticmethod
    def get_image_url(obj) -> Optional[str]:
        if getattr(obj, 'image', None):
            return obj.absolute_url() + "/@@images/image"

        return None
