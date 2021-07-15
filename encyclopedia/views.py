from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from random import randint
import markdown2

from encyclopedia import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, wiki):
    entry = util.get_entry(wiki)
    if entry == None:
        return HttpResponseNotFound("<h1>Entry not found</h1>")
    else:
        return render(request, "encyclopedia/wiki.html", {
            "wiki": wiki,
            "entry": markdown(entry)
        })


def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        return redirect('wiki', wiki=query)
    elif query not in entries:
        a = []
        for entry in entries:
            if query.lower() in entry.lower():
                a.append(entry)
        if a == None:
            return HttpResponseNotFound("<h1>Query not found</h1>")
        else:
            return render(request, "encyclopedia/search.html", {
                "search": query,
                "results": a
                })
    else:
        return HttpResponseNotFound("<h1>Query not found</h1>")


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in util.list_entries():
            return HttpResponseNotFound("<h1>Entry already exists</h1>")
        else:
            util.save_entry(title, content)
            return redirect(wiki, title)


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                    "title": title,
                    "content": content
                    })
    if request.method == "POST":
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        util.save_entry(new_title, new_content)
        return redirect(wiki, new_title)


def random_page(request):
    entries = util.list_entries()
    num = (len(entries) - 1)
    rand = randint(0 ,num)
    rand_entry = entries[rand]
    entry = util.get_entry(rand_entry)
    return render(request, "encyclopedia/wiki.html", {
            "wiki": rand_entry,
            "entry": markdown(entry)
        })

def markdown(markdown):
    converted = markdown2.markdown(markdown)
    return converted