import os
KLANG = os.environ.get('KLANG', 'tr')
SUF = '' if KLANG == 'tr' else '_' + KLANG
OPTS = {
    'tr': {'country': 'TR', 'city': 'Eskişehir', 'name': 'Sabri Asfaltoğlu', 'rival': 'Necmi Kaldırım', 'party': 'Demlik Partisi'},
    'en': {'country': 'US', 'city': None, 'name': 'Rick Asphalt', 'rival': 'Ned Sidewalk', 'party': 'Kettle Party'},
}[KLANG]
NEWGAME = """(o) => { const {G,Screens,U,P}=window.__cbs; const opts=Object.assign(%s, o||{});
  const C0 = COUNTRIES.find(c=>c.code===opts.country);
  G.newGame({country:opts.country, name: opts.name, city: opts.city||C0.cities[0],
    look:{skin:'#e8b48f',hair:2,hairColor:'#3a2a1e',facial:0,glasses:0,suit:'#2b3350',tie:'#8a4fd8'},
    style: 'people', partyName: opts.party, partyColor: '#8a4fd8'});
  G.S.rival.name = opts.rival; G.S.rival.look = {skin:'#f6d3b3',hair:1,hairColor:'#b5452e',facial:0,glasses:0,suit:'#5a5f6b',tie:'#eeeeee'};
  document.documentElement.style.setProperty('--party', G.S.party.color);
  document.documentElement.style.setProperty('--party-dk', U.shade(G.S.party.color, -0.4));
  return {rival:G.S.rival.name, city: G.S.city};
}""" % __import__('json').dumps(OPTS)
