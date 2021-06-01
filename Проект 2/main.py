import cgi
import sqlite3
import docx
import time
from string import Template

class Storage:
    def __init__(self, storage_data):
        self._storage_data = storage_data

    def _search_by_category(self, category):
        category = str(category)

        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        curs.execute("""SELECT "wares" FROM "shipments" WHERE "category" = ?""", (category,))
        l = curs.fetchall()
        conn.close()

        return set([e[0] for e in l])

    def _search_by_name_part(self, pattern): 
        pattern = str(pattern)

        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        curs.execute("""SELECT "wares" FROM "shipments" WHERE instr("wares", ?) > 0 COLLATE NOCASE""", (pattern,))
        l = curs.fetchall()
        conn.close()

        return set([e[0] for e in l])

    def _get_remainder(self, wares):
        wares = str(wares)

        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        curs.execute("""SELECT "mass" FROM "shipments" WHERE "wares" = ?""", (wares,))
        l = curs.fetchall()
        conn.close()

        return [e[0] for e in l]

    def _get_wares_info(self, wares):
        wares = str(wares)

        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        curs.execute("""SELECT "mass", "shipment_id" FROM "shipments" WHERE "wares" = ?""", (wares,))
        l = curs.fetchall()

        res = []
        for e in l:
            curs.execute("""SELECT "building", "section", "shelf" FROM "addresses" WHERE "shipment_id" = ?""", (e[1],))
            p = curs.fetchone()
            res.append((e[0], e[1], "корпус {}, відділення {}, полиця {}".format(p[0], p[1], p[2])))
        conn.close()
        return res

    def _add_shipment(self, wares, category, mass, building, section, shelf):
        wares = str(wares)
        category = str(category)
        mass = float(mass)
        building = int(building)
        section = int(section)
        shelf = int(shelf)

        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        curs.execute("""SELECT "shipment_id" FROM "addresses" WHERE "building" = ? AND "section" = ? AND "shelf" = ?""", (building, section, shelf))
        if curs.fetchone() == None:
            curs.execute("""INSERT INTO "shipments" ("wares", "category", "mass") VALUES (?, ?, ?)""", (wares, category, mass))
            id = curs.lastrowid
            curs.execute("""INSERT INTO "addresses" ("building", "section", "shelf", "shipment_id") VALUES (?, ?, ?, ?)""", (building, section, shelf, id))

            conn.commit()
            conn.close()

            return "Партію додано!"
        else:
            return "Дане місце на складі заняте!"

    def _remove_shipment(self, id_list):
        conn = sqlite3.connect(self._storage_data)
        curs = conn.cursor()

        description = ""
        i = 0

        for id in id_list:
            id = int(id)
            curs.execute("""SELECT "building", "section", "shelf" FROM "addresses" WHERE "shipment_id" = ?""", (id,))
            place = curs.fetchone()
            if place != None:
                curs.execute("""SELECT "wares", "mass" FROM "shipments" WHERE "shipment_id" = ?""", (id,))
                (wares, mass) = curs.fetchone()
                curs.execute("""DELETE FROM "addresses" WHERE "shipment_id" = ?""", (id,))
                curs.execute("""DELETE FROM "shipments" WHERE "shipment_id" = ?""", (id,))
                conn.commit()

                description += "партію товару \"{}\" масою {} видано з корпусу {}, відділення {}, полиці {};$end$".format(wares, round(mass, 3), place[0], place[1], place[2])
                i += 1

        conn.close()

        return (description, i)

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "").lstrip("/")
        params = {"result": ""}
        status = "200 OK"
        headers = [("Content-Type", "text/html; charset=utf-8")]

        if path == "":
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            input = form.getfirst("search_bar", "")
            action = form.getfirst("action", "")

            if action == "category":
                l = self._search_by_category(input)
                if len(l) > 0:
                    params["result"] += "Список товарів категорії \"{}\":<br>".format(input)
                    for w in l:
                        params["result"] += "{}<br>".format(w)
                else:
                    params["result"] += "Товарів категорії \"{}\" не знайдено!".format(input)
            elif action == "pattern":
                l = self._search_by_name_part(input)
                if len(l) > 0:
                    params["result"] += "Товари з частиною \"{}\" в найменуванні:<br>".format(input)
                    for w in l:
                        params["result"] += "{}<br>".format(w)
                else:
                    params["result"] += "Товарів з частиною \"{}\" в найменуванні не знайдено!".format(input)
            elif action == "remainder":
                l = self._get_remainder(input)
                params["result"] += "Залишок товару \"{}\":<br>".format(input)
                if len(l) == 0:
                    params["result"] += "Даного товару немає на складі!"
                elif len(l) <= 5:
                    params["result"] += "Знайдено {} партій масою ".format(len(l))
                    for f in l:
                        params["result"] += str(round(f, 3)) + "; "
                else:
                    params["result"] += "Знайдено {} партій загальною масою {}; мінімальна {}; максимальна {}".format(len(l), round(sum(l), 3), round(min(l), 3), round(max(l), 3))
            elif action == "place":
                l = self._get_wares_info(input)
                if len(l) > 0:
                    params["result"] += "Знайдено {} партій:<br>".format(len(l))
                    for e in l:
                        params["result"] += "партія з номером {}, масою {} та розташуванням {}<br>".format(e[1], round(e[0], 3), e[2])
                else:
                    params["result"] += "Даного товару немає на складі!"

            html = "templates/wares.html"

        elif path == "add_shipment":
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            wares = form.getfirst("wares", "")
            category = form.getfirst("category", "")
            mass = form.getfirst("mass", "")
            building = form.getfirst("building", "")
            section = form.getfirst("section", "")
            shelf = form.getfirst("shelf", "")
            if wares and category and mass and building and section and shelf:
                params["result"] = self._add_shipment(wares, category, mass, building, section, shelf)
            html = "templates/add_shipment.html"

        elif path == "remove_shipment":
            form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
            l = form.getfirst("id_list", "").replace("_", "").split()
            if len(l) > 0:
                good = True
                for e in l:
                    try:
                        int(e)
                        if "." in e:
                            good = False
                            break
                    except ValueError:
                        good = False
                        break
                if good:
                    res = self._remove_shipment(l)
                    if res[1] == 0:
                        params["result"] += "Партій з даними номерами немає на складі!"
                    else:
                        params["result"] += "Загальна кількість виданих партій: {}<br>".format(res[1]) + res[0].replace("$end$", "<br>")
                        doc = docx.Document("data/note.docx")
                        t = time.localtime(time.time())
                        DATE = str(t.tm_mday) + "." + str(t.tm_mon) + "." + str(t.tm_year)
                        COUNT = str(res[1])
                        RESULT = res[0].replace("$end$", "\n")
                        for p in doc.paragraphs:
                            for r in p.runs:
                                r.text = r.text.replace("$date$", DATE)
                                r.text = r.text.replace("$count$", COUNT)
                                r.text = r.text.replace("$result$", RESULT)
                        doc.save("data/Накладна ({}).docx".format(time.asctime(t).replace(":", "-")))
                else:
                    params["result"] += "Будь ласка, введіть цілі значення номерів через пропуск!"

            html = "templates/remove_shipment.html"
            
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
    app = Storage("data/storage.db")
    from wsgiref.simple_server import make_server
    make_server(HOST, PORT, app).serve_forever()