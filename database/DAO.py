from database.DB_connect import DBConnect
from model.name import Name


class DAO():

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT avg_rating
                    FROM ratings
                    ORDER BY avg_rating"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(r1, r2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.*
                    FROM names n, role_mapping r, movie m, ratings ra
                    WHERE n.id = r.name_id
                    AND r.movie_id = m.id
                    AND m.id = ra.movie_id
                    AND ra.avg_rating BETWEEN %s AND %s
                    AND n.date_of_birth IS NOT NULL"""

        cursor.execute(query, (r1, r2))

        for row in cursor:
            results.append(Name(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllEdges(r1, r2, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.idActor as n1, t2.idActor as n2, t1.incasso as incasso
                    FROM
                        (SELECT n.id as idActor, m.id as idMovie, m.worlwide_gross_income as incasso
                        FROM names n, role_mapping r, movie m, ratings ra
                        WHERE n.id = r.name_id
                        AND r.movie_id = m.id
                        AND m.id = ra.movie_id
                        AND ra.avg_rating BETWEEN %s AND %s
                        AND n.date_of_birth IS NOT NULL
                         AND m.worlwide_gross_income LIKE '$%') t1,
                        (SELECT n.id as idActor, m.id as idMovie, m.worlwide_gross_income as incasso
                        FROM names n, role_mapping r, movie m, ratings ra
                        WHERE n.id = r.name_id
                        AND r.movie_id = m.id
                        AND m.id = ra.movie_id
                        AND ra.avg_rating BETWEEN %s AND %s
                        AND n.date_of_birth IS NOT NULL
                        AND m.worlwide_gross_income LIKE '$%') t2
                    WHERE t1.idActor < t2.idActor
                    AND t1.idMovie = t2.idMovie"""


        # e poi in python converto stringa $incassi in numeri da sommare
        # oppure lo faccio direttamente qui:
        # faccio group by t1.idActor, t2.idActor, e sum(t1.incasso) as peso
        # per avere quei t1.incasso come numeri, nelle sottoquryy faccio
        # SELECT n.id as idActor, m.id as idMovie, m.worlwide_gross_income as incasso
        # anzichè m.worlwide_gross_income as incasso
        # metto CAST(REPLACE(REPLACE(m.worlwide_gross_income, '$', ''), ',', '') AS UNSIGNED) AS incasso

        cursor.execute(query, (r1, r2, r1, r2))

        for row in cursor:
            results.append((idMap[row["n1"]], idMap[row["n2"]], row["incasso"]))

        cursor.close()
        conn.close()
        return results
