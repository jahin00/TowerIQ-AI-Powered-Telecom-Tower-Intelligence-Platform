from pathlib import Path
import json, sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from toweriq_engine import TowerIQEngine, compact_json
from llm_client import LLMClient

st.set_page_config(page_title='TowerIQ Investigation Console', layout='wide')
st.title('TowerIQ Investigation Console')
st.caption('Evidence-first natural-language investigation for telecom tower analytics')

engine = TowerIQEngine(ROOT / 'toweriq.db')
llm = LLMClient()

with st.sidebar:
    st.subheader('Investigation controls')
    st.write('Mode:', 'LLM + evidence' if llm.configured else 'Evidence-only')
    st.write('Database:', str(ROOT / 'toweriq.db'))
    st.divider()
    st.write('Guardrails')
    st.write('• Read-only SQL')
    st.write('• Evidence before explanation')
    st.write('• No unsupported causality')
    st.write('• Max 200 result rows')

q = st.text_input('Ask a TowerIQ question', placeholder='Why did tower T0148 decline?')
examples = [
    'Why did tower T0148 decline?',
    'Which towers are declining?',
    'How are the regions performing?',
    'What is the current data quality status?'
]
st.write('Examples:', ' · '.join(examples))

if q:
    try:
        packet = engine.build_evidence(q)
        st.subheader('Evidence packet')
        st.json(packet['evidence'])

        system = (ROOT / 'prompts' / 'investigation_system.txt').read_text()
        user = f"Question: {q}\n\nEvidence packet:\n{compact_json(packet)}"
        if llm.configured:
            answer = llm.answer(system, user)
        else:
            answer = 'Evidence-only mode: configure TOWERIQ_API_KEY to enable the LLM explanation layer. The evidence above is the source of truth.'
        st.subheader('Investigation result')
        st.write(answer)
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader('Network snapshot')
s = engine.executive_snapshot()
a,b,c,d = st.columns(4)
a.metric('Latest revenue', f"{s['total_revenue']:,.0f}")
b.metric('Revenue MoM', f"{s['revenue_mom_pct']:.2f}%")
c.metric('Avg tenancy', f"{s['avg_tenancy_pct']:.2f}%")
d.metric('Avg downtime', f"{s['avg_downtime_hours']:.2f} h")

st.caption(f"Latest month: {s['latest_month']} | Raw rows: {s['data_quality']['raw_rows']:,} | Quality-flagged: {s['data_quality']['quality_flagged_rows']:,} | Clean rows: {s['data_quality']['clean_rows']:,}")
