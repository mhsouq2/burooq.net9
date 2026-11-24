"""Daily E-Sannad promo video: vertical 720x1280, 30 fps, ~23 s, Arabic + English, original music.

  python3 make.py                      # today's product (rotates by date)
  python3 make.py --product emenu      # a given product
  python3 make.py --date 2026-11-24    # as if it were that day
  python3 make.py --stills             # only a few test frames

Writes out/<date>-<product>.mp4 and out/<date>-<product>.json (captions + hashtags + page URL).
Needs: playwright (chromium), ffmpeg, numpy, scipy."""
import datetime, json, os, shutil, subprocess, sys
from html import escape as E
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C

W, H, FPS = 720, 1280, 30
NAVY, GOLD, GREEN = '#0F3D63', '#E8A33D', '#25D366'
FONTS = os.path.join(HERE, 'fonts')
OUT = os.path.join(HERE, 'out')
WORK = os.path.join(HERE, 'work')


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


day = datetime.date.fromisoformat(arg('--date', datetime.date.today().isoformat()))
n = day.toordinal()
key = arg('--product') or C.ROTATION[n % len(C.ROTATION)]
p = C.P[key]
cycle = n // len(C.ROTATION)
hook_en, hook_ar = p['hooks'][(cycle + n) % len(p['hooks'])]
off = 0 if cycle % 2 == 0 else 3
feats = p['features'][off:off + 3]
ACC = p['color']
start_en, start_ar = C.SEASON.get(day.month, C.START)
url_path = f"/software/{p['slug']}/"

BASE = f"""
@font-face{{font-family:Tajawal;font-weight:700;src:url(file://{FONTS}/tajawal-arabic-700-normal.woff2)}}
@font-face{{font-family:Tajawal;font-weight:800;src:url(file://{FONTS}/tajawal-arabic-800-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:500;src:url(file://{FONTS}/inter-latin-500-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:700;src:url(file://{FONTS}/inter-latin-700-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url(file://{FONTS}/inter-latin-800-normal.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{NAVY};font-family:Inter,Tajawal,sans-serif;color:#fff}}
.ar{{font-family:Tajawal,sans-serif;direction:rtl}}
#root{{position:absolute;inset:0;animation:fade var(--d) linear both}}
@keyframes fade{{0%{{opacity:0}}4%{{opacity:1}}95%{{opacity:1}}100%{{opacity:0}}}}
.bg{{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#1b5a8c 0,{NAVY} 62%)}}
.cap{{position:absolute;left:36px;right:36px;text-align:center}}
.cap .en{{font-size:60px;font-weight:800;line-height:1.1}}
.cap .ar{{font-size:54px;font-weight:800;line-height:1.3;color:{GOLD};margin-top:16px}}
.up{{animation:up var(--d) ease-out both}}
@keyframes up{{0%{{opacity:0;transform:translateY(40px)}}12%{{opacity:1;transform:none}}100%{{opacity:1;transform:none}}}}
.brand{{position:absolute;left:0;right:0;bottom:34px;text-align:center;font:700 24px Inter;opacity:.75;letter-spacing:.5px}}
"""


def page(css, body, dur):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}{css}</style></head>'
            f'<body style="--d:{dur}s"><div id="root"><div class="bg"></div>{body}'
            f'<div class="brand">E-Sannad · burooq.net</div></div></body></html>')


SC = []
# 0 — first-second hook: who this is for
SC.append(('s0', 1.8, f"""
.flash{{position:absolute;inset:0;background:{GOLD};animation:fl var(--d) linear both}}
@keyframes fl{{0%{{opacity:1}}30%{{opacity:1}}100%{{opacity:0}}}}
.cw{{position:absolute;left:30px;right:30px;top:420px;text-align:center;animation:punch var(--d) cubic-bezier(.2,1.6,.4,1) both}}
@keyframes punch{{0%{{transform:scale(2.2);opacity:0}}18%{{transform:scale(1);opacity:1}}100%{{transform:scale(1.04)}}}}
.cw .en{{font:800 86px Inter;line-height:1.05;color:#fff;text-shadow:0 6px 0 rgba(0,0,0,.25)}}
.cw .ar{{font:800 74px Tajawal;line-height:1.25;color:#fff;margin-top:18px;text-shadow:0 6px 0 rgba(0,0,0,.25)}}
.warn{{width:120px;height:120px;margin:0 auto 34px;border-radius:50%;background:#ef4444;color:#fff;font:800 84px Inter;
  display:flex;align-items:center;justify-content:center;animation:shake var(--d) linear both}}
@keyframes shake{{0%,20%{{transform:rotate(0)}}25%{{transform:rotate(-12deg)}}30%{{transform:rotate(12deg)}}35%{{transform:rotate(-8deg)}}40%,100%{{transform:rotate(0)}}}}
#root{{animation:none}} .brand{{display:none}}
""", f"""<div class="flash"></div><div class="cw"><div class="warn">!</div><div class="en">{E(p['call'][0])}</div><div class="ar">{E(p['call'][1])}</div></div>"""))
# 1 — the pain
SC.append(('s1', 3.8, f"""
.paper{{position:absolute;left:50%;top:150px;width:330px;height:420px;margin-left:-165px;background:#f5efe4;border-radius:16px;
  box-shadow:0 30px 60px rgba(0,0,0,.45);padding:34px 30px;animation:pin var(--d) ease-out both;color:#5b4632}}
.paper b{{display:block;font:800 36px Inter;margin-bottom:22px}} .paper b.ar{{font:800 36px Tajawal}}
.paper i{{display:block;height:15px;background:#d6cbb8;border-radius:8px;margin:20px 0}} .paper i:nth-child(odd){{width:68%}}
.x1,.x2{{position:absolute;left:50%;top:360px;width:440px;height:18px;margin-left:-220px;background:#ef4444;border-radius:9px}}
.x1{{animation:x1 var(--d) ease-out both}} .x2{{animation:x2 var(--d) ease-out both}}
@keyframes pin{{0%{{opacity:0;transform:rotate(-12deg) scale(.9)}}14%{{opacity:1;transform:rotate(-6deg)}}100%{{transform:rotate(-6deg)}}}}
@keyframes x1{{0%,34%{{transform:rotate(45deg) scaleX(0)}}48%,100%{{transform:rotate(45deg) scaleX(1)}}}}
@keyframes x2{{0%,44%{{transform:rotate(-45deg) scaleX(0)}}58%,100%{{transform:rotate(-45deg) scaleX(1)}}}}
""", f"""<div class="paper"><b>{E(p['old'][0])}</b><b class="ar">{E(p['old'][1])}</b><i></i><i></i><i></i><i></i><i></i></div>
<div class="x1"></div><div class="x2"></div>
<div class="cap up" style="top:660px"><div class="en">{E(hook_en)}</div><div class="ar">{E(hook_ar)}</div></div>"""))

# 2 — the product on a phone
rows = ''.join(f'<div class="card c{i}"><div class="l">{E(l)}</div><div class="v">{E(v)}</div></div>'
               for i, (l, v) in enumerate(p['screen']))
bars = ''.join(f'<span style="height:{h}%;animation-delay:{i * 0.08:.2f}s"></span>'
               for i, h in enumerate([40, 62, 48, 75, 58, 88, 70]))
SC.append(('s2', 5.4, f"""
.top{{position:absolute;left:30px;right:30px;top:60px;text-align:center;animation:up var(--d) ease-out both}}
.top .k{{font:800 30px Inter;color:{GOLD};letter-spacing:1px}}
.top .en{{font:800 58px Inter;line-height:1.08;margin-top:10px}} .top .ar{{font:800 50px Tajawal;margin-top:10px}}
.phone{{position:absolute;left:50%;width:420px;height:860px;margin-left:-210px;border-radius:56px;background:#0b1220;padding:14px;
  box-shadow:0 40px 80px rgba(0,0,0,.45),0 0 0 3px #2b3a52;animation:ph var(--d) cubic-bezier(.2,.8,.2,1) both}}
@keyframes ph{{0%,10%{{top:1300px}}30%,100%{{top:440px}}}}
.brand{{display:none}}
.scr{{width:100%;height:100%;border-radius:44px;overflow:hidden;background:#f4f6fa;color:#111827}}
.hd{{background:{ACC};color:#fff;padding:54px 24px 22px}} .hd .a{{font:800 30px Inter}} .hd .b{{font:800 26px Tajawal;direction:rtl;margin-top:6px;opacity:.95}}
.card{{margin:16px 18px 0;background:#fff;border-radius:20px;padding:18px 22px;box-shadow:0 4px 14px rgba(0,0,0,.06);
  animation:cr var(--d) ease-out both}}
.card .l{{font:700 22px Inter;color:#6b7280}} .card .v{{font:800 40px Inter;color:#111827;margin-top:4px}}
.c1{{animation-name:cr1}} .c2{{animation-name:cr2}}
@keyframes cr{{0%,30%{{opacity:0;transform:translateY(20px)}}38%,100%{{opacity:1;transform:none}}}}
@keyframes cr1{{0%,36%{{opacity:0;transform:translateY(20px)}}44%,100%{{opacity:1;transform:none}}}}
@keyframes cr2{{0%,42%{{opacity:0;transform:translateY(20px)}}50%,100%{{opacity:1;transform:none}}}}
.chart{{margin:18px 18px 0;background:#fff;border-radius:20px;height:150px;padding:18px 22px;display:flex;gap:14px;align-items:flex-end}}
.chart span{{flex:1;background:{ACC};border-radius:8px 8px 0 0;animation:bar var(--d) ease-out both}}
@keyframes bar{{0%,44%{{transform:scaleY(0)}}62%,100%{{transform:scaleY(1)}}}}
.chart span{{transform-origin:bottom}}
""", f"""<div class="top"><div class="k">E-SANNAD · إي-سند</div><div class="en">{E(p['en'])}</div><div class="ar">{E(p['ar'])}</div></div>
<div class="phone"><div class="scr"><div class="hd"><div class="a">{E(p['en'])}</div><div class="b">{E(p['ar'])}</div></div>{rows}
<div class="chart">{bars}</div></div></div>"""))

# 3 — three features
fc = ''.join(f'<div class="f f{i}"><div class="ck">✓</div><div><div class="en">{E(a)}</div><div class="ar">{E(b)}</div></div></div>'
             for i, (a, b) in enumerate(feats))
SC.append(('s3', 8.4, f"""
.t{{position:absolute;left:30px;right:30px;top:80px;text-align:center;animation:up var(--d) ease-out both}}
.t .en{{font:800 56px Inter}} .t .ar{{font:800 50px Tajawal;color:{GOLD};margin-top:8px}}
.list{{position:absolute;left:34px;right:34px;top:330px;display:flex;flex-direction:column;gap:30px}}
.f{{display:flex;gap:24px;align-items:center;background:#fff;color:#111827;border-radius:28px;padding:30px 30px;
  box-shadow:0 18px 40px rgba(0,0,0,.3);animation:f0 var(--d) cubic-bezier(.2,.8,.2,1) both}}
.f1{{animation-name:f1}} .f2{{animation-name:f2}}
.ck{{flex:none;width:84px;height:84px;border-radius:50%;background:{ACC};color:#fff;font:800 50px Inter;display:flex;align-items:center;justify-content:center}}
.f .en{{font:800 42px Inter;line-height:1.12}} .f .ar{{font:800 38px Tajawal;color:{ACC};margin-top:6px;text-align:right}}
.f>div:last-child{{flex:1}}
@keyframes f0{{0%,8%{{opacity:0;transform:translateX(-80px)}}16%,100%{{opacity:1;transform:none}}}}
@keyframes f1{{0%,36%{{opacity:0;transform:translateX(80px)}}44%,100%{{opacity:1;transform:none}}}}
@keyframes f2{{0%,64%{{opacity:0;transform:translateX(-80px)}}72%,100%{{opacity:1;transform:none}}}}
""", f"""<div class="t"><div class="en">All in one place</div><div class="ar">كل شيء في مكان واحد</div></div><div class="list">{fc}</div>"""))

# 3b — honest urgency: the cost of waiting
SC.append(('s3b', 3.6, f"""
.band{{position:absolute;left:0;right:0;top:330px;background:#dc2626;padding:56px 40px;text-align:center;transform:rotate(-3deg);
  box-shadow:0 20px 50px rgba(0,0,0,.4);animation:sl var(--d) cubic-bezier(.2,.8,.2,1) both}}
@keyframes sl{{0%{{transform:rotate(-3deg) translateX(-110%)}}16%,100%{{transform:rotate(-3deg) translateX(0)}}}}
.band .en{{font:800 54px Inter;line-height:1.12}} .band .ar{{font:800 50px Tajawal;line-height:1.3;margin-top:18px}}
.go{{position:absolute;left:0;right:0;top:860px;text-align:center;animation:pulse var(--d) ease-in-out both}}
.go b{{display:inline-block;background:{GOLD};color:#1f2937;font:800 62px Inter;padding:24px 54px;border-radius:70px}}
.go .ar{{display:block;font:800 56px Tajawal;color:{GOLD};margin-top:22px}}
@keyframes pulse{{0%,30%{{opacity:0;transform:scale(.8)}}40%{{opacity:1;transform:scale(1.08)}}50%{{transform:scale(1)}}62%{{transform:scale(1.07)}}74%,100%{{transform:scale(1)}}}}
""", f"""<div class="band"><div class="en">{E(p['loss'][0])}</div><div class="ar">{E(p['loss'][1])}</div></div>
<div class="go"><b>{E(start_en)} →</b><span class="ar">{E(start_ar)}</span></div>"""))

# 4 — price + how to buy
SC.append(('s4', 5.6, f"""
.wrap{{position:absolute;left:36px;right:36px;top:110px;text-align:center}}
.nm{{font:800 46px Inter;animation:up var(--d) ease-out both}} .nma{{font:800 42px Tajawal;color:{GOLD};margin-top:6px;animation:up var(--d) ease-out both}}
.price{{margin:44px auto 0;background:#fff;color:#111827;border-radius:30px;padding:30px 24px;animation:pop var(--d) cubic-bezier(.2,.8,.2,1) both}}
.price .a{{font:800 52px Inter;color:{ACC}}} .price .b{{font:700 26px Inter;color:#4b5563;margin-top:8px}}
.price .c{{font:800 46px Tajawal;direction:rtl;color:{ACC};margin-top:18px}} .price .d{{font:700 26px Tajawal;direction:rtl;color:#4b5563;margin-top:4px}}
@keyframes pop{{0%,10%{{opacity:0;transform:scale(.85)}}22%,100%{{opacity:1;transform:none}}}}
.buy{{display:inline-block;margin-top:40px;background:{GOLD};color:#1f2937;font:800 44px Inter;padding:22px 44px;border-radius:60px;animation:pop2 var(--d) ease-out both}}
.buy span{{font-family:Tajawal}}
@keyframes pop2{{0%,30%{{opacity:0;transform:scale(.8)}}40%,100%{{opacity:1;transform:none}}}}
.buy{{animation:pop2 var(--d) ease-out both,beat 1s ease-in-out 1.4s infinite}}
@keyframes beat{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.06)}}}}
.url{{font:800 46px Inter;margin-top:28px;animation:pop2 var(--d) ease-out both}}
.wa{{display:inline-flex;gap:18px;align-items:center;margin-top:30px;background:{GREEN};color:#fff;font:800 50px Inter;padding:20px 40px;border-radius:60px;
  animation:pop3 var(--d) ease-out both}}
.wa i{{width:56px;height:56px;border-radius:50%;background:#fff;color:{GREEN};font:800 34px Inter;font-style:normal;display:flex;align-items:center;justify-content:center}}
@keyframes pop3{{0%,44%{{opacity:0;transform:translateY(30px)}}54%,100%{{opacity:1;transform:none}}}}
""", f"""<div class="wrap"><div class="nm">{E(p['en'])}</div><div class="nma ar">{E(p['ar'])}</div>
<div class="price"><div class="a">{E(C.PRICE_EN)}</div><div class="b">{E(C.PRICE_EN2)}</div>
<div class="c">{E(C.PRICE_AR)}</div><div class="d">{E(C.PRICE_AR2)}</div></div>
<div class="buy"><bdi>Buy online</bdi> · <bdi><span>اشترِ أونلاين</span></bdi></div><div class="url">burooq.net</div>
<div class="wa"><i>✆</i>{E(C.WHATSAPP)}</div></div>"""))


def chrome(pw):
    for exe in (os.environ.get('CHROME'), None, '/usr/bin/google-chrome', '/usr/bin/chromium'):
        try:
            kw = {'executable_path': exe} if exe else {}
            return pw.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files'], **kw)
        except Exception as e:  # try the next browser
            last = e
    raise last


def render(stills=False):
    os.makedirs(OUT, exist_ok=True); os.makedirs(WORK, exist_ok=True)
    files = []
    with sync_playwright() as pw:
        b = chrome(pw)
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
        for name, dur, css, body in SC:
            path = os.path.join(WORK, name + '.html')
            open(path, 'w', encoding='utf-8').write(page(css, body, dur))
            pg.goto('file://' + path); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.evaluate('document.getAnimations().forEach(a => a.pause())')
            if stills:
                for frac in (0.5, 0.9):
                    pg.evaluate(f'document.getAnimations().forEach(a => a.currentTime = {dur * frac * 1000})')
                    pg.screenshot(path=os.path.join(OUT, f'{name}_{int(frac * 100)}.jpg'), type='jpeg', quality=92)
                continue
            frames = int(round(dur * FPS)); tmp = os.path.join(WORK, name + '.tmp.mp4'); dst = os.path.join(WORK, name + '.mp4')
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                   '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp],
                                  stdin=subprocess.PIPE)
            for i in range(frames):
                pg.evaluate(f'document.getAnimations().forEach(a => a.currentTime = {i * 1000 / FPS})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait() != 0: raise SystemExit(f'ffmpeg failed on {name}')
            os.replace(tmp, dst); files.append(dst)
        b.close()
    return files


def caption():
    f = '\n'.join(f'✅ {a}' for a, _ in feats); fa = '\n'.join(f'✅ {b}' for _, b in feats)
    link = C.SITE + url_path
    en = (f"{p['call'][0]} {hook_en}\n\nE-Sannad {p['en']} by Alburooq:\n{f}\n\n💳 {C.PRICE_EN} ({C.PRICE_EN2}).\n"
          f"⏳ {p['loss'][0]} {start_en}.\nBuy online: {link}\nWhatsApp: {C.WHATSAPP}")
    ar = (f"{p['call'][1]} {hook_ar}\n\n{p['ar']} من إي-سند (البروق):\n{fa}\n\n💳 {C.PRICE_AR} ({C.PRICE_AR2}).\n"
          f"⏳ {p['loss'][1]} {start_ar}.\nاشترِ أونلاين: {link}\nواتساب: {C.WHATSAPP}")
    return {'date': day.isoformat(), 'product': key, 'page_url': link, 'hook_en': hook_en, 'hook_ar': hook_ar,
            'features': feats, 'caption': ar + '\n\n' + en + '\n\n' + p['tags'], 'hashtags': p['tags']}


if __name__ == '__main__':
    stills = '--stills' in sys.argv
    parts = render(stills)
    if stills: print('stills in', OUT); raise SystemExit
    total = sum(d for _, d, _, _ in SC)
    starts = [sum(d for _, d, _, _ in SC[:i]) for i in range(len(SC))]
    ix = {nm: i for i, (nm, *_ ) in enumerate(SC)}
    dings = [0.05] + [starts[ix['s3']] + SC[ix['s3']][1] * x for x in (0.1, 0.38, 0.66)] + [starts[ix['s4']] + SC[ix['s4']][1] * 0.46]
    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{f}'\n" for f in parts))
    silent = os.path.join(WORK, 'silent.mp4'); wav = os.path.join(WORK, 'music.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', silent], check=True)
    subprocess.run([sys.executable, os.path.join(HERE, 'make_music.py'), f'{total:.2f}', wav, *[f'{d:.2f}' for d in dings],
                    '--seed', str(n)], check=True)
    base = os.path.join(OUT, f'{day.isoformat()}-{key}')
    tmp = base + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, base + '.mp4')
    json.dump(caption(), open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    shutil.rmtree(WORK, ignore_errors=True)
    print(base + '.mp4'); print(base + '.json')
