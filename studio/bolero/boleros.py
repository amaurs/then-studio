from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

LINK_TEMPLATE = "http://www.morellajimenez.com.do/%s"
LINKS = ["letadoro."letadoro."letacariciame."letacariciame."letalaorilladelmar.h"letalgocontigo."letalgodiferente."letamaryvivir."letamorsinesperanza."letamorconllanto."letamordelacalle."letamorgitano."letamorperdido.h"letamordemivida.h"letamordecobre."letamorosamente."letamorosamente."letamorcitocorazon."letangustia.h"letaquelviejoamor."letarrancamelavida."letarrancamelavida2."letarrancamelavida2."letarrepentida."letaunquemecueste."letbajocero."letbesameotravez."letbesameamor."letbesame."letbuscotrecuerdo."letcataclismo."letcaribesoy."letceloso."letcercadelmar."letcaminemos."letcaminopuente."letcenizas."letciegodamor."letciegodamor."let5centavitos."let5centavitos."letcienanos."letcienanos."letcondicion."letcongoja."letcongoja."letconmicorazon."letcontigolospanchos."letcontigo2."letconaprendi."letcomohanpasado.h"letcomohepodido."letcomofue."letconciertootono."letcorazonhotel."letcorazonloco."letcorazondeacero."letcosasdalma."letcosascomotu."letcosascomotu."letcrei."letcuanvuelva."letcuandonomequieras."letcuandoelamor."letcuandotmquieras."letcuandoestoycontigo."letcuandoestemosviejos."letcuandoestemosviejos."letdecigarroencigarro."letdemujeramujer."letdondestascorazon."letdosalmas."letdosgardenias."letdondequieraqestes."letdileque."letdelito."letdimelo."letegoismo."letel19."letelarbol."letelarbol."letelpayador."Letenorillamar."letencadenados."letesperanzinutil."letesperare."letenunrincon."letenlaoscuridad."letenunbesovida.h"letentretuamor."letenamorado."letenvidia."letesoshombres."letelamoracaba."letelmalquerido."letelmaryelcielo."letescandalo."letescribeme."letespumas."letevocacion."letesperame."letesperame."letesa."letfalsa."letfichasnegras."letflordazalea."letfloresnegras."letfrenesi."lethazunmilagro."lethayqsaberperder."lethesabidoqtamaba."letholasoledad."lethipocrita."lethdunamor."lethojaseca."lethoyesviernes."letincertidumbre."letinolvidable."letjurame."letjuguete."letlabarca."letlagrimasalma."letlagrimasnegras."letaretesdeluna."letlapared."letluzysombras."letlacoparota."letlapuerta."letloquetuvecontigo2."letlagloria."letllantodeluna.h"letllevame."letllevatela."letmadrigal."letmuchcorazon."letmienteme.h"letmujer."letmisnochesinti."letmicorazonada."letmujerdivina."letmilbesos."letmigajas."letmiraquelinda."letmiultimofracaso."letmitodo."letmotivos."letmorirdeamor."letmunequitalinda."letmicarino."letnegrura."letnaufragio."letnosotros."letnostalgia."letnoplatiques."letnomevayasaenganar."letnuestrojuramento."letnocheronda."letnoesvenganza."letnoquieroqtvayas."letolvidame."letojostristes."letorgasmo."letobsesion."letpalabrasmujer."letpalabrascielo."letparaquevolver."letpareceayer."letperfidia."letperfidia."letperfumegardenia."letpeleas."letporquenollorar."letporqahora."letpordoscaminos."letporfin."letpoquitafe."letprisionero.h"letpresentimiento."letpuedendecir."letquiereme."letquequierestudemi."letrondandotuesquina."letregalamenoche."letrayitoluna."letrayitoluna."letreloj."letsabordengano."letsaboranada."letsaborami."letsabrasqtequiero."letsentimiento."letsemeolvidotn."letsenora."letsenorabonita."letseteolvida."letsinegoismo."letsinunamor."letsimecomprendieras."letsitecontara."letsomosdiferentes2.h"letsoyloprohibido."letsolamente1vez."letsonar."lettextrano."lettristezamarina."leteodioytequiero.h"lettiemblas."letumeacostumbraste."letumehacesfalta."lettemeridad."letunocomprendes."letupanuelo."letriunfamos."letupromesadamor."letotal."lettodomegustadeti."let3palabras."leteamaretodalavida."letunacopamas."letunviejoamor."letunsiglodausencia."letunpocomas."letusted."letunalimosna."letunamorparalahistoria."letunamorcalle."letunicamentetu2.h"letunaventuramas."letviajera."letvidaconsentida."letvirgenmediancohe."letvoy."letvuelvemequerer."letviejaluna."leyasonlas12.h"letlinda."letyovivomivida.htm"]

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def main():
    """
    Parses and filters content for the bolero songs.
    """
    file = open("boleros.txt","w") 
    for link in list(set(LINKS)):
        try:
            final_link = LINK_TEMPLATE % link
            raw_html = simple_get(final_link)
            html = BeautifulSoup(raw_html, 'html.parser')
            song = ""
            for p in html.find_all('p', align=True):
                sentence = " ".join(p.text.split())
                if "Página Principal" in sentence or 
                   "Imágenes" in sentence or 
                   "Imagen" in sentence or 
                   "Tube" in sentence:
                    break
                else:
                    if not "Autor" in sentence:
                        song = song + " " + sentence
            file.write(song.strip() + "\n") 
        except Exception as e:
            log_error(e)
    file.close() 

if __name__ == '__main__':
    main()
