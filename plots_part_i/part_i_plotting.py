"""
Plotting script for Part I (sector coupling) results.
Reads CSVs written by part_i/part_i.py from the same directory.
Run from the project root:  python plots_part_i/part_i_plotting.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Resolve paths relative to this file so the script works from any cwd
DIR = os.path.dirname(os.path.abspath(__file__))

def csv(name):
    return os.path.join(DIR, name)

# =============================================================================
# LOAD DATA
# =============================================================================
cap_elec   = pd.read_csv(csv('cap_elec_table.csv'),   index_col=0)
cap_heat   = pd.read_csv(csv('cap_heat_table.csv'),   index_col=0)
gen_mix    = pd.read_csv(csv('generation_mix.csv'),   index_col=0).squeeze()
heat_supply = pd.read_csv(csv('heat_supply_mix.csv'), index_col=0)
dispatch   = pd.read_csv(csv('dispatch_by_tech.csv'), index_col=0, parse_dates=True)
heat_dnk   = pd.read_csv(csv('heat_dispatch_dnk.csv'), index_col=0, parse_dates=True)

# Electricity techs that belong on electricity buses
ELEC_TECHS   = ["Onshore wind", "Offshore wind", "Solar", "OCGT", "CCGT",
                 "battery storage", "pumped hydro"]
ELEC_LABELS  = ["Onshore wind", "Offshore wind", "Solar PV", "Gas (OCGT)",
                 "Gas (CCGT)", "Battery storage", "Hydro"]
ELEC_COLORS  = ['blue', 'dodgerblue', 'orange', 'crimson',
                 'darkviolet', 'lightgreen', 'pink']

HEAT_LABELS  = ["Heat pump", "Gas boiler"]
HEAT_COLORS  = ['teal', 'saddlebrown']

COUNTRY_ORDER = ["Denmark", "Sweden", "Norway", "Germany"]

# Restrict electricity dispatch to electricity-relevant techs only
elec_dispatch = dispatch[[c for c in ELEC_TECHS if c in dispatch.columns]]

# =============================================================================
# 1. ELECTRICITY INSTALLED CAPACITY — stacked bar by country
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
cap_elec.reindex(COUNTRY_ORDER).plot(
    kind="bar", stacked=True,
    color=ELEC_COLORS, rot=0, ax=ax
)
ax.set_ylabel("Installed capacity [GW]")
ax.set_xlabel("")
ax.set_title("Electricity installed capacity by country", fontweight='bold')
ax.legend(ELEC_LABELS, loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_elec_capacity_by_country.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_elec_capacity_by_country.png")

# =============================================================================
# 2. TOTAL ELECTRICITY INSTALLED CAPACITY — pie chart
# =============================================================================
total_elec = cap_elec.reindex(COUNTRY_ORDER).sum()
total_elec = total_elec[total_elec > 0]
labels_pie = [f"{l}\n{p:.1f}%"
              for l, p in zip(
                  [ELEC_LABELS[ELEC_TECHS.index(t)] for t in total_elec.index],
                  100 * total_elec / total_elec.sum()
              )]
colors_pie = [ELEC_COLORS[ELEC_TECHS.index(t)] for t in total_elec.index]

fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
ax.pie(total_elec, labels=labels_pie, colors=colors_pie,
       startangle=90, labeldistance=1.18)
ax.set_title("Total electricity installed capacity", y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_elec_capacity_total_pie.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_elec_capacity_total_pie.png")

# =============================================================================
# 3. ANNUAL ELECTRICITY GENERATION MIX — pie chart
# =============================================================================
gen_plot = gen_mix.reindex(ELEC_TECHS).fillna(0)
gen_plot = gen_plot[gen_plot > 0]
gen_labels_pie = [f"{l}\n{p:.1f}%"
                  for l, p in zip(
                      [ELEC_LABELS[ELEC_TECHS.index(t)] for t in gen_plot.index],
                      100 * gen_plot / gen_plot.sum()
                  )]
gen_colors_pie = [ELEC_COLORS[ELEC_TECHS.index(t)] for t in gen_plot.index]

fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
ax.pie(gen_plot, labels=gen_labels_pie, colors=gen_colors_pie,
       startangle=90, labeldistance=1.18, wedgeprops={'linewidth': 0})
ax.set_title("Annual electricity generation mix", y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_generation_mix_pie.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_generation_mix_pie.png")

# =============================================================================
# 4. HEAT INSTALLED CAPACITY — stacked bar by country
# =============================================================================
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
cap_heat.reindex(COUNTRY_ORDER).plot(
    kind="bar", stacked=True,
    color=HEAT_COLORS, rot=0, ax=ax
)
ax.set_ylabel("Installed capacity [GW]")
ax.set_xlabel("")
ax.set_title("Heat installed capacity by country", fontweight='bold')
ax.legend(HEAT_LABELS, loc='upper right', fontsize='small')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_heat_capacity_by_country.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_heat_capacity_by_country.png")

# =============================================================================
# 5. ANNUAL HEAT SUPPLY MIX — stacked bar by country
# =============================================================================
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
heat_supply.reindex(COUNTRY_ORDER).plot(
    kind="bar", stacked=True,
    color=HEAT_COLORS, rot=0, ax=ax
)
ax.set_ylabel("Annual heat supply [TWh]")
ax.set_xlabel("")
ax.set_title("Annual heat supply by country", fontweight='bold')
ax.legend(HEAT_LABELS, loc='upper right', fontsize='small')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_heat_supply_by_country.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_heat_supply_by_country.png")

# =============================================================================
# 6. DURATION CURVE — sorted dispatch by electricity technology
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
for tech, label, color in zip(ELEC_TECHS, ELEC_LABELS, ELEC_COLORS):
    if tech in elec_dispatch.columns:
        sorted_vals = elec_dispatch[tech].sort_values(ascending=False).reset_index(drop=True)
        ax.plot(sorted_vals, label=label, color=color, lw=2)
ax.axhline(0, color='black', lw=0.8)
ax.set_ylabel("Dispatch [MWh/h]")
ax.set_xlabel("Hours")
ax.set_title("Duration curve of electricity generation and storage", fontweight='bold')
ax.legend(fancybox=True, shadow=True, loc='upper right', fontsize='small')
plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_duration_curve.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_duration_curve.png")

# =============================================================================
# 7. DNK HEAT DISPATCH — weekly sample (winter vs summer)
# =============================================================================
fig, axes = plt.subplots(2, 1, figsize=(10, 6), dpi=300, sharex=False)

for ax, (label, start) in zip(axes, [("Winter (Jan)", "2015-01-05"),
                                       ("Summer (Jul)", "2015-07-06")]):
    week = heat_dnk.loc[start: pd.Timestamp(start) + pd.Timedelta(hours=167)]
    ax.stackplot(range(len(week)),
                 week["heat pump"].values,
                 week["gas boiler"].values,
                 labels=HEAT_LABELS, colors=HEAT_COLORS, alpha=0.85)
    ax.set_ylabel("Heat [MWh/h]")
    ax.set_title(f"Denmark heat dispatch — {label}", fontweight='bold')
    ax.legend(loc='upper right', fontsize='small')
    ax.set_xticks(range(0, len(week), 24))
    ax.set_xticklabels([f"Day {i+1}" for i in range(len(week) // 24)], fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(DIR, 'fig_dnk_heat_dispatch.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: fig_dnk_heat_dispatch.png")

print("\nAll plots saved to", DIR)
