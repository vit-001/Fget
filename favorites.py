__author__ = 'Vit'

import os

from setting import Setting
from base_classes import URL


class FavoriteRecord():
    thumb='thumb'
    pix='pix'
    video='video'

    def __init__(self,url=URL(),category='',type='pix',name=''):
        self.url=url
        self.category=category
        self.type=type
        self.name=name

    @property
    def combo_view(self):
        if self.type==FavoriteRecord.thumb:
            prexix='+ '
        else:
            prexix='  '
        if self.name!='':
            return prexix+self.name
        return prexix+self.url.get()

    @property
    def save_line(self):
        return 'type='+self.type+' category='+ self.category+ ' url='+self.url.to_save()+' name='+self.name

    @staticmethod
    def get_from_save_line(save_line=''):
        url=URL()
        category=type=name=''
        items=save_line.strip().split(' ')
        for pair in items:
            split=pair.split('=')
            if split[0]=='type':
                type=split[1]
            elif split[0]=='category':
                category=split[1]
            elif split[0]=='url':
                url=URL(split[1])
            elif split[0]=='name':
                name=split[1]
        result=FavoriteRecord(url,category,type,name)
        return result

    def is_thumb(self):
        return self.type==FavoriteRecord.thumb

    def is_pix(self):
        return self.type==FavoriteRecord.pix

    def is_video(self):
        return self.type==FavoriteRecord.video

    def __eq__(self, arg):
        if self.url==arg.url and self.category==arg.category:
            return True
        return False

    def __str__(self, *args, **kwargs):
        return '<FavRecord: '+self.combo_view+' in '+self.category+'>'

    def __repr__(self, *args, **kwargs):
        return self.__str__()

class Favorites():
    def __init__(self,file):
        self.records=list()
        self.listeners=list()

        if Setting.fav_debug: print('Favorites: loading fav file')
        for line in file:
            item=FavoriteRecord.get_from_save_line(line)
            self.add(item,silent=True)

    def add_listener(self,on_change_listener=lambda x:None):
        self.listeners.append(on_change_listener)

    def changed(self,x):
        self.save_tmp()
        for listener in self.listeners:
            listener(x)

    def add(self,record=FavoriteRecord(), silent=False):
        for item in self.records:
            if item==record:
                self.records.remove(item)
                break
        self.records.append(record)

        if not silent: self.changed(record)

    def delete(self,record, silent=False):
        for item in self.records:
            if item==record:
                self.records.remove(item)
                break

        if not silent: self.changed(None)

    def get_categories(self):
        categories=set()
        for item in self.records:
            categories.add(item.category)
        return sorted(categories)

    def get(self,category):
        records=dict()
        for item in self.records:
            if item.category==category:
                if item.name in records:
                    records[item.name].append(item)
                else:
                    records[item.name]=[item]

        t=list()
        for name in sorted(records):
            for item in records[name]:
                t.append(item)
        return t

    def save_tmp(self):
        if Setting.fav_debug: print('saving temp fav file')
        fav_tmp_filename=Setting.fav_filename+'.tmp'
        try:
            os.replace(fav_tmp_filename, fav_tmp_filename+'.old')
        except OSError:
            pass
        try:
            self.save(open(fav_tmp_filename,'w'))
        except OSError as err:
            print('Favorites save temp:',err)


    def save(self,file):
        if Setting.fav_debug: print('saving fav file')
        for category in self.get_categories():
            for item in self.get(category):
                file.write(item.save_line+'\n')
        pass



if __name__ == "__main__":
    fav=Favorites()

    for i in range(1,10):
        for j in range(1,5):
            rec=FavoriteRecord(URL('http://xxx.com/aaa/%01d*'%j),'c%03d'%i,'pix','r%03d%03d'%(i,j))
            fav.add(rec)

    print(fav.get_categories())
    print(fav.get('c004'))
    print(fav.get_sorted_urls('c004'))