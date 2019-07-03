from SPARQLWrapper import SPARQLWrapper, JSON
import json


class ArtistInfo:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.result = None
        self.GetAlbumDetails()

    def GetAlbumDetails(self):
        pl = self.artist_name
        if "_" in pl:
            pl = pl.split("_")
            try:
                # pl = " ".join(pl[0:2])
                pl = pl[0]
            except IndexError:
                pl = " ".join(pl[0:1])
        self.artist_name = pl
        self.artist_name = '"{}"'.format(self.artist_name)
        self.query()

    def query(self):
        query_string = """
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix nm:<http://dbpedia.org/resource/>
            prefix dbo:<http://dbpedia.org/ontology/>
            prefix dbp:<http://dbpedia.org/property/>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT distinct 
                replace(STR(?artist), nm:,"") as ?artist,
                replace(STR(?year_active), nm:,"") as ?year_active, 
                replace(STR(?birth_date),nm:,"") as ?birth_date,
                replace(STR(?birth_place),nm:,"") as ?birth_place,
                replace(STR(?genre),nm:,"") as ?genre,
                replace(STR(?description),nm:,"") as ?description
            WHERE{
                ?album a dbo:Album .
                ?album dbo:artist ?artist.
                ?artist dbo:birthDate ?birth_date.
                ?artist dbo:birthPlace ?birth_place.
                ?artist dbo:abstract ?description.
                ?artist dbo:activeYearsStartYear ?year_active.
                ?artist dbo:genre  ?genre.
            
            FILTER (lang(?description)= "en" && REGEX(?artist,""" + self.artist_name + ""","i"))
            }
            LIMIT 100
        """

        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        genres = []
        nm = []
        for i in results["results"]["bindings"]:
            name = i['artist']['value']
            if len(nm) == 0:
                nm.append(name)
            if name in nm:
                try:
                    dob = i['birth_date']['value']
                except KeyError:
                    dob = "--"
                try:
                    Desc = i['description']['value']
                except KeyError:
                    Desc = "Not Available"
                try:
                    year_active = i['year_active']['value']
                except KeyError:
                    year_active = "="
                try:
                    cntry = i['birth_place']['value']
                except KeyError:
                    cntry = "--"
                try:
                    genres.append(i['genre']['value'])
                except KeyError:
                    genres.append("--")


            else:
                break

        genres = list(dict.fromkeys(genres))

        self.result = json.dumps({
            "name": nm[0].replace("http://dbpedia.org/resource/", ""),
            "genre": genres,
            "dob": dob,
            "Desc": Desc,
            "image": year_active,
            "cntry": cntry,

        })
