#20CS60R56
#VINEETH KUMAR BALAPANURU
# IMPLEMENTED BOTH TASK1 AND TASK2 IN THIS PROGRAM ITSELF

import urllib.request, urllib.error, urllib.parse
import ply.lex as lex
import ply.yacc as yacc
import re
import os
import sys

tokens = (
            'MOVIENAMEATTR' , 'MOVIENAME' ,
            'MOVIEDESCRIPATTR' , 'MOVIEDESCRIP' ,
            'DIRECTORATTR' , 'PRODUCERATTR' , 'WRITERATTR'  ,
            'OGLANGATTR' , 'OGLANG',
            'CASTATTR' , 'CAST' , 'ROLE'  , 'CASTREF',
            'BOXOFFICEATTR' , 'BOXOFFICE' ,
            'RUNTIMEATTR' , 'RUNTIME' ,
            'GENREATTR' , 'GENRE' ,
             'SIMMOVIEATTR','SIMMOVIE' , 'SIMMOVIEREF' ,
             'BDAYATTR' , 'BDAY' , 'HRATEDATTR' , 'LRATEDATTR' ,
             'MOVIE' , 'MLISTATTR' , 'MLIST' ,
             'WHERETOATTR' , 'WHERETO' ,
            'CELEBRITY' , 'END'
    )


# Ignored characters
t_ignore = "\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    t.lexer.skip(1)

#------------------------- MOVIE NAME LEXICONS ----------------------------------
def t_MOVIENAMEATTR(t):
    r'<meta\ name="viewport"\ content="width=device-width,\ initial-scale=1">'
    t.value = 'name'
    return t


def  t_MOVIENAME(t):
    r'<title>([^<]*)'
    t.value = (t.value)[7:-18]
    return t

#------------------------- MOVIE DESCRIPTION LEXICONS ----------------------------------

# MOVIEDESCRIP START IS SAME AS MOVIENAMEEND

def t_MOVIEDESCRIPATTR(t):
    r'</title>'
    t.value = 'story'
    return t

def t_MOVIEDESCRIP(t):
    r'<meta\ name="description"\ content=([^>]*)'
    t.value = (t.value)[34:-1]
    return t
#------------------------- ORIGINAL LANGUAGE DESCRIPTION LEXICONS ----------------------------------
def t_OGLANGATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Original\ Language:</div>'
    t.value = 'language'
    return t

def t_OGLANG(t):
    r'<div\ class="meta-value"\ data-qa="movie-info-item-value">[A-Za-z][A-Za-z]([A-Za-z\s\(\)]+)\n'
    s = (t.value).find('>')
    t.value = (t.value)[s+1:-1]
    return t
#------------------------- DIRECTOR DESCRIPTION LEXICONS ----------------------------------

def t_DIRECTORATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Director:</div>'
    t.value = 'director'
    return t


#DIRECTOREND IS SAME AS PRODUCERSTART

#------------------------- PRODUCER DESCRIPTION LEXICONS ----------------------------------

def t_PRODUCERATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Producer:</div>'
    t.value = 'producer'
    return t

#PRODUCEREND IS SAME AS WRITERSTART

#------------------------- WRITER DESCRIPTION LEXICONS ----------------------------------

def t_WRITERATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Writer:</div>'
    t.value = 'writer'
    return t

#------------------------- CAST & CREW DESCRIPTION LEXICONS ----------------------------------

def t_CASTATTR(t):
    r'<h2\ class="panel-heading"\ data-qa="cast-crew-section-title">Cast\ &amp;\ Crew</h2>'
    t.value = 'cast'
    return t

def t_CASTREF(t):
    r'<a\ href="([A-Za-z0-9_/-]+)"\ data-qa="cast-crew-item-img-link">'
    t.value = (t.value).replace('<a href="' , '').replace('" data-qa="cast-crew-item-img-link">' , '' )
    return t

def t_CAST(t):
    r'<span\ class="characters\ subtle\ smaller"\ title="([^>]+)'
    t.value = (t.value).replace('<span class="characters subtle smaller" title="' , '').replace('"' , '')
    return t

def t_ROLE(t):
    r'<br/>([\n\s]+)([A-Za-z\(\)\s-]+)([\s\n]+)((<br/>)*)([\s\n]*)</span>([\s\n]+)</div>([\s\n]*)</div>'
    t.value = t.value.replace('\n' , "").replace(" " , "").replace('<br/>' , "").replace('</div>' , "").replace('</span>' , "")
    return t

#------------------------- BOX OFFICE LEXICONS ----------------------------------
def t_BOXOFFICEATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Box\ Office\ \(Gross\ USA\):</div>'
    t.value = 'boxoffice'
    return t

def t_BOXOFFICE(t):
    r'<div\ class="meta-value"\ data-qa="movie-info-item-value">\$([0-9,.]+)([KMB]*)</div>'
    t.value = (t.value)[56:-6]
    return t
#------------------------- RUNTIME LEXICONS ----------------------------------
def t_RUNTIMEATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Runtime:</div>'
    t.value = 'runtime'
    return t

def t_RUNTIME(t):
    r'<time\ datetime="([A-Za-z0-9\s]+)">\n(\s+)([A-Za-z0-9\s]+)'
    x = t.value.split('\n')
    t.value = x[1].strip()
    return t

#------------------------- GENRE LEXICONS ----------------------------------
def t_GENREATTR(t):
    r'<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Genre:</div>'
    t.value = 'genre'
    return t

def t_GENRE(t):
    r'<div\ class="meta-value\ genre"\ data-qa="movie-info-item-value">([A-Za-z,\n\s]+)</div>'
    t.value = (t.value)[63:-7].replace(' ' , '').replace('\n' , '')
    return t

#-------------------------CELEB LEXICONS---------------------------------------
def t_BDAYATTR(t):
    r'<p\ class="celebrity-bio__item"\ data-qa="celebrity-bio-bday">'
    t.value = 'bday'
    return t

def t_BDAY(t):
    r'Birthday:\n(\s+)([A-Za-z0-9,\s]+)'
    t.value = t.value.replace('Birthday:\n' , '').strip()
    return t

def t_HRATEDATTR(t):
    r'Highest\ Rated:'
    t.value = 'hrated'
    return t

def t_LRATEDATTR(t):
    r'Lowest\ Rated:'
    t.value = 'lrated'
    return t

def t_MOVIE(t):
    r'<a\ class="celebrity-bio__link"\ href="([A-Za-z0-9_/-]+)">\n(\s+)([A-Za-z0-9\(\)\s,.-]+)\n(\s+)</a>'
    idx = t.value.find('>')
    t.value = (t.value)[idx+1 : -4].strip()
    return t

def t_MLISTATTR(t):
    r'<h2\ class="celebrity-filmography__h2"\ data-qa="celebrity-filmography-header">Filmography</h2>'
    t.value = 'mlist'
    return t

def t_MLIST(t):
    r'<tr\n(\s+)data-title="([A-Za-z0-9\(\).,\s/-]+)"\n(\s+)data-boxoffice="([0-9]+)"\n(\s+)data-year="([0-9]+)"'
    return t
#------------------------- MISC LEXICONS ----------------------------------
def t_CELEBRITY(t):
    r'<a\ href="/celebrity/([^<\n]+)</a>'
    s = (t.value).find('>')
    t.value = (t.value)[s+1:-4]
    return t

def t_SIMMOVIEATTR(t):
    r'<h2\ class="panel-heading\ recommendations-panel__heading-title">You\ might\ also\ like</h2>'
    t.value = 'ymal'
    return t

def t_SIMMOVIEREF(t):
    r'<a\ href="/m/([A-Za-z0-9_-]+)"\ class="recommendations-panel__poster-link">'
    t.value = (t.value)[9:-45]
    return t

def t_SIMMOVIE(t):
    r'<span\ slot="title"\ class="recommendations-panel__poster-title">([A-Za-z0-9,\(\)\s:\'".-]+)</span>'
    t.value = (t.value)[63:-7]
    return t


def t_WHERETOATTR(t):
    r'<h2\ class="\ panel-heading\ where-to-watch__header"\ data-qa="where-to-watch-header">Where\ to\ watch</h2>'
    t.value = 'wheretowatch'
    return t

def t_WHERETO(t):
    r'data-affiliate="([A-Za-z-]+)"'
    t.value = (t.value)[16:-1].replace('-' , ' ')
    return t

def t_END(t):
    r'</html>'
    t.value = 'end'
    return t

#--------------------------------GRAMMAR PRODUCTIONS -------------------------------

def p_start(p):
    '''start : pair start
             | END
             '''

def p_pair(p):
    '''pair : attribute value'''

    attr.append(p[1])
    attrval.append(p[2])

def p_attribute(p):
    '''attribute : WRITERATTR
                 | DIRECTORATTR
                 | PRODUCERATTR
                 | MOVIENAMEATTR
                 | MOVIEDESCRIPATTR
                 | RUNTIMEATTR
                 | BOXOFFICEATTR
                 | CASTATTR
                 | OGLANGATTR
                 | GENREATTR
                 | SIMMOVIEATTR
                 | HRATEDATTR
                 | LRATEDATTR
                 | BDAYATTR
                 | MLISTATTR
                 | WHERETOATTR
                 '''
    p[0] = p[1]

def p_value(p):
    '''value : celeb
             | castnchar
             | val
             | refnmovie
             | mlistrec
             | where
             '''
    p[0] = p[1]

def p_castnchar(p):
    '''castnchar : castnchar CASTREF CAST ROLE
                 | castnchar CAST ROLE
                 | CAST ROLE
                 | CASTREF CAST ROLE
                 '''
    if len(p) > 4:
        p[0] = p[1] + [(p[2] , p[3] , p[4])]
    elif len(p) > 3 and type(p[1]) == str:
        p[0] = [(p[1] , p[2] , p[3])]
    elif len(p) > 3:
        p[0] = p[1] + [('' , p[2] , p[3])]
    else:
        p[0] = [('' , p[1] , p[2])]

def p_celeb(p):
    '''celeb : celeb CELEBRITY
             | CELEBRITY
             '''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_val(p):
    '''val : MOVIENAME
           | MOVIEDESCRIP
           | OGLANG
           | BOXOFFICE
           | RUNTIME
           | GENRE
           | MOVIE
           | BDAY CELEBRITY
           '''
    p[0] = p[1]

def p_where(p):
    '''where : where WHERETO
             | WHERETO
             '''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_refnmovie(p):
    '''refnmovie : refnmovie SIMMOVIEREF SIMMOVIE
                 | SIMMOVIEREF SIMMOVIE
                 '''
    if len(p) == 4:
        p[0] = p[1] + [(p[2] , p[3])]
    else:
        p[0] = [(p[1] , p[2])]

def p_mlistrec(p):
    '''mlistrec : mlistrec MLIST
                | MLIST
                '''
    if len(p) > 2:
        lst = []
        sidx = p[2].find('data-title')
        eidx = p[2].find('data-boxoffice')
        lst.append(p[2][sidx+12 : eidx-2].replace('\n' , '').strip())
        sidx = p[2].find('data-year')
        lst.append(p[2][sidx+11:-1])
        p[0] = p[1] + [lst]

    else:
        lst = []
        sidx = p[1].find('data-title')
        eidx = p[1].find('data-boxoffice')
        lst.append(p[1][sidx+12 : eidx-1].replace('\n' , '').strip())
        sidx = p[1].find('data-year')
        lst.append(p[1][sidx+11:-1])
        p[0] = [lst]

def p_error(p):
    pass
#--------------------------------RUNNING THE PARSER-----------------------------------


def download_page(url , fname):
    url = "https://www.rottentomatoes.com" + url
    print(url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f = open(fname , 'wb')
    f.write(webContent)
    f.close()
    return fname


def main():
    global attr , attrval
    attr = []
    attrval = []
    Queries = {'you might also like':'ymal' ,
                'where to watch':'wheretowatch' ,
                'birthday':'bday' ,
                'highest rated movie':'hrated' ,
                'lowest rated movie':'lrated' ,
                'story' : 'story' ,
                'name' : 'name' ,
                'language':'language' ,
                'genre':'genre' ,
                'box office':'boxoffice' ,
                'runtime' : 'runtime' ,
                'cast' : 'cast' ,
                'director' : 'director' ,
                'writer' : 'writer' ,
                'producer' : 'producer' ,
                'other movies' : 'othermovies' ,
                'quit' : 'quit'
                }
    #result = {'name' , 'story' , 'writer' , 'director' , 'producer' , 'runtime' , 'boxoffice' , 'cast' , 'language'}
    fp = open("moviefile.html")
    data = fp.read()
    lexer = lex.lex()
    parser = yacc.yacc()
    parser.parse(data)
    os.remove('moviefile.html')

   # for i in range(len(attr)):
    #    print(attr[i] , attrval[i])


    exit = False
    while not exit:
        query = input("What details you want:")
        try:
            query = Queries[query]
        except:
            print('Requested Query not available!')
            continue

        if query.lower() == 'quit':
            exit = True
        elif query.lower() == 'ymal':
            try:
                idx = attr.index('ymal')
                mlist = []
                for i in range(len(attrval[idx])):
                    print(str(i+1) + '. ' + attrval[idx][i][1])
                    mlist.append(attrval[idx][i][1])
                quer = input('Enter a movie name:')
                try:
                    midx = mlist.index(quer)
                    url = attrval[idx][midx][0]
                    fp = open(download_page(url , 'moviefile.html'))
                    attr = []
                    attrval = []
                    data = fp.read()
                    lexer = lex.lex()
                    parser = yacc.yacc()
                    parser.parse(data)
                    os.remove('moviefile.html')
                except:
                    print('Movie not available')
            except:
                print('Not Available!')

        elif query.lower() == 'cast':
            idx = attr.index('cast')
            clist = []
            for i in range(len(attrval[idx])):
                print(str(i+1) + '. ' + attrval[idx][i][1])
                clist.append(attrval[idx][i][1])
            quer = input('know about which cast member:')
            cidx = clist.index(quer)
            if cidx == -1:
                print('No cast member present with given name')
            else:
                url = attrval[idx][cidx][0]
                download_page(url , 'castfile.html')
                data = open('castfile.html').read()
                attr = []
                attrval = []
                lexer = lex.lex()
                parser = yacc.yacc()
                parser.parse(data)
                os.remove('castfile.html')

                #for i in range(len(attr)):
                    #print(attr[i] , attrval[i])


                cexit = False

                while not cexit:
                    quer = input('What is the query?')

                    try:
                        quer = Queries[quer]
                    except:
                        print('Requested Query not available!')
                        continue

                    if quer == 'othermovies':
                        year = input('year?')
                        i=1
                        year = int(year)
                        midx = attr.index('mlist')
                        for movie in attrval[midx]:
                            if int(movie[1]) >= year:
                                i += 1
                                print(str(i)+'. '+movie[0])

                    elif quer == 'quit':
                        cexit = True
                        exit = True

                    else:
                        try:
                            idx = attr.index(quer)
                            print(attr[idx] + ' ' + attrval[idx])
                        except:
                            print('Not available')


        elif query.lower() in attr:
            try:
                idx = attr.index(query)
                print(query + ':' , attrval[idx])
            except:
                print(query + ' information is not available')

if __name__ == '__main__':
	main()
