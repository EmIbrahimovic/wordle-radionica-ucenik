import random
from flask import Flask, request, jsonify, session, render_template
import unicodedata

# 1. APLIKACIJA: Ovdje inicijaliziramo Flask aplikaciju.
app = Flask(__name__)

# Tajni ključ je neophodan za čuvanje ciljne riječi u sesiji korisnikovog preglednika.
app.secret_key = 'tajna_wordle_srednja_skola'

def normalizuj(tekst):
    """
    TRENUTAK ZA UČENJE: Unicode normalizacija (NFC) osigurava da npr. slovo 'Š' 
    uvijek bude predstavljeno istim kodom, bez obzira na operativni sistem.
    """
    if not tekst:
        return ""
    # 'NFC' spaja osnovno slovo i kvačicu u jedan jedinstven karakter.
    return unicodedata.normalize('NFC', tekst.strip().upper())

# 2. RJEČNIK: Lista od 20 bosanskih riječi od 4 slova sa dijakritičkim znakovima.
# TRENUTAK ZA UČENJE: Python 3 podržava Unicode, pa su slova poput Č, Ć, Ž sasvim regularna.
RJECNIK = [normalizuj(r) for r in [
    'RUŽA', 'KUĆA', 'KIŠA', 'ČAŠA', 'VOĆE', 'KOŽA', 'ŠUMA', 'LAĐA', 
    'ŽABA', 'ČVOR', 'VRAČ', 'ČELO', 'DUŠA', 'NOĆI', 'PEĆI', 'MRAZ', 
    'BUĐA', 'MEČE', 'ŽITO', 'BIĆE'
]]

def provjeri_pogodak(ciljna, pogodak):
    """
    TRENUTAK ZA UČENJE: Ova funkcija upoređuje pogodak sa tajnom rječju.
    Vraća listu rezultata (tačno, prisutno ili odsutno) za svako slovo.
    """
    rezultat = [{'slovo': znak, 'status': 'odsutno'} for znak in pogodak]
    lista_ciljne = list(ciljna)
    # Prvi prolaz: Označi slova na tačnoj poziciji (Zeleno)
    for i in range(4):
        if pogodak[i] == ciljna[i]:
            rezultat[i]['status'] = 'tacno'
            lista_ciljne[i] = None
            
    # Drugi prolaz: Označi slova koja postoje ali su na pogrešnom mjestu (Žuto)
    for i in range(4):
        if rezultat[i]['status'] == 'tacno':
            continue
        if pogodak[i] in lista_ciljne:
            rezultat[i]['status'] = 'prisutno'
            lista_ciljne[lista_ciljne.index(pogodak[i])] = None
            
    return rezultat

@app.route("/")
def pozdrav_svijete():
    """Glavna ruta koja inicijalizira igru."""
    if 'ciljna_rijec' not in session:
        session['ciljna_rijec'] = random.choice(RJECNIK)
    print("Tajna riječ je ", session['ciljna_rijec'])
    return render_template("index.html", naslov="Wordle-4")

@app.route('/provjeri', methods=['POST'])
def provjeri():
    """Prima pogodak i provjerava ga protiv rječnika i ciljne riječi."""
    podaci = request.get_json()
    pogodak = normalizuj(podaci.get('pogodak', ''))
    
    # Provjera da li je riječ u rječniku
    if pogodak not in RJECNIK:
        return jsonify({'greska': 'Riječ nije u rječniku'}), 400
        
    ciljna = session.get('ciljna_rijec', normalizuj('RUŽA'))
    rezultati = provjeri_pogodak(ciljna, pogodak)
    
    return jsonify({
        'rezultati': rezultati,
        'pobjeda': pogodak == ciljna,
        'ciljna': ciljna
    })

@app.route('/restart', methods=['POST'])
def restart():
    """Restartuje sesiju sa novom riječi."""
    session['ciljna_rijec'] = random.choice(RJECNIK)
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(debug=True)