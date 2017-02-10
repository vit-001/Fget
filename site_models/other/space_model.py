__author__ = 'Vit'

from site_models.base_site_model import *


class SpaceSite(BaseSite):
    def __init__(self, model: AbstractModelFromSiteInterface, base_addr='e:/out/', text=''):
        self.text = text
        super().__init__(model, base_addr)

    def start_button_name(self):
        return self.text

    def autoraise(self):
        return True


if __name__ == "__main__":
    pass
