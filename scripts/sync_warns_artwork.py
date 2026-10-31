"""Update Warns covers and imagery while retaining the existing site theme.

python scripts/sync_warns_artwork.py --source C:/SEERWARNS
Requires Pillow and beautifulsoup4. No source book build is performed.
"""
from pathlib import Path
import argparse,hashlib,json,re,shutil,sys
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.runtime'),str(ROOT.parent/'SEERWORLDS_WEB/.runtime')]
from bs4 import BeautifulSoup
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def version(p):
    p=p.split('?')[0];return p+'?v='+digest(ROOT/p.lstrip('/'))[:12]
def theme_signature(raw):return hashlib.sha256(re.sub(r'\?v=[a-zA-Z0-9]+','',raw).encode()).hexdigest()
def sync(source,pages_only=False):
    css=ROOT/'style.css';before=theme_signature(css.read_text(encoding='utf-8'))
    pub=ROOT/'publication-sources.json';data=json.loads(pub.read_text(encoding='utf-8'))
    records=[]
    if not pages_only:
        for b in data['books']:
            directory=source/f'book{b["number"]:02}';front=directory/'images-print/cover-front.png'
            full=Image.open(front).convert('RGB');im=full.copy();im.thumbnail((1280,2048),Image.Resampling.LANCZOS)
            target=ROOT/b['cover'].lstrip('/');im.save(target,quality=90,method=6)
            full.save(ROOT/f'images/cover-{b["slug"]}-front.jpg',quality=94,optimize=True)
            b['source_art']=front.relative_to(source).as_posix();b.pop('source_crop_px',None);b['web_cover_size']=list(im.size)
            records.append({'number':b['number'],'cover':b['cover'],'size':list(im.size),
                'source_cover':front.relative_to(source).as_posix(),'source_cover_sha256':digest(front)})
            print(f'Synced Warns cover {b["number"]:02}',flush=True)
        globals=[]
        for name,src in [('hero-home.webp','book01/images-print/background-art-master.png'),('hero-sub.webp','assets/author.png'),('about-scene.webp','assets/author.png'),('harmon-map.webp','assets/map.jpg')]:
            target=ROOT/'images'/name
            with Image.open(target) as old:size=old.size
            ImageOps.fit(Image.open(source/src).convert('RGB'),size,Image.Resampling.LANCZOS).save(target,quality=90,method=6)
            globals.append({'asset':'/images/'+name,'source':src,'source_sha256':digest(source/src),'size':list(size)})
        shutil.copyfile(source/'assets/author.png',ROOT/'images/author-b-carter.png')
        shutil.copyfile(source/'assets/logo.png',ROOT/'images/seer-warns-logo.png')
        shutil.copyfile(source/'assets/map.jpg',ROOT/'images/harmon-map.jpg')
        Image.open(ROOT/'images/hero-home.webp').save(ROOT/'images/hero-home.png')
        (ROOT/'data/warns-artwork.json').write_text(json.dumps({'source':str(source),'books':records,'images':globals,'theme_signature':before},indent=2)+'\n',encoding='utf-8')
        # Edition verification remains the existing record; only artwork fields change.
        data['artwork_updated']='2026-10-26'
        data['notes']=re.sub(r'Artwork:.*?Reader copy:', 'Artwork: current source cover-front.png exports refreshed October 26, 2026. Reader copy:',data['notes'])
        pub.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raw=css.read_text(encoding='utf-8');raw=re.sub(r'(/images/[\w/.-]+\.(?:webp|jpg|png))(?:\?v=[\w]+)?',lambda m:version(m[1]) if (ROOT/m[1].lstrip('/')).exists() else m[0],raw);css.write_text(raw,encoding='utf-8',newline='\n')
    assert before==theme_signature(raw),'The Warns theme must remain unchanged'
    for p in ROOT.rglob('*.html'):
        if any(part.startswith('.') for part in p.relative_to(ROOT).parts):continue
        s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for img in s.select('img'):
            path=img.get('src','').split('?')[0]
            if path.startswith('/images/') and (ROOT/path.lstrip('/')).is_file():
                with Image.open(ROOT/path.lstrip('/')) as im:img['width'],img['height']=im.size
        for tag,attr in [('img','src'),('script','src'),('link','href')]:
            for el in s.select(f'{tag}[{attr}]'):
                path=el[attr].split('?')[0]
                if path.startswith(('/images/','/style.css')) and (ROOT/path.lstrip('/')).is_file():el[attr]=version(path)
        for el in s.select('meta[property="og:image"],meta[name="twitter:image"]'):
            url=el.get('content','');path='/'+url.split('/',3)[-1].split('?')[0] if url.startswith('http') else url.split('?')[0]
            if path.startswith('/images/') and (ROOT/path.lstrip('/')).is_file():el['content']='https://warns.i4seer.com'+version(path)
        p.write_text(str(s),encoding='utf-8',newline='\n')
    print('Updated Warns artwork and cache versions; theme signature unchanged.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=Path('C:/SEERWARNS'));parser.add_argument('--pages-only',action='store_true');args=parser.parse_args();sync(args.source,args.pages_only)
