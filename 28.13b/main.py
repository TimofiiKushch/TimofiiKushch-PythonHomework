import cgi
import xml.etree.ElementTree as et
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
    def change_route(self, new_from, new_to):
        self._from_city = new_from
        self._to_city = new_to

class RouteCost:
    def __init__(self, passengers_data, routes_data, rate):
        self._passengers_data = passengers_data
        self._routes_data = routes_data
        self._rate = rate
        self._update_routes()

    def _update_routes(self):
        etree = et.parse(self._routes_data)
        self._routes = [[r.find("from").text, r.find("to").text, float(r.find("dist").text)] for r in etree.iter("route")]

    def _get_passenger_names(self):
        etree = et.parse(self._passengers_data)
        return [p.get("name") for p in etree.iter("passenger")]

    def _load_passenger(self, name): 
        etree = et.parse(self._passengers_data)
        for p in etree.iter("passenger"):
            if p.get("name") == name:
                return Passenger(name, p.find("from").text, p.find("to").text)

    def _change_passenger_route(self, name, new_from, new_to):
        etree = et.parse(self._passengers_data)
        for p in etree.iter("passenger"):
            if p.get("name") == name:
                p.find("from").text = new_from
                p.find("to").text = new_to
        etree.write(self._passengers_data, encoding = "utf-8", xml_declaration = True)

    def _add_passenger(self, name, from_city, to_city):
        etree = et.parse(self._passengers_data)

        p = et.Element("passenger")
        p.set("name", name)
        f = et.Element("from")
        f.text = from_city
        t = et.Element("to")
        t.text = to_city
        p.append(f)
        p.append(t)
        
        etree.getroot().append(p)
        etree.write(self._passengers_data, encoding = "utf-8", xml_declaration = True)

    def _add_route(self, from_city, to_city, dist):
        etree = et.parse(self._routes_data)

        r = et.Element("route")

        f = et.Element("from")
        f.text = from_city
        t = et.Element("to")
        t.text = to_city
        d = et.Element("dist")
        d.text = str(dist)
        r.append(f)
        r.append(t)
        r.append(d)
        
        etree.getroot().append(r)
        etree.write(self._routes_data, encoding = "utf-8", xml_declaration = True)
        self._update_routes()

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "").lstrip("/")
        params = {"result": "", "passengers" : "", "routes" : "", "cost" : ""}
        status = "200 OK"
        headers = [("Content-Type", "text/html; charset=utf-8")]

        if path == "":
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            name = form.getfirst("passengers", "")
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
                params["passengers"] += Template(OPTION_PASSENGER).substitute(name=n)
            for r in self._routes:
                rc = r[0] + " - " + r[1]
                params["routes"] += Template(OPTION_ROUTE).substitute(route=rc)

            html = "templates/routes.html"

            params["result"] += "Список маршрутів:<br>"
            etree = et.parse(self._routes_data)
            xml_str = et.tostring(etree.getroot()).decode("utf-8")
            xml_str = xml_str.replace("<routes>", "<routes>\n")
            xml_str = xml_str.replace("<route>", "<route>\n")
            xml_str = xml_str.replace("</route>", "</route>\n")
            xml_str = xml_str.replace("</from>", "</from>\n")
            xml_str = xml_str.replace("</to>", "</to>\n")
            xml_str = xml_str.replace("</dist>", "</dist>\n")
            params["result"] += ((xml_str.replace("<", "&#60 ")).replace(">", "&#62 ")).replace("\n", "<br>")

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
            name = form.getfirst("name", "")
            from_city = form.getfirst("from", "")
            to_city = form.getfirst("to", "")

            if name:
                if not from_city or not to_city:
                    from_city = "0"
                    to_city = "0"
                self._add_passenger(name, from_city, to_city)
                params["result"] = "Пасажир доданий!"
            else:
                params["result"] = ""

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
    app = RouteCost("data/passengers.xml", "data/routes.xml", 10)
    from wsgiref.simple_server import make_server
    make_server(HOST, PORT, app).serve_forever()