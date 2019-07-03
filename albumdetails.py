from SPARQLWrapper import SPARQLWrapper, JSON
import json


class AlbumDetail:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def __init__(self, album_name):
        self.album_name = album_name
        self.tm_result = None
        self.GetAlbumDetails()

    def GetAlbumDetails(self):
        album_name = self.album_name.split(" ")[0]
        self.album_name = album_name
        self.Query()

    def Query(self):
        query_string = """
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix nm:<http://dbpedia.org/resource/>
            prefix dbo:<http://dbpedia.org/ontology/>
            prefix dbp:<http://dbpedia.org/property/>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            
            SELECT distinct replace(STR(?album), nm:,"") as ?Album,
            replace(STR(?performer), nm:,"") as ?Artist , 
            replace(STR(?longtype),nm:,"") as ?RunTime,
            replace(STR(?musicType),nm:,"") as ?Genre,
            replace(STR(?compiler),nm:,"") as ?Composer,
            replace(STR(?releasedate),nm:,"") as ?ReleaseDate,
            replace(STR(?comment),nm:,"") as ?Description
            
            WHERE{
                ?album a dbo:Album .
                ?album dbo:artist ?performer.
                ?album dbo:runtime ?longtype.
                ?album dbo:genre   ?musicType.
                ?album dbp:producer ?compiler.
                ?album dbp:released ?releasedate.
                ?album rdfs:comment ?comment.
                FILTER (lang(?comment)= "en" && REGEX(replace(STR(?album), nm:, "") as ?Album,"^""" + self.album_name + """", "i"))
            }
            ORDER BY ?album, ?performer, ?musicType
            LIMIT 3
            """
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        tm_results = self.sparql.query().convert()
        album = []
        artist = []
        runtime = []
        genre = []
        composer = []
        releasedate = []
        description = []

        for i in tm_results["results"]["bindings"]:
            album.append(i['Album']['value'])
            artist.append(i['Artist']['value'])
            runtime.append(i['RunTime']['value'])
            genre.append(i['Genre']['value'])
            composer.append(i['Composer']['value'])
            releasedate.append(i['ReleaseDate']['value'])
            description.append(i['Description']['value'].split("_")[0])

        self.tm_result = json.dumps({
            "album": album,
            "artist": artist,
            "runtime": runtime,
            "genre": genre,
            "composer": composer,
            "releasedate": releasedate,
            "description": description
        })

