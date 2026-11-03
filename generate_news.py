#!/usr/bin/env python3
'Free, RSS-based newsletter. No LLM and no API keys required.'
import datetime as dt
import email.utils
import html
import os
from pathlib import Path
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from urllib.parse import urlencode
from zoneinfo import ZoneInfo
import feedparser

ROOT = Path(__file__).resolve().parent
KST = ZoneInfo("Asia/Seoul")
NOW = dt.datetime.now(dt.timezone.utc)
LOCAL_DATE = NOW.astimezone(KST).date().isoformat() + ("-test" if os.environ.get("TEST_MODE") == "1" else "")
LOOKBACK = dt.timedelta(hours=24)
PAGE_URL = os.environ.get("SITE_URL", "https://gmlans77-ops.github.io/ai-maritime-news/").rstrip("/") + "/"
SOURCES = {
    "AI 최신 소식": ["OpenAI OR Anthropic OR Gemini when:1d", "인공지능 AI 모델 출시 when:1d"],
    "업무용 AI 활용": ["enterprise AI productivity automation when:1d", "업무 자동화 생성형AI 기업 when:1d"],
    "조선·해운 산업": ["shipbuilding shipping maritime industry when:1d", "조선 해운 선박 수주 when:1d"],
}
MAX_PER_TOPIC = 3

def plain(value):
    value = re.sub(r"<[^>]*>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def get_time(entry):
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            try: return dt.datetime(*t[:6], tzinfo=dt.timezone.utc)
            except (ValueError, TypeError): pass
    return None

def fetch_articles():
    seen = set()
    result = {}
    for topic, queries in SOURCES.items():
        found = []
        for query in queries:
            url = "https://news.google.com/rss/search?" + urlencode({"q": query,"hl":"ko","gl":"KR","ceid":"KR:ko"})
            try:
                feed = feedparser.parse(url, agent="Mozilla/5.0 AI-Maritime-News/1.0")
                if getattr(feed,"bozo",False) and not feed.entries:
                    print(f"RSS issue for {topic}: {feed.bozo_exception}",file=sys.stderr)
            except Exception as exc:
                print(f"RSS connection issue for {topic}: {exc}",file=sys.stderr)
                continue
            for entry in feed.entries:
                stamp = get_time(entry)
                if stamp is None or not (NOW-LOOKBACK <= stamp <= NOW+dt.timedelta(minutes=10)):
                    continue
                headline = plain(entry.get("title",""))
                link = entry.get("link", "")
                if not headline or not link.startswith("https://"):
                    continue
                key = re.sub(r"\W+", "",headline.lower())[:90]
                if key in seen: continue
                # Google News RSS commonly includes markup with related headlines instead of an actual synopsis.
                # Avoid passing this off as an independently written AI summary.
                desc = plain(entry.get("summary", ""))
                if len(desc) > 230 or headline.lower() in desc.lower() or "Google News" in desc:
                    desc = ""
                source = plain(entry.get("source", {}).get("title", "")) if entry.get("source") else "뉴스 RSS"
                found.append({"title":headline,"url":link,"date":stamp,"source":source,"description":desc})
                seen.add(key)
        found.sort(key=lambda a:a["date"],reverse=True)
        result[topic] = found[:MAX_PER_TOPIC]
    return result

def make_news_html(groups):
    sections=[]
    for topic, articles in groups.items():
        cards=[]
        for a in articles:
            excerpt=(f'<p class="excerpt">{html.escape(a["description"])}</p>' if a["description"] else '<p class="excerpt">RSS에서 별도 기사 소개문을 제공하지 않아 제목과 출처만 표시했습니다.</p>')
            cards.append(f'''<article><h3><a href="{html.escape(a['url'],quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(a['title'])}</a></h3><p class="meta">{html.escape(a['source'])} · RSS 게시 시각 {a['date'].astimezone(KST).strftime('%Y-%m-%d %H:%M')} KST</p>{excerpt}<a class="read" href="{html.escape(a['url'],quote=True)}">기사 열기 ↗</a></article>''')
        sections.append(f'<section><h2>{html.escape(topic)}</h2>'+(''.join(cards) if cards else '<div class="none">최근 24시간 이내 확인된 RSS 기사가 없습니다.</div>')+'</section>')
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI & Maritime Brief | {LOCAL_DATE}</title><style>
    *{{box-sizing:border-box}}body{{margin:0;background:#f3f6fb;color:#152b45;font-family:system-ui,-apple-system,"Malgun Gothic",sans-serif}}main{{max-width:790px;margin:auto;padding:24px 16px 60px}}header{{background:linear-gradient(120deg,#142c4a,#234d7c);border-radius:18px;color:white;padding:34px 30px}}header p{{color:#d8e6f6}}h1{{font-size:2rem;margin:9px 0}}h2{{font-size:1.4rem;margin:30px 0 14px}}h3{{font-size:1.05rem;line-height:1.55;margin:0 0 9px}}article,.none{{background:white;border:1px solid #dfe6f0;padding:21px 22px;border-radius:14px;margin-bottom:12px}}a{{color:#12539b;text-decoration:none}}a:hover{{text-decoration:underline}}.meta{{font-size:.82rem;color:#697c93}}.excerpt{{line-height:1.6;color:#3d536b}}.read{{font-size:.88rem;font-weight:700}}footer{{font-size:.82rem;color:#6d7f95;line-height:1.7;margin-top:28px}}footer a{{color:#2869a4}}@media(max-width:550px){{header{{padding:26px 20px}}h1{{font-size:1.6rem}}}}</style></head><body><main>
    <header><small>AI & MARITIME BRIEF · RSS EDITION</small><h1>AI와 조선·해운의 오늘</h1><p>{LOCAL_DATE} · 최근 24시간 공개 RSS 기사</p></header>
    {''.join(sections)}
    <footer><p>이 뉴스레터는 Google 뉴스 검색 RSS의 제목·출처·제공된 소개문을 자동 정리합니다. AI가 기사 본문을 읽고 사실 검증하거나 독자적으로 요약한 결과가 아닙니다. 날짜는 원 기사 발행일이 아닌 RSS 게시 시각일 수 있으며, 링크는 Google 뉴스 경유일 수 있습니다. 링크된 기사 원문을 확인하세요.</p><p><a href="{html.escape(PAGE_URL,quote=True)}">뉴스레터 아카이브</a></p></footer></main></body></html>'''

def make_index():
    archives=sorted((ROOT/'archive').glob('????-??-??*.html'),reverse=True)
    entries=[]
    for i,p in enumerate(archives):
        date=p.stem
        title='AI & Maritime Brief — '+date
        entries.append(f'<article><div class="meta">{html.escape(date)} · 뉴스레터</div><h2><a href="archive/{html.escape(p.name,quote=True)}">{html.escape(title)} →</a></h2><p>AI 최신 소식, 업무용 AI 활용, 조선·해운 뉴스</p><a href="archive/{html.escape(p.name,quote=True)}">뉴스레터 읽기</a></article>')
    original=(ROOT/'index.html').read_text(encoding='utf-8')
    # Retain existing design; replace from section start through the closing section tag.
    start=original.index('<section class="section">')
    end=original.index('</section>',start)+len('</section>')
    section='<section class="section"><span class="pill">NEWSLETTER ARCHIVE</span><h2>발행된 뉴스레터</h2><p class="meta">매일 뉴스 RSS를 확인하고 새로운 뉴스레터를 자동 추가합니다.</p>\n'+'\n'.join(entries)+'</section>'
    (ROOT/'index.html').write_text(original[:start]+section+original[end:],encoding='utf-8')

def send_mail(html_body, count):
    username=os.environ.get('GMAIL_ADDRESS','').strip()
    app_password=os.environ.get('GMAIL_APP_PASSWORD','').replace(' ','')
    recipient=os.environ.get('NEWSLETTER_TO','').strip()
    if not (username and app_password and recipient):
        print('Email skipped: configure GMAIL_ADDRESS, GMAIL_APP_PASSWORD and NEWSLETTER_TO as GitHub Secrets.')
        return
    msg=EmailMessage()
    msg['From']=username
    msg['To']=recipient
    msg['Subject']=f'[AI·조선해운 뉴스레터] {LOCAL_DATE} · RSS 기사 {count}건'
    msg.set_content(f'{LOCAL_DATE} 뉴스레터: {PAGE_URL}archive/{LOCAL_DATE}.html\n\n기사 {count}건. 원문 링크와 소개문은 뉴스레터를 참고하세요.')
    msg.add_alternative(html_body,subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com',465,timeout=35,context=ssl.create_default_context()) as smtp:
        smtp.login(username,app_password)
        smtp.send_message(msg)
    print('Email sent.')

def main():
    groups=fetch_articles()
    count=sum(len(a) for a in groups.values())
    print(f'Found {count} articles from last 24 hours.')
    if not count:
        print('No current articles found; skip publication to avoid an empty newsletter.')
        return 0
    archive=ROOT/'archive'/f'{LOCAL_DATE}.html'
    archive.parent.mkdir(parents=True,exist_ok=True)
    if archive.exists() and not os.environ.get('FORCE_REGENERATE'):
        print('Newsletter for today already exists; skipping generation and email to avoid duplicates.')
        return 0
    body=make_news_html(groups)
    archive.write_text(body,encoding='utf-8')
    make_index()
    print(f'Generated {archive.relative_to(ROOT)} and updated index.html')
    # Email intentionally handled separately *after successful site deployment* by the workflow.
    return 0

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='send':
        path=ROOT/'archive'/f'{LOCAL_DATE}.html'
        if path.exists():
            body = path.read_text(encoding='utf-8')
            send_mail(body, body.count('class="read"'))
        else: print('No newsletter to email today.')
    else: sys.exit(main())
