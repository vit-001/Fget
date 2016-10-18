__author__ = 'Vit'

from site_models.base_site_model import *
from base_classes import URL

from site_models.simple.vp_nest.vp_model import VPSite
from site_models.simple.vp_nest.ps_model import PSSite
from site_models.simple.vp_nest.bb_model import BBSite
from site_models.simple.vp_nest.nn_model import NNSite
from site_models.simple.vp_nest.np_model import NPSite
from site_models.simple.vp_nest.vp_multy_model import VPmultiSite

class VPNest(BaseNest):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.add_site(VPSite(self))
        self.add_site(BBSite(self))
        self.add_site(NNSite(self))
        self.add_site(NPSite(self))
        self.add_site(VPmultiSite(self))
        self.add_site(PSSite(self))

    def startpage(self):
        return URL("http://www.vibraporn.com/galleries")

    def start_button_name(self):
        return "VPnest"



