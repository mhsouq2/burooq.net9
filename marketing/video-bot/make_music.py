"""Original upbeat background track (synthesised, royalty-free) + optional notification dings.
Usage: make_music.py <seconds> <out.wav> [ding_time ...] [--seed N]"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
args = sys.argv[1:]
seed = 7
if '--seed' in args:
    i = args.index('--seed'); seed = int(args[i + 1]); del args[i:i + 2]
dur = float(args[0]); out = args[1]; dings = [float(x) for x in args[2:]]
N = int(SR * dur); t = np.arange(N) / SR
BPM = [96, 104, 112][seed % 3]; beat = 60 / BPM; bar = 4 * beat
rng = np.random.default_rng(seed)
mix = np.zeros((N, 2))

def note(f): return 440 * 2 ** ((f - 69) / 12)
def env(n, a=0.005, d=0.25, s=0.0, r=0.05, length=None):
    length = length or n
    e = np.ones(n)
    ai = int(a * SR); di = int(d * SR)
    e[:ai] = np.linspace(0, 1, ai) if ai else 1
    if di: e[ai:ai + di] = np.linspace(1, s, len(e[ai:ai + di]))
    e[ai + di:] = s
    ri = min(int(r * SR), n); e[-ri:] *= np.linspace(1, 0, ri)
    return e
def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[:N - i] * gain
    mix[i:i + len(sig), 0] += sig * (1 - pan) ** 0.5 * 0.7
    mix[i:i + len(sig), 1] += sig * (1 + pan) ** 0.5 * 0.7

# progression: C - G - Am - F  (bright, friendly)
PROG = [([[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], [36, 43, 45, 41]),   # C G Am F
        ([[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]], [45, 41, 36, 43]),   # Am F C G
        ([[53, 57, 60], [55, 59, 62], [57, 60, 64], [60, 64, 67]], [41, 43, 45, 36])]   # F G Am C
chords, bass = PROG[(seed // 3) % 3]

def pad(freqs, length):
    n = int(length * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.12):
            ph = 2 * np.pi * note(f + det) * tt
            s += np.sin(ph) * 0.5 + 0.18 * np.sin(2 * ph)
    return s / len(freqs) * env(n, a=0.4, d=0.5, s=0.7, r=0.4)
def pluck(f, length=0.35):
    n = int(length * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * note(f) * tt) + 0.3 * np.sin(4 * np.pi * note(f) * tt) + 0.1 * np.sin(6 * np.pi * note(f) * tt)
    return s * env(n, a=0.003, d=0.3, s=0.0, r=0.03)
def bassnote(f, length):
    n = int(length * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * note(f) * tt) + 0.25 * np.sin(4 * np.pi * note(f) * tt)
    return s * env(n, a=0.005, d=length * 0.8, s=0.3, r=0.05)
def kick():
    n = int(0.35 * SR); tt = np.arange(n) / SR
    f = 50 + 90 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
sos_hp = butter(4, 7000, 'hp', fs=SR, output='sos'); sos_bp = butter(2, [900, 4000], 'bp', fs=SR, output='sos')
def hat():
    n = int(0.06 * SR); return sosfilt(sos_hp, rng.standard_normal(n)) * np.exp(-np.arange(n) / SR * 70)
def clap():
    n = int(0.25 * SR); return sosfilt(sos_bp, rng.standard_normal(n)) * np.exp(-np.arange(n) / SR * 18)

nbars = int(np.ceil(dur / bar)) + 1
arp_pat = [0, 1, 2, 1, 2, 0, 1, 2]
for b in range(nbars):
    t0 = b * bar; c = chords[b % 4]
    add(pad([x + 12 for x in c], bar + 0.4), t0, gain=0.22)
    for k in range(8):                                  # bass on eighths
        add(bassnote(bass[b % 4] + (12 if k % 4 == 3 else 0), beat / 2), t0 + k * beat / 2, gain=0.42)
    if b >= 1:                                          # arpeggio enters after bar 1
        for k in range(8):
            add(pluck(c[arp_pat[k]] + 12), t0 + k * beat / 2, pan=0.35 if k % 2 else -0.35, gain=0.2)
    for k in range(4):                                  # drums
        add(kick(), t0 + k * beat, gain=0.75)
        if k in (1, 3): add(clap(), t0 + k * beat, gain=0.25)
        for h in range(2): add(hat(), t0 + k * beat + h * beat / 2 + beat / 4, pan=0.4, gain=0.18)

# gentle "sidechain" pump so the beat breathes
pump = 1 - 0.25 * np.exp(-((t % beat) / 0.12))
mix *= pump[:, None]

# notification dings (two soft bell tones)
def ding():
    n = int(0.6 * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for f, d, a in ((1318.5, 0.0, 1.0), (1760.0, 0.09, 0.8)):
        i = int(d * SR); m = n - i
        s[i:] += a * np.sin(2 * np.pi * f * tt[:m]) * np.exp(-tt[:m] * 9)
    return s
for d in dings: add(ding(), d, gain=0.45)

# master: fade in/out, normalise
fi, fo = int(0.6 * SR), int(1.6 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]; mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = np.tanh(mix * 1.2)
mix *= 0.6 / np.max(np.abs(mix))                       # leaves headroom; it sits under the visuals
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print('wrote', out, round(dur, 2), 's')
