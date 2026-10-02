import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from toweriq_engine import TowerIQEngine
DB = Path(__file__).resolve().parents[1] / 'database' / 'toweriq.db'
def test_read_only_validation():
    e = TowerIQEngine(DB)
    assert e.validate_sql('SELECT 1')[0]
    assert not e.validate_sql('DELETE FROM tower_operations_raw')[0]
    e.close()
def test_decliners_and_quality():
    e = TowerIQEngine(DB)
    assert len(e.top_decliners(5)) == 5
    q = e.quality_summary()
    assert q['raw_rows'] >= q['clean_rows']
    e.close()
