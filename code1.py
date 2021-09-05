import urllib.request, urllib.error, urllib.parse
import ply.lex as lex
import ply.yacc as yacc
import re
import os
import sys




def genrate_url(url , genre):
    gdict = {"action adventure":"_action__adventure_movies" , 
                "animation":"_animation_movies" , 
                "comedy":"_comedy_movies" , 
                "mystery suspense":"_mystery__suspense_movies",
                "horror" : "_horror_movies",
                "science fiction":"_science_fiction__fantasy_movies",
                "documentary":"_documentary_movies",
                "romance" : "_romance_movies",
                "classics" : "_classics_movies"
                }
    return url+gdict[genre]

def download_page(url):
    url = "https://www.rottentomatoes.com" + url
    print(url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f = open('moviefile.html' , 'wb')
    f.write(webContent)
    f.close()

def main():
    url = "https://www.rottentomatoes.com/top/bestofrt/top_100"
    genre = input('Select a Genre:')
    url = genrate_url(url , genre)
    print(url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    #webContent = str(webContent)

    html = webContent.decode('utf-8')
    html = html.split("\n")

    start = 0
    stop = 0

    for i in range(len(html)):
        line = html[i]
        if line.find('<div class=\"subtle pull-right sortText\">') >=0:
            start = i

        if line.find('<div class=\"col-right hidden-xs\">') >=0:
            stop = i



    html = html[start : stop]
    indices = []

    for i in range(len(html)):
        line = html[i]
        if line.find("<a href") >=0:
            indices.append(i)

    MovieList = []
    MovieURLList = []
    for i in indices:
        url = html[i].replace("<a href=" , "").replace("class=\"unstyled articleLink\"" , "").replace("\"" , "").replace(">" , "").strip()
        MovieURLList.append(url)
        MovieList.append(html[i+1].replace("</a>" , "").strip())

    i=1
    for m in range(len(MovieList)):
        print(str(i) + ". " + MovieList[m])
        i += 1


    movie = input("Select the movie:")
    if movie in MovieList:

        url = "https://www.rottentomatoes.com" + MovieURLList[MovieList.index(movie)]
        print(url)
        response = urllib.request.urlopen(url)
        webContent = response.read()
        f = open('moviefile.html' , 'wb')
        f.write(webContent)
        f.close()


if __name__ == '__main__':
	main()