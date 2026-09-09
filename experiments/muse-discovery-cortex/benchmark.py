from discovery_cortex import baseline, discovery

CASES = [
('Reduce congestion in a city without simply adding roads.', ['feedback control','traffic routing']),
('How could an AI detect and correct its own reasoning errors?', ['debugging','contradiction search']),
('How can decentralized systems adapt without a central controller?', ['ant colony foraging','feedback control']),
('How might pricing become more stable when demand changes quickly?', ['market pricing','feedback control']),
('How can an AI decide what information deserves attention?', ['meta-attention','knowledge graph']),
('How could experiments efficiently resolve uncertain beliefs?', ['scientific experiment','contradiction search']),
('How can a system use relationships rather than isolated facts?', ['knowledge graph','scientific experiment']),
('How can an organization respond to repeated operational errors?', ['debugging','immune response']),
('How can a network adapt to changing load?', ['traffic routing','feedback control']),
('How can a learning system turn conflict into useful discovery?', ['contradiction search','scientific experiment']),
('How can distributed agents find resources efficiently?', ['ant colony foraging','traffic routing']),
('How can an autonomous agent notice blind spots in its own plan?', ['meta-attention','scientific experiment']),
('How can biological adaptation inspire robust software systems?', ['immune response','debugging']),
]

def hit_baseline(prompt, expected):
    return int(bool(set(baseline(prompt)) & set(expected)))

def hit_discovery(prompt, expected):
    bridges=discovery(prompt)['bridges']
    names={x['from'] for x in bridges}|{x['to'] for x in bridges}
    return int(bool(names & set(expected)))

if __name__=='__main__':
    b=d=0
    print('Muse Discovery Cortex pilot benchmark')
    print('-'*60)
    for i,(prompt,expected) in enumerate(CASES,1):
        hb=hit_baseline(prompt,expected); hd=hit_discovery(prompt,expected)
        b+=hb; d+=hd
        print(f'{i:02d} baseline={hb} discovery={hd} | {prompt}')
    print('-'*60)
    print(f'baseline_hits={b}/13 ({b/13:.1%})')
    print(f'discovery_hits={d}/13 ({d/13:.1%})')
    print(f'improvement={(d-b)/13:.1%}')
    assert d>b, 'Discovery Cortex did not beat baseline on this pilot.'
