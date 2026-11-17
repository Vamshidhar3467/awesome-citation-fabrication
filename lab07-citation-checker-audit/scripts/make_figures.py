"""Paper figures, drawn only from results/phase4 files.   python scripts/make_figures.py"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results/phase4'
OUT = ROOT / 'paper/figures'
COLORS = {'B1': '#2a78d6', 'B2': '#eb6834', 'B3': '#1baf7a'}  # validated categorical slots 1-3
NAMES = {'B1': 'B1 DOI-only', 'B2': 'B2 metadata (Jaccard)', 'B3': 'B3 metadata (containment)'}
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e4e3df'

plt.rcParams.update({'font.family': 'serif', 'font.size': 8, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'axes.grid.axis': 'y', 'grid.color': GRID, 'grid.linewidth': .6,
                     'axes.axisbelow': True, 'legend.frameon': False, 'savefig.dpi': 300})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f'{name}.pdf', bbox_inches='tight')
    fig.savefig(OUT / f'{name}.png', bbox_inches='tight')
    plt.close(fig)


def grouped(ax, categories, values, labels):
    width = .26
    for j, m in enumerate(('B1', 'B2', 'B3')):
        xs = [i + (j - 1) * (width + .02) for i in range(len(categories))]
        bars = ax.bar(xs, values[m], width, color=COLORS[m], label=NAMES[m], edgecolor='white', linewidth=.8)
        for x, v, text in zip(xs, values[m], labels[m]):
            ax.text(x, v + .02, text, ha='center', va='bottom', fontsize=5.5, color=INK)
    ax.set_xticks(range(len(categories)))
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, .25, .5, .75, 1])


def figure_detection_vs_false_flags(metrics):
    errors = ['wrong_year', 'wrong_author', 'wrong_doi', 'frankenstein', 'synthetic_unmatched']
    stress = ['et_al_first_author', 'venue_abbrev', 'subtitle_dropped', 'print_year', 'title_hyphen_break']
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.1, 2.5), gridspec_kw={'width_ratios': [1, 1]})
    rec = {m: [metrics[f'ext/{m}']['any_error']['per_category'][c]['recall'] for c in errors] for m in COLORS}
    grouped(a, errors, rec, {m: [f'{v:g}' for v in rec[m]] for m in COLORS})
    a.set_xticklabels(['wrong\nyear', 'wrong\nauthor', 'wrong\nDOI', 'Franken-\nstein', 'synthetic\nunmatched'], fontsize=6.5)
    a.set_ylabel('Recall (higher is better)')
    a.set_title('(a) Constructed errors, extension set (40 works)', fontsize=8, loc='left', color=INK)
    per = {m: metrics[f'ext_stress/{m}']['per_category'] for m in COLORS}
    rate = {m: [per[m][c]['false_flags'] / per[m][c]['n'] for c in stress] for m in COLORS}
    grouped(b, stress, rate, {m: [str(per[m][c]['false_flags']) for c in stress] for m in COLORS})
    names = ['"et al."\nauthors', 'abbrev.\nvenue', 'subtitle\ndropped', 'print-year\ndrift', 'hyphen\nbreak']
    b.set_xticklabels([f"{n}\nn={per['B1'][c]['n']}" for n, c in zip(names, stress)], fontsize=6.5)
    b.set_ylabel('False-flag rate (lower is better)')
    b.set_title('(b) Legitimate variants (all should pass)', fontsize=8, loc='left', color=INK)
    handles, labels = a.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(.5, 1.07))
    fig.tight_layout()
    save(fig, 'fig_detection_false_flags')


def figure_ablation():
    rows = list(csv.DictReader((RES / 'ablation.csv').open(encoding='utf-8')))
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.grid(True, axis='both')
    offsets = {'B2 all fields': (-20, -11), 'title only': (4, 5), 'authors only': (6, -3), 'year only': (-4, -11),
               'venue only': (6, -3), 'without title': (-46, 6), 'without authors': (6, -3),
               'without year': (-8, -11), 'without venue': (-62, -3)}
    for r in rows:
        x, y = float(r['stress_false_flag_rate']), float(r['macro_recall'])
        full = r['variant'] == 'B2 all fields'
        ax.scatter(x, y, s=34 if full else 22, color=COLORS['B2'] if full else COLORS['B1'], zorder=3,
                   edgecolor='white', linewidth=1)
        ax.annotate(r['variant'], (x, y), xytext=offsets[r['variant']], textcoords='offset points', fontsize=6, color=INK)
    ax.set_xlabel('False-flag rate on legitimate variants (lower is better)')
    ax.set_ylabel('Macro recall on constructed errors')
    ax.set_xlim(-.03, .62)
    ax.set_ylim(.3, 1.08)
    save(fig, 'fig_ablation')


def figure_sensitivity():
    rows = list(csv.DictReader((RES / 'sensitivity.csv').open(encoding='utf-8')))
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.1), sharey=True)
    for ax, parameter, title in zip(axes, ('title_threshold', 'author_threshold'),
                                    ('(a) Title similarity threshold', '(b) Author Jaccard threshold')):
        sel = [r for r in rows if r['parameter'] == parameter]
        xs = [float(r['value']) for r in sel]
        ax.plot(xs, [float(r['stress_false_flag_rate']) for r in sel], color=COLORS['B2'], linewidth=2, marker='o', markersize=4, label='False-flag rate, legitimate variants')
        ax.plot(xs, [float(r['macro_recall']) for r in sel], color=COLORS['B1'], linewidth=2, linestyle='--', label='Macro recall, constructed errors')
        frozen = next(float(r['value']) for r in sel if r['frozen_operating_point'] == 'True')
        ax.axvline(frozen, color=MUTED, linewidth=.8, linestyle=':')
        ax.text(frozen, .08, ' frozen', fontsize=6, color=MUTED)
        ax.set_title(title, fontsize=8, loc='left', color=INK)
        ax.set_ylim(0, 1.08)
        ax.grid(True, axis='both')
    axes[0].set_ylabel('Rate')
    axes[1].legend(loc='lower left', fontsize=6)
    fig.tight_layout()
    save(fig, 'fig_sensitivity')


if __name__ == '__main__':
    metrics = json.loads((RES / 'metrics.json').read_text(encoding='utf-8'))
    figure_detection_vs_false_flags(metrics)
    figure_ablation()
    figure_sensitivity()
    print('written:', sorted(p.name for p in OUT.iterdir()))
