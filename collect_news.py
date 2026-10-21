#!/usr/bin/env python3
"""K-water-related news headline index from Google News RSS.

Public metadata only. No full article text, paywalled scraping, or AI assertions.
Can run under a public GitHub repository without secrets.
"""
import email.utils
import hashlib
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'news-data.json'
KST = timezone(timedelta(hours=9))
QUERY = '("한국수자원공사" OR "K-water" OR "한국수자원공사 주암댐") when:30d'
URL = ('https://news.google.com/rss/search?q=' + urllib.parse.quote(QUERY) +
       '&hl=ko&gl=KR&ceid=KR:ko')
AGENCY = re.compile(r'한국수자원공사|K\s*-\s*water|kwater|주암댐|한국수자원공사', re.I)


def tag_and_route(title):
    tags=[]
    for tag,words in [
        ('안전',('홍수','가뭄','댐 안전','수질','녹조','오염','안전','재난','누수','수해')),
        ('역동',('ai','인공지능','디지털','스마트','혁신','초순수','데이터','기술','반도체')),
        ('공정',('지역상생','주민','협력','청렴','공정','보상','지원사업','민원','지역사회')),
        ('계약',('계약','구매','조달','협약','입찰','수주')),
        ('사업관리',('사업','예산','운영','경영','투자')),
    ]:
        if any(w in title.lower() for w in words): tags.append(tag)
    if '역동' in tags:return tags,'project-p5'
    if '안전' in tags:return tags,'project-p4'
    if '공정' in tags:return tags,'project-p7'
    return tags,'company-overview'


def fetch():
    req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 (compatible; KwaterStudyIndex/1.0)'})
    with urllib.request.urlopen(req,timeout=25) as r: raw=r.read(1_500_000)
    return ET.fromstring(raw)


def to_iso(date):
    try:return email.utils.parsedate_to_datetime(date).astimezone(KST).strftime('%Y-%m-%d')
    except Exception:return ''


def run():
    doc=fetch();found=[];seen=set()
    for entry in doc.findall('.//channel/item'):
        title=(entry.findtext('title') or '').strip()
        link=(entry.findtext('link') or '').strip()
        date=to_iso(entry.findtext('pubDate') or '')
        source_tag=entry.find('source')
        source=(source_tag.text or 'Google 뉴스 검색 피드').strip() if source_tag is not None else 'Google 뉴스 검색 피드'
        # RSS results are a search index; source claims are NOT verified against the full article.
        if not AGENCY.search(title) or not date or not link.startswith('https://'):
            continue
        key=hashlib.sha256((title+'|'+date).encode()).hexdigest()[:18]
        if key in seen:continue
        seen.add(key)
        tags,folder=tag_and_route(title)
        found.append({'id':key,'title':title[:190],'date':date,'source':source[:85],
                      'sourceType':'external','url':link,
                      'summary':'뉴스 검색 피드에서 제목과 게시일을 수집했어요. 사실관계는 기사 원문과 공식 자료를 대조해 확인해 주세요.',
                      'tags':tags,'folder':folder})
    if not found:
        print('No matching fresh items. Keep previous news-data.json unchanged.',file=sys.stderr)
        return 2
    found=sorted(found,key=lambda x:x['date'],reverse=True)[:40]
    result={'schema_version':1,'generated_at':datetime.now(KST).isoformat(timespec='minutes'),
            'source':'Google News RSS · 검색 결과 (자동 사실 검증 아님)',
            'source_url':URL,'items':found}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(found)} items to {OUT.name}')
    return 0


if __name__=='__main__':
    try:sys.exit(run())
    except (urllib.error.URLError,ET.ParseError,TimeoutError) as e:
        print('Feed error; previous data preserved:',e,file=sys.stderr)
        sys.exit(2)
