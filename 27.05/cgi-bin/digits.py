import cgi
from string import Template

def sep_digits(string):
    d, o = "", ""
    for char in string:
        if char.isdigit():
            d += char
        else:
            o += char
    return d, o

if __name__ == '__main__':
    form = cgi.FieldStorage()
    d, o = sep_digits(form.getfirst("string", ""))
    d = "Цифри: " + d
    o = "Не цифри: " + o

    with open("result.html", encoding = "utf-8") as f:
        page = Template(f.read()).substitute(digits = d, nondigits = o)

    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

    print("Content-type: text/html charset=utf-8\n")
    print(page)