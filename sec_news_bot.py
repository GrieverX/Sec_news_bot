#!/usr/bin/env python3.7

import requests
from bs4 import BeautifulSoup
import json
import os.path
import telepot

queries = dict()
DB = "percorso db file ..."

lista_utenti = [id1, id2, ...]


def load_from_file(DB):
    global queries
    if not os.path.isfile(DB):
        return
    with open(DB) as file:
        queries = json.load(file)
    file.close()


def ricerca():
    ricerca_codiceinsicuro()
    ricerca_securityinfo_news()
    ricerca_securityinfo_emergenze_e_scenari()
    ricerca_securityinfo_minacce_e_guide_alla_sicurezza()
    ricerca_thehackernews()


def sendto(msg):
    global lista_utenti
    for utente in lista_utenti:
        bot.sendMessage(utente, msg)


# controlla se un dato articolo e' gia' presente nelle queries e nel caso non lo sia lo posta
def controlla_e_posta(sito, titolo, data, url):
    global queries
    if not queries.get(sito):  # se manca il sito aggiunge il nuovo sito e i campi relativi
        queries[sito] = {titolo: {"data": data, "url": url}}
        tmp = titolo + "\n" + data + "\n" + url
        sendto(tmp)
    elif not queries.get(sito).get(titolo):  # se il sito e' presente ma l'articolo no aggiunge quello
        queries[sito][titolo] = {"data": data, "url": url}
        tmp = titolo + "\n" + data + "\n" + url
        sendto(tmp)

# ---------------- CODICEINSICURO ----------------
# ricerca nuovi articoli parsando la home del sito codiceinsicuro
def ricerca_codiceinsicuro():
    sito = "https://codiceinsicuro.it"
    global queries
    page = requests.get(sito)
    soup = BeautifulSoup(page.text, 'html.parser')
    blocco_contenuti = soup.find(class_='portus-content-block')
    articoli = blocco_contenuti.find_all(class_='item-content')
    for articolo in articoli:
        titolo = articolo.find('a').contents[0]
        url = sito + articolo.find('a').get('href')
        data = articolo.find('span').contents[1]
        controlla_e_posta(sito, titolo, data, url)
    salva(DB)
# ---------------- FINE CODICEINSICURO ----------------


# ---------------- SECURITYINFO.IT ----------------
# ricerca nuovi articoli parsando la home del sito securityinfo.it
def ricerca_securityinfo_news():
    sito = "https://www.securityinfo.it/"
    global queries
    page = requests.get(sito)
    soup = BeautifulSoup(page.text, 'html.parser')
    blocco_superiore = soup.find(class_='news-recenti widget widget_ultimate_posts')
    securityinfo_news_e_minacce_e_guide_alla_sicurezza_ciclo_for(sito, blocco_superiore)
    salva(DB)


# ciclo for di securityinfo per emergenze e scenari
def securityinfo_emergenze_e_scenari_ciclo_for(sito, blocco_contenuti):
    # primo articolo perche' in un contenitore diverso dagli dagli altri
    primo_articolo = blocco_contenuti.find(class_='feature-text-col')
    titolo = primo_articolo.find(class_='title').get('title')
    url = primo_articolo.find(class_='title').get('href')
    data = primo_articolo.find(class_='meta-date').contents[1]
    controlla_e_posta(sito, titolo, data, url)
    # restanti articoli della sezione
    articoli = blocco_contenuti.find_all(class_='small-feature')
    for articolo in articoli:
        titolo = articolo.find(class_="feature-text").find('a').get('title')
        url = articolo.find('a').get('href')
        data = articolo.find(class_='post-meta').find(class_='meta-date').contents[1]
        controlla_e_posta(sito, titolo, data, url)


# ricerca nuove emergenze parsando la home del sito securityinfo.it
def ricerca_securityinfo_emergenze_e_scenari():
    sito = "https://www.securityinfo.it/"
    global queries
    page = requests.get(sito)
    soup = BeautifulSoup(page.text, 'html.parser')
    # emergenze
    blocco_contenuti = soup.find(class_='main-post-col1')
    securityinfo_emergenze_e_scenari_ciclo_for(sito, blocco_contenuti)
    # scenari
    blocco_contenuti = soup.find(class_='main-post-col2')
    securityinfo_emergenze_e_scenari_ciclo_for(sito, blocco_contenuti)
    salva(DB)


# ciclo for di securityinfo per minacce e giode alla sicurezza
def securityinfo_news_e_minacce_e_guide_alla_sicurezza_ciclo_for(sito, blocco_superiore):
    blocco_contenuti = blocco_superiore.find(class_='upw-posts hfeed')
    articoli = blocco_contenuti.find_all('article')
    for articolo in articoli:
        titolo = articolo.find(class_="entry-title-widget-custom").find('a').contents[0][19:-16:]
        url = articolo.find('a').get('href')
        data = articolo.find(class_='post-meta date').contents[1][1::]
        controlla_e_posta(sito, titolo, data, url)


# ricerca nuove minacce e guide alla sicurezza parsando la home del sito securityinfo.it
def ricerca_securityinfo_minacce_e_guide_alla_sicurezza():
    sito = "https://www.securityinfo.it/"
    global queries
    page = requests.get(sito)
    soup = BeautifulSoup(page.text, 'html.parser')
    # minacce
    blocco_superiore = soup.find(class_='minacce-recenti widget widget_ultimate_posts')
    securityinfo_news_e_minacce_e_guide_alla_sicurezza_ciclo_for(sito, blocco_superiore)
    # guide alla sicurezza
    blocco_superiore = soup.find(class_='guide-last-sb widget widget_ultimate_posts')
    securityinfo_news_e_minacce_e_guide_alla_sicurezza_ciclo_for(sito, blocco_superiore)
    salva(DB)
# ---------------- FINE SECURITYINFO.IT ----------------


# ---------------- THEHACKERNEWS ----------------
# ricerca nuovi articoli parsando la home del sito thehackernews
def ricerca_thehackernews():
    sito = "https://thehackernews.com"
    global queries
    page = requests.get(sito)
    soup = BeautifulSoup(page.text, 'html.parser')
    blocco_contenuti = soup.find(class_='main-left-right clear')
    articoli = blocco_contenuti.find_all(class_='body-post clear')
    for articolo in articoli:
        titolo = articolo.find(class_='home-title').contents[0]
        url = articolo.find('a').get('href')
        data = articolo.find(class_='item-label').contents[1]
        controlla_e_posta(sito, titolo, data, url)
    salva(DB)
# ---------------- FINE THEHACKERNEWS ----------------

def salva(DB):
    with open(DB, 'w') as file:
        file.write(json.dumps(queries))
    file.close()


if __name__ == '__main__':
    bot = telepot.Bot('bot token')
    load_from_file(DB)
    ricerca()
