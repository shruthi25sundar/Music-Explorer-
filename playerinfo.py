from SPARQLWrapper import SPARQLWrapper, JSON
import json


class PlayerInfo:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def __init__(self, player_name):
        self.player_name = player_name
        self.result = None
        self.result2 = None
        self.name_pre_process()

    def name_pre_process(self):
        pl = self.player_name
        if "_" in pl:
            pl = pl.split("_")
            try:
                pl = " ".join(pl[0:2])
            except IndexError:
                pl = " ".join(pl[0:1])
        self.player_name = pl
        self.player_name = '"{}"'.format(self.player_name)
        self.query()

    def query(self):
        query_string = """prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix nm:<http://dbpedia.org/resource/>
prefix dbo:<http://dbpedia.org/ontology/>
prefix dbp:<http://dbpedia.org/property/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?player, MIN(replace(?birthDate,xsd:,""))as ?birthDate , replace(str(?country), nm:, "") as ?country, replace(str(?clubs), nm:, "") as ?clubs, ?thumbnail, MIN(?comment) as ?comment
WHERE {
?player a dbo:Cricketer ; rdfs:label ?name ;dbp:international "true"^^rdf:langString .
FILTER (lang(?name)= "en" && REGEX(?name,"""+self.player_name+""","i") && lang(?comment)= "en")
OPTIONAL {?player dbp:club ?clubs .}
OPTIONAL {?player dbo:birthDate ?birthDate .}
OPTIONAL {?player dbo:country ?country .}
OPTIONAL {?player dbo:thumbnail ?thumbnail .}
OPTIONAL {?player rdfs:comment ?comment.}
}
ORDER BY ?name"""
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        clubs = []
        nm = []
        for i in results["results"]["bindings"]:
            name = i['player']['value']
            if len(nm) == 0:
                nm.append(name)
            if name in nm:
                try:
                    dob = i['birthDate']['value']
                except KeyError:
                    dob = "--"
                try:
                    Desc = i['comment']['value']
                except KeyError:
                    Desc = "Not Available"
                try:
                    img = i['thumbnail']['value']
                except KeyError:
                    img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/No_image_available_500_x_500.svg/2000px-No_image_available_500_x_500.svg.png'
                try:
                    cntry = i['country']['value']
                except KeyError:
                    cntry = "--"
                try:
                    clubs.append(i['clubs']['value'])
                except KeyError:
                    clubs.append("--")
            else:
                break
        self.result = json.dumps({"name": nm[0].replace("http://dbpedia.org/resource/", ""), "Clubs": clubs,
                                  "dob": dob, "Desc": Desc, "image": img, "cntry": cntry})
        player_name = nm[0].replace("http://dbpedia.org/resource/", "")
        player_name = player_name.split("_")
        if len(player_name) > 2:
            player_name = "_".join(player_name[0:2])
        else:
            player_name = "_".join(player_name)
        player_name = '"{}"'.format(player_name)
        query_string1 = """prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                            prefix nm:<http://dbpedia.org/resource/>
                                            prefix dbo:<http://dbpedia.org/ontology/>
                                            prefix dbp:<http://dbpedia.org/property/>
                                            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                            prefix xsd: <http://www.w3.org/2001/XMLSchema#>

                                            SELECT DISTINCT ?name,
                                            MAX(?hundreds) as ?hundreds, MAX(?batAvg) as ?batAvg, MAX(?bestBowling) as ?bestBowling, MIN(?bowlAvg) as ?bowlAvg, MIN(?role) as ?role, MAX(?runs) as ?runs, MAX(?topScore) as ?topScore, MAX(?wickets) as ?bestWickets, MIN(?externalLink) as ?externalLink
                                            WHERE {
?player a dbo:Cricketer ; rdfs:label ?name.
?player dbp:international "true"^^rdf:langString .
FILTER (lang(?name)= "en" && REGEX(?player,"""+player_name+""","i"))
OPTIONAL {?player <http://dbpedia.org/property/100s/50s> ?hundreds. }
OPTIONAL {?player dbp:batAvg ?batAvg. }
OPTIONAL {?player dbp:bestBowling ?bestBowling. }
OPTIONAL {?player dbp:bowlAvg ?bowlAvg. }
OPTIONAL {?player dbp:role ?role. }
OPTIONAL {?player dbp:runs ?runs . }
OPTIONAL {?player dbp:topScore ?topScore . }
OPTIONAL {?player dbp:wickets ?wickets. }
OPTIONAL {?player dbo:wikiPageExternalLink ?externalLink. }
}Limit 1"""

        self.sparql.setQuery(query_string1)
        self.sparql.setReturnFormat(JSON)
        results2 = self.sparql.query().convert()
        #print(results2)
        for i in results2['results']['bindings']:
            print(1)
            try:
                topScore = i['topScore']['value']
            except KeyError:
                topScore = "--"
            try:
                bestWickets = i['bestWickets']['value']
            except KeyError:
                bestWickets = "--"
            try:
                runs = i['runs']['value']
            except KeyError:
                runs = "--"
            try:
                externalLink = i['externalLink']['value']
            except:
                externalLink = "--"
            try:
                role = i['role']['value']
            except KeyError:
                role = "--"
            try:
                bowlAvg = i['bowlAvg']['value']
            except KeyError:
                bowlAvg = "--"
            try:
                name = i['name']['value']
            except KeyError:
                name = "--"
            try:
                batAvg = i['batAvg']['value']
            except KeyError:
                batAvg = "--"
            try:
                bestBowling = i['bestBowling']['value']
            except KeyError:
                bestBowling = "--"
            try:
                hundreds = i['hundreds']['value']
            except KeyError:
                hundreds = "--"

        self.result2 = json.dumps({"topScore": topScore, "bestWickets": bestWickets, "runs": runs,
                                   "externalLink": externalLink,
                                   "role": role.replace("http://dbpedia.org/resource/", ""), "bowlAvg": bowlAvg,
                                   "name": name, "batAvg": batAvg, "bestBowling": bestBowling, "hundreds": hundreds})

