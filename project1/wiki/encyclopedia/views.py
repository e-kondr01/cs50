import markdown2

from django.shortcuts import render, redirect
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_entry(request, title):
    f = util.get_entry(title)
    if not f:
        f = util.get_error('PageNotFound')
    text = markdown2.markdown(f)
    return render(request, "encyclopedia/wiki_entry.html", {
        "title": title,
        'text': text,
    })


def random(request):
    entries = util.list_entries()
    i = randint(0, len(entries) - 1)
    title = entries[i]

    return redirect(f'/wiki/{title}')


def search(request):
    q = request.GET.get('q', '')
    q.lower()
    entries = util.list_entries()
    formatted_entries = []
    no_res = False
    for entry in entries:
        formatted_entries.append(entry.lower())
    if q in formatted_entries:
        return redirect(f'/wiki/{q}')
    else:
        search_res = []
        for i in range(len(formatted_entries)):
            if q in formatted_entries[i]:
                search_res.append(entries[i])
        if not search_res:
            no_res = True

        return render(request, "encyclopedia/search.html", {
            "entries": search_res,
            "q": q,
            'no_res': no_res,
        })


def new_page(request):
    pass


def create_page(request):
    pass
