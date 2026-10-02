from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from toweriq_engine import TowerIQEngine

ROOT = Path(__file__).resolve().parents[1]

def money(x): return f"{x:,.0f}"

def build_report(engine):
    s = engine.executive_snapshot()
    lines = [
        '# TowerIQ Network Investigation Report',
        '',
        f"**Reporting month:** {s['latest_month']}",
        '',
        '## Executive snapshot',
        f"- Total revenue: {money(s['total_revenue'])}",
        f"- Revenue MoM: {s['revenue_mom_pct']:.2f}%",
        f"- Average tenancy: {s['avg_tenancy_pct']:.2f}%",
        f"- Average downtime: {s['avg_downtime_hours']:.2f} hours",
        '',
        '## Latest-month declining towers',
        '',
        '| Tower | Region | Revenue | MoM change | Tenant change | Downtime | Incidents |',
        '|---|---|---:|---:|---:|---:|---:|',
    ]
    for r in s['top_decliners']:
        lines.append(f"| {r['tower_id']} | {r['region_name']} | {money(r['revenue'])} | {r['revenue_change_pct']:.2f}% | {r['tenant_change']} | {r['downtime_hours']:.2f} h | {r['incidents']} |")
    lines += ['', '## Regional context', '', '| Region | Revenue | Avg tenancy | Avg downtime | Incidents |', '|---|---:|---:|---:|---:|']
    for r in s['regions']:
        lines.append(f"| {r['region_name']} | {money(r['total_revenue'])} | {r['avg_tenancy_pct']:.2f}% | {r['avg_downtime_hours']:.2f} h | {r['total_incidents']:,} |")
    q=s['data_quality']
    lines += ['', '## Data quality', f"- Raw rows: {q['raw_rows']:,}", f"- Quality-flagged rows: {q['quality_flagged_rows']:,}", f"- Clean analytical rows: {q['clean_rows']:,}", '', '## Analytical note', 'Observed co-movement between revenue, tenancy, downtime and incidents should be treated as evidence for investigation, not automatic proof of causation.']
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    eng=TowerIQEngine(ROOT/'toweriq.db')
    out=ROOT/'reports'/'network_investigation_report.md'
    out.write_text(build_report(eng), encoding='utf-8')
    print(out)
