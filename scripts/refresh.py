#!/usr/bin/env python3
"""Daily auto-refresh for Best.Life (run by .github/workflows/refresh.yml).
Rebuilds data/videos.json and data/news.json from public RSS/Atom feeds.
Stdlib only. Any feed that fails is skipped; existing data is kept if everything fails."""
import json, os, re, sys, datetime, urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (compatible; BL-Refresh/1.0; +https://best.life/)"}

# (channel id, expected name fragment, topic)
CHANNELS = [
    ("UCAuUUnT6oDeKwE6v1NGQxug", "ted", "Purpose"),
    ("UCsooa4yRKGN_zEE8iknghZA", "ted-ed", "Mind"),
    ("UCsT0YIqwnpJCM-mx7-gSA4Q", "tedx", "Purpose"),
    ("UC7IcJI8PUf5Z3zKxnZvTBog", "school of life", "Love"),
    ("UCsXVk37bltHxD1rDPwtNM8Q", "kurzgesagt", "Mind"),
    ("UCvQECJukTDE2i6aCoMnS-Vg", "big think", "Mind"),
    ("UCJ24N4O0bP7LGLBDvye7oCA", "matt d", "Work"),
    ("UCG-KntY7aVnIGXYEBQvmBAQ", "thomas frank", "Work"),
    ("UCoOae5nYA7VqaXzerajD0lg", "ali abdaal", "Work"),
    ("UCFKE7WVJfvaHW5q283SxchA", "yoga with adriene", "Health"),
]
FEEDS = [
    ("BBC News — Health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
    ("NPR — Health", "https://feeds.npr.org/1128/rss.xml"),
    ("ScienceDaily — Mind & Brain", "https://www.sciencedaily.com/rss/mind_brain.xml"),
    ("ScienceDaily — Health & Medicine", "https://www.sciencedaily.com/rss/health_medicine.xml"),
    ("The Conversation — Health", "https://theconversation.com/us/health/articles.atom"),
    ("Harvard Health Blog", "https://www.health.harvard.edu/blog/feed"),
]

def get(url, timeout=25):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.status, r.read()

def strip_ns(root):
    for el in root.iter():
        if "}" in el.tag: el.tag = el.tag.split("}", 1)[1]
    return root

def iso(s):
    if not s: return ""
    try: return parsedate_to_datetime(s).astimezone(datetime.timezone.utc).isoformat()
    except Exception: pass
    try: return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(datetime.timezone.utc).isoformat()
    except Exception: return ""

def clean(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()

def load(name):
    try:
        with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f: return json.load(f)
    except Exception: return {}

def save(name, new, keys):
    old = load(name)
    if all(old.get(k) == new.get(k) for k in keys):
        print(name, "unchanged"); return
    new["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(os.path.join(ROOT, "data", name), "w", encoding="utf-8") as f:
        json.dump(new, f, ensure_ascii=False, indent=1)
    print(name, "updated")

def videos():
    old = load("videos.json"); featured = []
    for v in old.get("featured", []):
        try:
            _, raw = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote("https://www.youtube.com/watch?v=" + v["id"], safe=""))
            j = json.loads(raw); v["title"] = j.get("title") or v["title"]; v["channel"] = j.get("author_name") or v.get("channel", "")
            featured.append(v)
        except urllib.error.HTTPError as ex:
            if ex.code in (400, 401, 403, 404): print("drop featured", v["id"], ex.code)
            else: featured.append(v)
        except Exception: featured.append(v)
    latest = []
    for cid, expect, topic in CHANNELS:
        try:
            _, raw = get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid)
            root = strip_ns(ET.fromstring(raw)); name = (root.findtext("title") or "").strip()
            if expect not in name.lower(): print("skip channel (name mismatch):", cid, name); continue
            n = 0
            for en in root.findall("entry"):
                vid, title = en.findtext("videoId"), clean(en.findtext("title"))
                if not vid or not title or "#shorts" in title.lower(): continue
                latest.append({"id": vid, "title": title, "channel": name, "topic": topic, "published": iso(en.findtext("published"))}); n += 1
                if n >= 2: break
        except Exception as ex: print("channel failed", cid, ex)
    latest.sort(key=lambda x: x["published"], reverse=True)
    if not latest: latest = old.get("latest", [])
    if not featured: featured = old.get("featured", [])
    save("videos.json", {"featured": featured, "latest": latest[:18]}, ("featured", "latest"))

def news():
    items, seen = [], set()
    for source, url in FEEDS:
        try:
            _, raw = get(url); root = strip_ns(ET.fromstring(raw)); n = 0
            for it in list(root.iter("item")) + list(root.iter("entry")):
                title = clean(it.findtext("title")); link = (it.findtext("link") or "").strip()
                if not link:
                    for l in it.findall("link"):
                        if l.get("rel") in (None, "alternate"): link = l.get("href") or ""; break
                if not title or not link.startswith("http") or link in seen: continue
                seen.add(link)
                items.append({"title": title[:180], "link": link, "source": source, "date": iso(it.findtext("pubDate") or it.findtext("published") or it.findtext("updated"))}); n += 1
                if n >= 7: break
        except Exception as ex: print("feed failed", source, ex)
    items.sort(key=lambda x: x["date"], reverse=True)
    if not items: print("no news fetched; keeping existing"); return
    save("news.json", {"items": items[:42]}, ("items",))

if __name__ == "__main__":
    videos(); news()
