import random
from flask import Flask, request, jsonify, session, render_template
import unicodedata

# ============================================================
# APLIKACIJA
# Ovdje inicijaliziramo Flask aplikaciju.
# ============================================================
app = Flask(__name__)

# Tajni ključ je neophodan za čuvanje ciljne riječi u sesiji korisnikovog preglednika.
app.secret_key = 'tajna_wordle_srednja_skola'


def normalizuj(tekst):
    """
    Unicode normalizacija (NFC) osigurava da npr. slovo 'Š' 
    uvijek bude predstavljeno istim kodom, bez obzira na operativni sistem.
    """
    if not tekst:
        return ""
    return unicodedata.normalize('NFC', tekst.strip().upper())


# ============================================================
# 1️⃣ RJEČNIK RIJEČI (LISTA)
# ============================================================
# TODO (ZADATAK 1):
# Napravi listu od TAČNO 20 bosanskih riječi od 4 slova.
# Sva slova trebaju biti velika (npr. "KUĆA").
# Primjeri: RUŽA, KIŠA, ŽABA, ŠUMA, NOĆI, ...
#
# Kada završiš, svaka riječ će automatski biti normalizovana.
RJECNIK = [normalizuj(r) for r in [
    # TODO: ovdje dodaj riječi
]]


# ============================================================
# 2️⃣ LOGIKA IGRE (Wordle algoritam)
# ============================================================
def provjeri_pogodak(ciljna, pogodak):
    """
    Ova funkcija upoređuje pogodak sa tajnom rječju.
    Vraća listu rezultata (tačno, prisutno ili odsutno) za svako slovo.
    """

    # Početno stanje: SVA slova su siva ("odsutno")
    rezultat = [{'slovo': znak, 'status': 'odsutno'} for znak in pogodak]
    lista_ciljne = list(ciljna)

    # --------------------------------------------------------
    # TODO (ZADATAK 3a):
    # PRVI PROLAZ
    # Ako je slovo na ISTOJ poziciji kao u ciljnoj riječi:
    #   - status postaje "tacno"
    # --------------------------------------------------------
    # TODO: ovdje napiši kod


    # --------------------------------------------------------
    # TODO (ZADATAK 3b):
    # DRUGI PROLAZ
    # Ako slovo NIJE tačno,
    # ali postoji NEGDJE u ciljnoj riječi:
    #   - status postaje "prisutno"
    # --------------------------------------------------------
    # TODO: ovdje napiši kod


    return rezultat


# ============================================================
# 3️⃣ RUTE (BACKEND)
# ============================================================
@app.route("/")
def pozdrav_svijete():
    """Glavna ruta koja inicijalizira igru."""

    if 'ciljna_rijec' not in session:
        session['ciljna_rijec'] = random.choice(RJECNIK)

    # TODO (ZADATAK 2):
    # Ispiši tajnu riječ u terminal
    # TODO: ovdje dodaj print

    return render_template("index.html", naslov="Wordle-4")


@app.route('/provjeri', methods=['POST'])
def provjeri():
    """Prima pogodak i provjerava koliko slova dijeli sa ciljnom rječju."""

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
