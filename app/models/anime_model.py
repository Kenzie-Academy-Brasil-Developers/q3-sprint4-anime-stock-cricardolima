from app.models import DatabaseConnector

class Anime(DatabaseConnector):
    anime_keys = ["anime", "released_date", "seasons"]
    
    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']
        
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