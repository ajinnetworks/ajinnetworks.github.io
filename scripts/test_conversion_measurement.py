from pathlib import Path

config = Path('_config.yml').read_text(encoding='utf-8')
default = Path('_layouts/default.html').read_text(encoding='utf-8')
js = Path('assets/js/conversion-tracking.js').read_text(encoding='utf-8')

assert 'google_analytics:' in config and 'G-' in config, 'GA4 measurement id missing'
assert 'conversion-tracking.js' in default, 'conversion tracking script not loaded'
for event in ('rfq_cta_click', 'pillar_cluster_click', 'company_site_click'):
    assert event in js, f'missing event: {event}'
for key in ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content'):
    assert key in js, f'missing attribution key: {key}'
assert 'https://www.ajinnetworks.co.kr/' in js, 'official company destination missing'
for pii in ('phone_number', 'customer_name', 'email_address', 'quotation_amount'):
    assert pii not in js, f'PII field must not be tracked: {pii}'
assert 'data-phase36-rfq' in js, 'RFQ CTA injection missing'
print('PHASE 3-6 CONVERSION MEASUREMENT TEST: PASS')
