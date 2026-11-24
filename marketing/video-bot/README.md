# E-Sannad daily promo video

`python3 make.py` makes today's 24-second vertical video (720x1280, Arabic + English, original music)
for one E-Sannad product, rotating daily (contracting, shop POS, e-menu and the others in `content.py`).
Output: `out/<date>-<product>.mp4` and `out/<date>-<product>.json` (caption with hashtags, page link).

Setup: `pip install playwright numpy scipy && python -m playwright install --with-deps chromium`, plus ffmpeg.
The daily task copies the mp4 to `/videos/daily/` so it has a public URL on burooq.net for Facebook/Instagram.
Edit `content.py` to change wording, features, prices or hashtags.
