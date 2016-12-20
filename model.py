__author__ = 'Vit'

from base_classes import *
from setting import Setting
from site_models.base_site_model import ParseResult
from site_models.collector.el_model import ELSite
from site_models.collector.xxp_model import XXPSite
from site_models.multi.mxt_multi_model import MXTmultiSite
from site_models.other.dude_model import DudeSite
from site_models.other.space_model import SpaceSite
from site_models.simple.bas_model import BASSite
from site_models.simple.be_nest.be_nest import BENest
from site_models.simple.cc_model import CCSite
from site_models.simple.dsb_model import DSBSite
from site_models.simple.dsu_model import DSUSite
from site_models.simple.dt_model import DTSite
from site_models.simple.fat_model import FATSite
from site_models.simple.fk_model import FKSite
from site_models.simple.fp_model import FPSite
from site_models.simple.hxp_model import HXPSite
from site_models.simple.lens_model import LENSSite
from site_models.simple.li_model import LISite
from site_models.simple.tma_model import TMASite
from site_models.simple.top_model import TOPSite
from site_models.simple.tp_model import TPSite
from site_models.simple.vp_nest.vp_nest import VPNest
from site_models.simple.xuk_model import XUKSite
from site_models.video.ajax.ext_video_model import EXTvideoSite
from site_models.video.ajax.pdg_video_model import PDGvideoSite
from site_models.video.nfl_video_model import NFLvideoSite
from site_models.video.pd_video_model import PDvideoSite
from site_models.video.pfun_video_model import PFUNvideoSite
from site_models.video.phd_video_model import PHDvideoSite
from site_models.video.plus_file.dfp_video_model import DFPvideoSite
from site_models.video.plus_file.h69_video_model import H69videoSite
from site_models.video.plus_file.pbz_video_model import PBZvideoSite
from site_models.video.plus_file.sxx_video_model import SXXvideoSite
from site_models.video.plus_file.tsp_video_model import TSPvideoSite
from site_models.video.plus_file.yp_video_model import YPvideoSite
from site_models.video.pt_video_model import PTvideoSite
from site_models.video.px_video_model import PXvideoSite
from site_models.video.script.cls_video_model import CLSvideoSite
from site_models.video.script.dc_video_model import DCvideoSite
from site_models.video.script.pc_video_model import PCvideoSite
from site_models.video.script.rt_video_model import RTvideoSite
from site_models.video.script.v24_video_model import V24videoSite
from site_models.video.simple.bmt_video_model import BMTvideoSite
from site_models.video.simple.cbp_video_model import CBPvideoSite
from site_models.video.simple.gb_video_model import GBvideoSite
from site_models.video.simple.hdep_video_model import HDEPvideoSite
from site_models.video.simple.hr_video_model import HRvideoSite
from site_models.video.simple.ml_video_model import MLvideoSite
from site_models.video.simple.nl_video_model import NLvideoSite
from site_models.video.simple.p4k_video_model import P4KvideoSite
from site_models.video.simple.pb_video_model import PBvideoSite
from site_models.video.simple.ps_video_model import PSvideoSite
from site_models.video.simple.ver_video_model import VERvideoSite
from site_models.video.skw_video_model import SKWvideoSite
from site_models.video.sm_video_model import SMvideoSite
from site_models.video.t8_video_model import T8videoSite
from site_models.video.tz_video_model import TZvideoSite
from site_models.video.vp_video_model import VPvideoSite
from site_models.video.wmgf_video_model import WMGFvideoSite


class SiteVewerModel(AbstractModel):
    def __init__(self, controller=PresenterFromModelInterface()):
        self.controller = controller
        self.debug = Setting.model_debug
        self.models = [
            # work on






            # classic
            SpaceSite(self, text='Classic:'),
            HDEPvideoSite(self),
            YPvideoSite(self), SXXvideoSite(self), PDGvideoSite(self), NFLvideoSite(self), V24videoSite(self),
            PCvideoSite(self), CBPvideoSite(self), PXvideoSite(self), RTvideoSite(self), CLSvideoSite(self),
            VERvideoSite(self), PBZvideoSite(self),
            T8videoSite(self), BMTvideoSite(self),
            PTvideoSite(self), VPvideoSite(self), NLvideoSite(self), TZvideoSite(self), SKWvideoSite(self),
            PHDvideoSite(self), TSPvideoSite(self), DFPvideoSite(self),
            H69videoSite(self),

            # amateur
            SpaceSite(self, text='Amateur:'),
            MLvideoSite(self), WMGFvideoSite(self), PFUNvideoSite(self), PBvideoSite(self),

            # s/m
            SpaceSite(self, text='Deviant:'),
            SMvideoSite(self), GBvideoSite(self), EXTvideoSite(self),

            # deviant
            HRvideoSite(self), DCvideoSite(self), PSvideoSite(self),

            # short video
            SpaceSite(self, text='Short:'),
            PDvideoSite(self),

            # photo archive
            SpaceSite(self, text='Photo:'),
            BENest(self), VPNest(self), FKSite(self), MXTmultiSite(self), TOPSite(self),
            TMASite(self), BASSite(self), DSBSite(self), TPSite(self), LISite(self), FATSite(self),
            FPSite(self), HXPSite(self), LENSSite(self), DTSite(self),
            DSUSite(self), XUKSite(self), ELSite(self), CCSite(self),

            # bad, temporally unworked etc
            SpaceSite(self, text='Non working:'),
            XXPSite(self),
            P4KvideoSite(self),  # unstable

            # info
            SpaceSite(self, text='Info:'),
            DudeSite(self),
        ]

        if Setting.show_sites:
            print('Sites:')
            sites_list = list()
            for item in self.models:
                sites_list.append(item.startpage().__str__())
            for item in sorted(sites_list):
                print(item)
            print('=============================')

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

        if result.is_no_result():
            print('Parsing has no result')
            self.controller.show_status('Parsing has no result')
            return

        if result.is_hrefs():
            if self.debug: print('Generating thumb view')
            result.set_base(Setting.base_dir + 'thumbs/')
            self.generate_thumb_view(url, thumb_list=result)

        if result.is_pictures():
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

        if result.is_video():
            if self.debug: print('Generating video view')
            self.controller.show_video_view(url, result.get_video(), result.controls)

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
                message = '  {0} in domain {1}'.format(self.domains[item], item)
                print(message)
                self.controller.show_status(message)
            print()

        self.controller.show_thumb_view(url=url,
                                        controls=thumb_list.controls,
                                        pages=thumb_list.pages,
                                        thumbs=thumbs,
                                        sites=thumb_list.sites,
                                        caption_visible=thumb_list.caption_visible)
