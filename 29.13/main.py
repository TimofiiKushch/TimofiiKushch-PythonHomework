import cgi
import sqlite3
from string import Template

OPTION_PASSENGER = "<option value=\"$name\">$name</option>"
OPTION_ROUTE = "<option value=\"$route\">$route</option>"

class Passenger:
    def __init__(self, name, from_city, to_city):
        self._name = name
        self._from_city = from_city
        self._to_city = to_city
    def route_cost(self, routes, rate):
        for r in routes:
            if r[0] == self._from_city and r[1] == self._to_city:
                return rate * r[2]
        return None
    def get_route(self):
        return self._from_city, self._to_city
    def change_route(self, new_from, new_to):
        self._from_city = new_from
        self._to_city = new_to

class RouteCost:
    def __init__(self, routes_data, rate):
        self._routes_data = routes_data
        self._rate = rate
        self._update_routes()

    def _update_routes(self):
        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""SELECT "from", "to", "distance" FROM "routes" """)
        l = curs.fetchall()
        self._routes = [(str(e[0]), str(e[1]), float(e[2])) for e in l if str(e[0]) != "none" and str(e[1]) != "none"]

        conn.close()

    def _get_passenger_names(self):
        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""SELECT "name" FROM "passengers" """)
        l = curs.fetchall()
        conn.close()

        return [str(e[0]) for e in l]

    def _load_passenger(self, name): 
        name = str(name)

        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""SELECT "route_id" FROM "passengers" WHERE "name" = ?""", (name,))
        id = int(curs.fetchone()[0])
        curs.execute("""SELECT "from", "to" FROM "routes" WHERE "route_id" = ?""", (id,))
        from_city, to_city = (str(e) for e in curs.fetchone())

        conn.close()
        return Passenger(name, from_city, to_city)

    def _redact_passenger(self, name, new_name, new_from, new_to):
        name = str(name)
        new_name = str(new_name)
        new_from = str(new_from)
        new_to = str(new_to)

        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""SELECT "route_id" FROM "routes" WHERE "from" = ? AND "to" = ?""", (new_from, new_to))
        id = curs.fetchone()
        if id == None:
            id = -1
        else:
            id = int(id[0])
            
        curs.execute("""UPDATE "passengers" SET "name" = ?, "route_id" = ? WHERE "name" = ?""", (new_name, id, name))

        conn.commit()
        conn.close()

    def _add_passenger(self, name, from_city, to_city):
        name = str(name)
        from_city = str(from_city)
        to_city = str(to_city)

        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""SELECT "route_id" FROM "routes" WHERE "from" = ? AND "to" = ?""", (from_city, to_city))
        id = curs.fetchone()
        if id == None:
            id = -1
        else:
            id = int(id[0])
        curs.execute("""INSERT INTO "passengers" ("name", "route_id") VALUES (?, ?)""", (name, id))

        conn.commit()
        conn.close()

    def _delete_passenger(self, name):
        name = str(name)

        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""DELETE FROM "passengers" WHERE "name" = ?""", (name,))

        conn.commit()
        conn.close()

    def _add_route(self, from_city, to_city, dist):
        from_city = str(from_city)
        to_city = str(to_city)
        dist = float(dist)

        conn = sqlite3.connect(self._routes_data)
        curs = conn.cursor()

        curs.execute("""INSERT INTO "routes" ("from", "to", "distance") VALUES (?, ?, ?)""", (from_city, to_city, dist))

        conn.commit()
        conn.close()
        self._update_routes()

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "").lstrip("/")
        params = {"result": "", "passengers" : "", "routes" : "", "cost" : ""}
        status = "200 OK"
        headers = [("Content-Type", "text/html; charset=utf-8")]

        if path == "":
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            name = form.getfirst("passengers", "").split("\n")[0].replace("\r", "")
            route = form.getfirst("routes", "")
            route = route.split()
            change_route = form.getfirst("change_route", "")
            if len(route) > 1:
                if change_route:
                    self._change_passenger_route(name, route[0], route[-1])
                passenger = self._load_passenger(name)
                cost = passenger.route_cost(self._routes, self._rate)
                if cost != None:
                    params["cost"] = "Поточний маршрут: {}, вартість: {}".format(passenger._from_city + " - " + passenger._to_city, cost)
                else:
                    params["cost"] = "Пасажир не має зареєстрованого маршруту"

            names = self._get_passenger_names()
            for n in names:
                from_city, to_city = self._load_passenger(n).get_route()
                params["passengers"] += Template(OPTION_PASSENGER).substitute(name = n + "\n(маршрут:{} - {})".format(from_city, to_city))
            for r in self._routes:
                rc = r[0] + " - " + r[1]
                params["routes"] += Template(OPTION_ROUTE).substitute(route = rc)

            html = "templates/routes.html"

        elif path == "add_route":
            html = "templates/add_route.html"
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            from_city = form.getfirst("from", "")
            to_city = form.getfirst("to", "")
            dist = form.getfirst("dist", "")

            if from_city and to_city:
                self._add_route(from_city, to_city, dist)
                params["result"] = "Маршрут додано!"
            else:
                params["result"] = ""

        elif path == "add_passenger":
            html = "templates/add_passenger.html"
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            passenger = form.getfirst("passengers", "").split("\n")[0].replace("\r", "")
            name = form.getfirst("name", "")
            from_city = form.getfirst("from", "")
            to_city = form.getfirst("to", "")
            delete_passenger = form.getfirst("delete_passenger", "")

            if not passenger:
                params["result"] = ""
            elif passenger == "-----додати-----":
                if name:
                    if not from_city or not to_city:
                        from_city = "0"
                        to_city = "0"
                    self._add_passenger(name, from_city, to_city)
                    params["result"] = "Пасажир доданий!"
                else:
                    params["result"] = ""
            else:
                if delete_passenger:
                    self._delete_passenger(passenger)
                    params["result"] = "Пасажир видалений!"
                else:
                    if not from_city or not to_city:
                        from_city = "0"
                        to_city = "0"
                    if not name:
                        name = passenger
                    self._redact_passenger(passenger, name, from_city, to_city)
                    params["result"] = "Зміни внесено!"

            params["passengers"] += Template(OPTION_PASSENGER).substitute(name="-----додати-----")
            names = self._get_passenger_names()
            for n in names:
                from_city, to_city = self._load_passenger(n).get_route()
                params["passengers"] += Template(OPTION_PASSENGER).substitute(name = n + "\n(маршрут:{} - {})".format(from_city, to_city))
            for r in self._routes:
                rc = r[0] + " - " + r[1]
                params["routes"] += Template(OPTION_ROUTE).substitute(route=rc)
            
        else:
            status = "404 NOT FOUND"
            html = "templates/error_404.html"

        start_response(status, headers)
        with open(html, encoding="utf-8") as f:
            page = Template(f.read()).substitute(params)
        return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == '__main__':
    app = RouteCost("data/routes.db", 10)
    from wsgiref.simple_server import make_server
    make_server(HOST, PORT, app).serve_forever()