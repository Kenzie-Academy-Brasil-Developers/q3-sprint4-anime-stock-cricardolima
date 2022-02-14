from app.models import DatabaseConnector

class Anime(DatabaseConnector):
    anime_keys = ["id", "anime", "released_date", "seasons"]
    
    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime'].title()
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']
    
    def create_anime(self):
        self.create_table()
        self.get_conn_cur()
        query = """
            INSERT INTO 
                animes(anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """
        query_values = list(self.__dict__.values())
        self.cur.execute(query, query_values)
        inserted_anime = self.cur.fetchone()
        self.commit_and_close()
        return inserted_anime
        
    @staticmethod
    def serialize_anime(data, keys=anime_keys):
        if type(data) is tuple:
            return dict(zip(keys, data))
        if type(data) is list:
            return [dict(zip(keys, anime)) for anime in data]
    
    @classmethod   
    def get_all(cls):
        cls.create_table()
        cls.get_conn_cur()
        query = """SELECT * FROM anime; """
        cls.cur.execute(query)
        animes = cls.cur.fetchall()
        cls.commit_and_close()
        return animes