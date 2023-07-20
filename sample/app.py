import json

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/temp")
def temp():
    return render_template('temp.html')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/localplayer")
def local():
    return render_template('localplayer.html')

@app.route('/upcoming')
def upcoming():
    return render_template('upcoming.html')

@app.route("/about")
def about():
    about='black'
    return render_template('about.html',about=about)


@app.route("/gen", methods=['POST'])
def generate():
    if request.method == "POST":

        width=str(request.form.get('width'))
        height=str(request.form.get('height'))
        url=str(request.form.get('link'))
        fstyle=str(request.form.get("fstyle"))
        # print(url)


        poster=str(request.form.get('poster'))
        print(poster)
        time="true"
        progress="true"
        muteb="true"
        fullscb="true"

        style="light"
        playb="true"
        tclass=""

        gifmode=str(request.form.get("gifmode"))
        overlay='true'
        autopause='true'
        muted='false'
        autoplay='false'
        loop='false'
        if gifmode=='true':
            autopause='false'
            muted='true'
            autoplay="true"
            loop="true"
            time = 'false'
            progress = 'false'
            muteb='false'
            fullscb='false'
            playb='false'
            overlay='false'
        else:
            autopause='true'
            muted='false'
            autoplay="false"
            loop="false"




        # fstyle=False
        if width=='None':
            width='100%'
        if height=='None':
            height='100%'



        strstyle='style="position: absolute; height:'+height+ '; width: '+width+ '; left: 0px; top: 0px; background-color: #000000;"'
        tclass='class="rounded-xl"'

        # else:
        #     strstyle='style="background-color: #000000;"'
        #     tclass='class="rounded-xl "'
        #     # mt - 2
            # mb - 2


        iframe='"<iframe id="fra" '+tclass+' frameborder="0" allowfullscreen="" scrolling="no" allow="autoplay;fullscreen" width="'+width+ '" height="'+height+ '" src="https://onelineplayer.com/player.html?autoplay='+autoplay+'&autopause='+autopause+'&muted='+muted+ '&loop='+loop+'&url='+url+ '&poster='+poster+ '&time='+time+ '&progressBar='+progress+ '&overlay='+overlay+'&muteButton='+muteb+ '&fullscreenButton='+fullscb+ '&style='+style+ '&quality=auto&playButton='+playb+ '"'+strstyle+ '></iframe>"'.format(url=url)
        # print(loop,autopause,autoplay,muted)
        print(gifmode)
        # print(gifmod)


        iframe2='"<iframe id="fra" '+tclass+' frameborder="0" allowfullscreen="" scrolling="no" allow="autoplay;fullscreen" width="100%" height="100%" src="https://onelineplayer.com/player.html?autoplay='+autoplay+'&autopause='+autopause+'&muted='+muted+ '&loop='+loop+'&url='+url+ '&poster='+poster+ '&time='+time+ '&progressBar='+progress+ '&overlay='+overlay+'&muteButton='+muteb+ '&fullscreenButton='+fullscb+ '&style='+style+ '&quality=auto&playButton='+playb+ '"style="position: absolute; height:100%; width: 100%; left: 0px; top: 0px; background-color: #000000;"></iframe>"'.format(url=url)

        # style = "'+strstyle+'"
        DICT=[iframe,iframe2]
        print(iframe)
        print(iframe2)


        return json.dumps(DICT)
    return ("<h1>error</h1>")


app.run(debug=True)
