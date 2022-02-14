from app.models import DatabaseConnector
from psycopg2 import sql

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
        query = """SELECT * FROM animes; """
        cls.cur.execute(query)
        animes = cls.cur.fetchall()
        cls.commit_and_close()
        return animes
    
    @classmethod
    def get_by_id(cls, id):
        cls.create_table()
        cls.get_conn_cur()

        query = sql.SQL("""
            SELECT * FROM
                animes
            WHERE
                id = {id}
        """).format(id=sql.Literal(id))

        cls.cur.execute(query)
        anime = cls.cur.fetchone()
        cls.commit_and_close()
        return anime
    
    @classmethod
    def update_anime(cls, id, data):
        cls.get_conn_cur()
        print(id)
        keys = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
                UPDATE 
                    animes
                SET
                    ({keys}) = ROW({values})
                WHERE
                    id={id}
                RETURNING *;
            """
        ).format(
            id=sql.Literal(id),
            keys=sql.SQL(",").join(keys),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)
        updated_anime = cls.cur.fetchone()
        print(updated_anime)
        cls.commit_and_close()
       
        return updated_anime
    
    @classmethod
    def delete_anime(cls, anime_id):
        cls.get_conn_cur()
        query = f"DELETE FROM animes WHERE id = {anime_id} RETURNING *;"
        
        cls.cur.execute(query)
        deleted_anime = cls.cur.fetchone()
        cls.commit_and_close()
        return deleted_anime