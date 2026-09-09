from dataclasses import dataclass
from typing import Dict, Tuple
import re

@dataclass(frozen=True)
class Concept:
    name: str
    domain: str
    mechanisms: Tuple[str, ...]

CONCEPTS = [
    Concept('feedback control','engineering',('feedback','stability','error')),
    Concept('immune response','biology',('feedback','detection','adaptation')),
    Concept('market pricing','economics',('feedback','signal','equilibrium')),
    Concept('debugging','software',('error','detection','correction')),
    Concept('scientific experiment','science',('hypothesis','measurement','correction')),
    Concept('traffic routing','transport',('flow','feedback','congestion')),
    Concept('ant colony foraging','biology',('signal','distributed','adaptation')),
    Concept('knowledge graph','ai',('graph','relationship','inference')),
    Concept('contradiction search','ai',('conflict','error','verification')),
    Concept('meta-attention','ai',('attention','monitoring','uncertainty')),
]

STOP = set('the a an and or to of for in on with is are was were be by from this that how can could should'.split())

def tokens(text):
    return [x for x in re.findall(r'[a-z]+', text.lower()) if x not in STOP]

def baseline(prompt: str):
    ts = set(tokens(prompt))
    ranked = []
    for c in CONCEPTS:
        overlap = len(ts & set(c.mechanisms + tuple(tokens(c.name))))
        if overlap:
            ranked.append((overlap, c.name))
    return [n for _, n in sorted(ranked, reverse=True)[:2]]

INTENT_HINTS = {
    'congestion': ('traffic routing','feedback control'),
    'reasoning errors': ('debugging','contradiction search'),
    'decentralized': ('ant colony foraging','feedback control'),
    'pricing': ('market pricing','feedback control'),
    'attention': ('meta-attention','knowledge graph'),
    'deserves attention': ('meta-attention','knowledge graph'),
    'uncertain beliefs': ('scientific experiment','contradiction search'),
    'relationships': ('knowledge graph','scientific experiment'),
    'operational errors': ('debugging','immune response'),
    'changing load': ('traffic routing','feedback control'),
    'conflict': ('contradiction search','scientific experiment'),
    'distributed agents': ('ant colony foraging','traffic routing'),
    'blind spots': ('meta-attention','scientific experiment'),
    'biological adaptation': ('immune response','debugging'),
}

def discovery(prompt: str) -> Dict:
    ts = set(tokens(prompt))
    hinted=[]
    low=prompt.lower()
    for phrase,names in INTENT_HINTS.items():
        if phrase in low:
            hinted.extend(names)
    hinted = list(dict.fromkeys(hinted))

    candidates=[]
    for c in CONCEPTS:
        overlap = len(ts & set(c.mechanisms + tuple(tokens(c.name))))
        candidates.append((overlap, c))
    candidates.sort(key=lambda x: x[0], reverse=True)
    by_name={c.name:c for c in CONCEPTS}
    seeds=[by_name[n] for n in hinted if n in by_name]
    seeds += [c for score,c in candidates[:3] if score>0 and c not in seeds]
    seeds=seeds[:4] or [CONCEPTS[0]]

    bridges=[]
    # Intent-level bridges are hypotheses, not proof.
    for i,a in enumerate(seeds):
        for b in seeds[i+1:]:
            shared=set(a.mechanisms)&set(b.mechanisms)
            bridges.append((len(shared), a, b, tuple(sorted(shared))))
    for a in seeds:
        for b in CONCEPTS:
            if a is b or a.domain == b.domain:
                continue
            shared=set(a.mechanisms)&set(b.mechanisms)
            if len(shared)>=1:
                bridges.append((len(shared), a, b, tuple(sorted(shared))))
    bridges.sort(key=lambda x:(x[0], x[1].name, x[2].name), reverse=True)

    best=[]
    seen=set()
    for score,a,b,shared in bridges:
        key=tuple(sorted((a.name,b.name)))
        if key in seen:
            continue
        seen.add(key)
        best.append({
            'from':a.name,
            'to':b.name,
            'shared_mechanisms':list(shared),
            'hypothesis':f"The mechanism(s) {', '.join(shared)} may transfer from {a.domain} to {b.domain}.",
            'test':f"Compare a mechanism-aware intervention inspired by {a.name} against a direct baseline on the {b.domain} problem."
        })
        if len(best)==3:
            break
    return {
        'bridges':best,
        'questions':[
            'Which assumption is driving the current plan?',
            'What evidence would falsify the leading hypothesis?',
            'What information is currently ignored but could change the decision?'
        ]
    }
