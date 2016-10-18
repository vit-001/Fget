__author__ = 'Vit'

from base_classes import *
from site_models.base_site_model import ParseResult

from site_models.simple.top_model import TOPSite
from site_models.simple.tma_model import TMASite
from site_models.simple.bas_model import BASSite
from site_models.simple.dsb_model import DSBSite
from site_models.simple.tp_model import TPSite
from site_models.simple.li_model import LISite
from site_models.simple.hxp_model import HXPSite
from site_models.simple.fat_model import FATSite
from site_models.simple.fp_model import FPSite
from site_models.simple.lens_model import LENSSite
from site_models.simple.dt_model import DTSite
from site_models.simple.dsu_model import DSUSite
from site_models.simple.xuk_model import XUKSite
from site_models.simple.cc_model import CCSite
from site_models.simple.fk_model import FKSite

from site_models.collector.el_model import ELSite
from site_models.collector.xxp_model import XXPSite

from site_models.multi.mxt_multi_model import MXTmultiSite
from site_models.simple.be_nest.be_nest import BENest
from site_models.simple.vp_nest.vp_nest import VPNest

from site_models.video.td_model import TDvideoSite
from site_models.video.xm_model import XMvideoSite
from site_models.video.ep_model import EPvideoSite
from site_models.video.vp_video_model import VPvideoSite
from site_models.video.pc_video_model import PCvideoSite
from site_models.video.su_video_model import SUvideoSite
from site_models.video.cbp_video_model import CBPvideoSite
from site_models.video.px_video_model import PXvideoSite
from site_models.video.skw_video_model import SKWvideoSite
from site_models.video.ml_video_model import MLvideoSite
from site_models.video.pd_video_model import PDvideoSite
from site_models.video.t8_video_model import T8videoSite
from site_models.video.rt_video_model import RTvideoSite
from site_models.video.tz_video_model import TZvideoSite
from site_models.video.pb_video_model import PBvideoSite
from site_models.video.nl_video_model import NLvideoSite
from site_models.video.hr_video_model import HRvideoSite
from site_models.video.sm_video_model import SMvideoSite
from site_models.video.gb_video_model import GBvideoSite


from setting import Setting


class SiteVewerModel(AbstractModel):
    def __init__(self, controller=ControllerFromModelInterface()):
        self.controller = controller
        self.debug = Setting.model_debug
        self.models = [RTvideoSite(self),  T8videoSite(self), HRvideoSite(self),SMvideoSite(self),GBvideoSite(self),
                       SUvideoSite(self),TZvideoSite(self),
                       SKWvideoSite(self),PXvideoSite(self),CBPvideoSite(self),
                       PCvideoSite(self),VPvideoSite(self),MLvideoSite(self),
                       PDvideoSite(self),PBvideoSite(self),NLvideoSite(self),
                       BENest(self), VPNest(self), FKSite(self), MXTmultiSite(self),TOPSite(self),
                       TMASite(self), BASSite(self),DSBSite(self),TPSite(self), LISite(self), FATSite(self),
                       FPSite(self), HXPSite(self), LENSSite(self), DTSite(self),
                       DSUSite(self), XUKSite(self), ELSite(self), CCSite(self),
                       XXPSite(self),TDvideoSite(self),EPvideoSite(self)]

    def register_site_model(self, control=ControlInfo()):
        self.controller.add_startpage(control)

    def can_accept_url(self, url):
        for s in self.models:
            if s.can_accept_index_file(url):
                return True
        return False

    def accept_index(self, url=URL(), index_fname=''):
        if self.debug: print('accept index file, URL:', url.get(), 'index:', index_fname)

        site = None
        for s in self.models:
            if s.can_accept_index_file(url):
                site = s
                break
        if site is None:
            print(url.to_save(), ' rejected')
            return

        result = site.parse_index_file(index_fname, url)

        if self.debug: print('Result type:', result.type)

        if result.type == 'none':
            print('Parsing has no result')
            return

        if result.type == 'hrefs':
            if self.debug: print('Generating thumb view')
            result.set_base(Setting.base_dir + 'thumbs/')
            self.generate_thumb_view(url, thumb_list=result)

        if result.type == 'pictures':
            if self.debug: print('Generating full view')
            if result.get_gallery_path() is None:
                page_dir = url.get_path(base=Setting.base_dir)
                if self.debug: print(page_dir)
                result.set_base(page_dir, url)
            else:
                page_dir = result.get_gallery_path()
                if self.debug: print(page_dir)
            # result.set_base(page_dir, url)
            self.controller.show_picture_view(url, page_dir, result.controls, result.full, result.picture_collector)

        if result.type=='video':
            if self.debug: print('Generating video view')
            self.controller.show_video_view(url,result.get_video(),result.controls)



    def generate_thumb_view(self, url=URL(), thumb_list=ParseResult()):
        thumbs = []
        accepted = 0
        rejected = 0
        self.domains = dict()

        for item in thumb_list.thumbs:
            domain = item.get_href().domain()
            self.domains[domain] = self.domains.get(domain, 0) + 1
            for s in self.models:
                if s.can_accept_index_file(item.get_href()):
                    thumbs.append(item)
                    accepted += 1
                    break
            else:
                rejected += 1
                print('Thumb not accepted', item.get_href().get())

        if Setting.statistic:
            print()
            print('Statistic for', url.get())
            print('Accepted     ', accepted)
            print('Rejected     ', rejected)
            for item in self.domains:
                print('%4d' % self.domains[item], 'in domain', item)
            print()

        self.controller.show_thumb_view(url=url,
                                        controls=thumb_list.controls,
                                        pages=thumb_list.pages,
                                        thumbs=thumbs,
                                        sites=thumb_list.sites)

