__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.simple.be_nest.be_model import BESite
from site_models.simple.be_nest.be_multy_thumb_model import BEmultiThumbSite
from site_models.simple.be_nest.bn_model import BEPSite


class BENest(BaseNest):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.add_site(BESite(self))

        # self.add_site(TOPSite(self))
        self.add_site(BEPSite(self))
        self.add_site(BEmultiThumbSite(self))

    def startpage(self):
        return URL("http://www.bravoerotica.com/")

    def start_button_name(self):
        return "BEnest"
