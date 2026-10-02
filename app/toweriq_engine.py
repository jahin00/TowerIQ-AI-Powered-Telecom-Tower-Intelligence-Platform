from __future__ import annotations
import json, re, sqlite3
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / 'toweriq.db'

ALLOWED_PREFIX = re.compile(r'^\s*(select|with)\b', re.I)
BLOCKED = re.compile(r'\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum|reindex|transaction|commit|rollback)\b', re.I)
MAX_ROWS = 200

SCHEMA_HINT = {
    'v_tower_monthly_kpi': [
        'tower_id','region_id','region_name','tower_type','month','revenue',
        'operating_cost','active_tenants','available_slots','downtime_hours',
        'incidents','maintenance_cost','tenancy_rate','revenue_per_tenant',
        'estimated_operating_margin','previous_revenue','revenue_change_pct',
        'previous_tenants','tenant_change','previous_downtime'
    ],
    'tower_data_quality': [
        'raw_row_id','tower_id','region_id','region_name_std','tower_type','month_raw',
        'revenue','active_tenants','available_slots','downtime_hours','month_std',
        'duplicate_count','bad_revenue_flag','bad_tenancy_flag','bad_downtime_flag',
        'bad_region_flag','bad_date_flag','has_quality_issue'
    ]
}

class TowerIQEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA query_only = ON')
        self.conn.execute('PRAGMA busy_timeout = 3000')

    def close(self):
        self.conn.close()

    def schema(self) -> dict[str, list[str]]:
        out = {}
        rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY name").fetchall()
        for r in rows:
            name = r['name']
            cols = self.conn.execute(f'PRAGMA table_info("{name}")').fetchall()
            out[name] = [c['name'] for c in cols]
        return out

    def validate_sql(self, sql: str) -> tuple[bool, str]:
        s = sql.strip().rstrip(';').strip()
        if not ALLOWED_PREFIX.match(s):
            return False, 'Only SELECT/WITH read-only queries are allowed.'
        if BLOCKED.search(s):
            return False, 'Blocked SQL keyword detected. The investigation layer is read-only.'
        if '--' in s or '/*' in s or '*/' in s:
            return False, 'SQL comments are disabled for generated queries.'
        if s.count(';'):
            return False, 'Multiple SQL statements are not allowed.'
        return True, 'OK'

    def run_query(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        ok, msg = self.validate_sql(sql)
        if not ok:
            raise ValueError(msg)
        wrapped = f'SELECT * FROM ({sql.rstrip(";")}) LIMIT {MAX_ROWS}'
        rows = self.conn.execute(wrapped, params).fetchall()
        return [dict(r) for r in rows]

    def evidence_for_tower(self, tower_id: str) -> dict[str, Any]:
        q = '''
        SELECT tower_id, region_name, tower_type, month, revenue,
               active_tenants, available_slots, tenancy_rate, downtime_hours,
               incidents, operating_cost, maintenance_cost, revenue_per_tenant,
               estimated_operating_margin, previous_revenue, revenue_change_pct,
               previous_tenants, tenant_change, previous_downtime
        FROM v_tower_monthly_kpi
        WHERE tower_id = ?
        ORDER BY month DESC
        LIMIT 24
        '''
        rows = [dict(r) for r in self.conn.execute(q, (tower_id,)).fetchall()]
        if not rows:
            raise ValueError(f'Unknown tower_id: {tower_id}')
        latest = rows[0]
        return {'tower_id': tower_id, 'latest': latest, 'history_24_months': rows}

    def top_decliners(self, limit: int = 10) -> list[dict[str, Any]]:
        q = '''SELECT tower_id, region_name, month, revenue, revenue_change_pct,
                      active_tenants, tenant_change, downtime_hours, incidents
               FROM v_tower_monthly_kpi
               WHERE revenue_change_pct IS NOT NULL
                 AND month = (SELECT MAX(month) FROM v_tower_monthly_kpi)
               ORDER BY revenue_change_pct ASC LIMIT ?'''
        return [dict(r) for r in self.conn.execute(q, (limit,)).fetchall()]

    def region_summary(self) -> list[dict[str, Any]]:
        q = '''SELECT region_name,
                      ROUND(SUM(revenue),2) total_revenue,
                      ROUND(AVG(tenancy_rate)*100,2) avg_tenancy_pct,
                      ROUND(AVG(downtime_hours),2) avg_downtime_hours,
                      SUM(incidents) total_incidents
               FROM v_tower_monthly_kpi
               GROUP BY region_name ORDER BY total_revenue DESC'''
        return [dict(r) for r in self.conn.execute(q).fetchall()]

    def monthly_summary(self) -> list[dict[str, Any]]:
        q = '''SELECT month, ROUND(SUM(revenue),2) total_revenue,
                      ROUND(AVG(tenancy_rate)*100,2) avg_tenancy_pct,
                      ROUND(AVG(downtime_hours),2) avg_downtime_hours
               FROM v_tower_monthly_kpi GROUP BY month ORDER BY month'''
        return [dict(r) for r in self.conn.execute(q).fetchall()]

    def quality_summary(self) -> dict[str, Any]:
        total = self.conn.execute('SELECT COUNT(*) n FROM tower_operations_raw').fetchone()['n']
        flagged = self.conn.execute('SELECT COUNT(*) n FROM tower_data_quality WHERE has_quality_issue=1').fetchone()['n']
        clean = self.conn.execute('SELECT COUNT(*) n FROM tower_monthly_clean').fetchone()['n']
        return {'raw_rows': total, 'quality_flagged_rows': flagged, 'clean_rows': clean}

    def build_evidence(self, question: str) -> dict[str, Any]:
        q = question.lower()
        m = re.search(r'\b(t\d{4})\b', q)
        if m:
            return {'question': question, 'intent': 'tower_investigation', 'evidence': self.evidence_for_tower(m.group(1).upper())}
        if 'declin' in q or 'fall' in q or 'drop' in q:
            return {'question': question, 'intent': 'declining_towers', 'evidence': self.top_decliners(10)}
        if 'region' in q or 'regional' in q:
            return {'question': question, 'intent': 'regional_summary', 'evidence': self.region_summary()}
        if 'quality' in q or 'missing' in q or 'duplicate' in q:
            return {'question': question, 'intent': 'data_quality', 'evidence': self.quality_summary()}
        return {'question': question, 'intent': 'monthly_summary', 'evidence': self.monthly_summary()}

    def executive_snapshot(self) -> dict[str, Any]:
        monthly = self.monthly_summary()
        latest = monthly[-1]
        previous = monthly[-2]
        mom = (latest['total_revenue'] - previous['total_revenue']) / previous['total_revenue'] * 100
        return {
            'latest_month': latest['month'],
            'total_revenue': latest['total_revenue'],
            'revenue_mom_pct': round(mom, 2),
            'avg_tenancy_pct': latest['avg_tenancy_pct'],
            'avg_downtime_hours': latest['avg_downtime_hours'],
            'top_decliners': self.top_decliners(5),
            'regions': self.region_summary(),
            'data_quality': self.quality_summary(),
        }

def compact_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, default=str)
