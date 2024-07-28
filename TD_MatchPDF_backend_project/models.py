from django.db import models

# Create your models here.
tipologia_infisso = {
    "101": "1 ANTA",
    "201": "2 ANTE",
    "202": "2 ANTE",
    "203": "2 ANTE",
    "204": "2 ANTE",
    "401": "2 ANTE",
    "301": "3 ANTE",
    "302": "3 ANTE",
    "303": "3 ANTE",
    "304": "3 ANTE",
    "321": "3 ANTE",
    "322": "3 ANTE",
    "323": "3 ANTE",
    "324": "3 ANTE",
    "414": "3 ANTE",
    "415": "3 ANTE",
    "420": "3 ANTE",
    "421": "3 ANTE",
    "424": "3 ANTE",
    "471": "4 ANTE",
    "472": "4 ANTE",
    "205": "1 ANTA CON SOPRALUCE",
    "206": "1 ANTA CON SOPRALUCE",
    "208": "1 ANTA CON SOPRALUCE",
    "309": "2 ANTE CON SOPRALUCE",
    "310": "2 ANTE CON SOPRALUCE",
    "329": "2 ANTE CON SOPRALUCE",
    "330": "2 ANTE CON SOPRALUCE",
    "403": "2 ANTE CON SOPRALUCE",
    "404": "2 ANTE CON SOPRALUCE",
    "207": "1 ANTA CON SOTTOLUCE FISSO VETRATO",
    "308": "2 ANTA CON SOTTOLUCE FISSO VETRATO",
    "402": "2 ANTA CON SOTTOLUCE FISSO VETRATO",
    "102": "FISSO",
    "601": "HST 2 ANTE",
    "602": "HST 2 ANTE",
    "501": "AST 2 ANTE",
    "502": "AST 2 ANTE",
    "914": "HST 4 ANTE"
}

nodo_centrale = {
    "01": "BIANCO EXTRALISCIO 01",
    "06": "GRIGIO SATINATO 06",
    "07": "BIANCO PERLA GOFFRATO 07",
    "13": "TINTA A LEGNO CASTAGNO 13",
    "19": "TINTA A LEGNO ROVERE 19",
    "27": "BIANCO PERLA SATINATO 27",
    "42": "BIANCO GOFFRATO 42",
    "45": "BIANCO SATINATO 45",
    "46": "GRIGIO SETA SATINATO 46",
    "55": "TINTA A LEGNO NOCE CHIARO 55"
}

nodo_centrale2 = {
    "S28": "NODO CON BATTUTA",
    "25": "NODO CON BATTUTA",
    "28": "NODO SENZA BATTUTA",
    "H25": "NODO HISTORY (MANIGLIA CENTRALE)"
}



maniglie_infissi = {
    "601": "MANIGLIA SERIE 1",
    "602": "MANIGLIA SERIE 1 CON PULSANTE",
    "603": "MANIGLIA SERIE 1 CON CHIAVE",
    "704": "MANIGLIA SERIE 2",
    "707": "MANIGLIA SERIE 2",
    "712": "MANIGLIA SERIE 2 A PRESSIONE",
    "1901; 1911; 3011; 4911": "MANIGLIA SERIE 11",
    "1902; 3012; 4912": "MANIGLIA SERIE 12",
    "1903; 3013; 4913": "MANIGLIA SERIE 13 CODICE 1903",
    "1904; 3014; 4914": "MANIGLIA SERIE 14",
    "1905; 3015; 4915": "MANIGLIA SERIE 15",
    "1906": "MANIGLIA SERIE 16 (SENZA BOCCHETTA)",
    "3016; 4916": "MANIGLIA SERIE 16 (CON BOCCHETTA)",
    "M03": "NERO OPACO M03",
    "M01": "BIANCO OPACO M01",
    "79": "TITANIO GF79",
    "74": "BRONZO 74",
    "56": "EVI 56",
    "40": "OTTONE LUCIDO 40",
    "07": "BIANCO PERLA 07",
    "01": "BIANCO LISCIO 01",
    "43": "ACCIAO INOX 43",
    "E03": "NERO ANODIZZATO E03",
    "E02": "BRONZO SCURO ANODIZZATO E02"
}


modello_finestra = {
    "974": "FIN-WINDOW 77 STEP LINE",
    "935": "FIN-WINDOW 77 STEP LINE DOOR (Profilo maggiorato per inserimento serratura)",
    "935K": "FIN-WINDOW 77 STEP LINE DOOR (Profilo maggiorato per inserimento serratura)",
    "935N": "FIN-WINDOW 77 STEP LINE DOOR (Profilo maggiorato per inserimento serratura)",
    "947": "FIN-WINDOW 77 STEP LINE DOOR OUT (Profilo maggiorato per inserimento serratura)",
    "947K": "FIN-WINDOW 77 STEP LINE DOOR OUT (Profilo maggiorato per inserimento serratura)",
    "973": "FIN-WINDOW 77 CLASSIC LINE",
    "973K": "FIN-WINDOW 77 CLASSIC LINE",
    "970": "FIN-WINDOW 77 SLIM LINE",
    "970K": "FIN-WINDOW 77 SLIM LINE",
    "C988": "FIN-WINDOW 77 SLIM LINE TWIN",
    "C988K": "FIN-WINDOW 77 SLIM LINE TWIN",
    "C788": "FIN-WINDOW 77 SLIM LINE TWIN",
    "C788K": "FIN-WINDOW 77 SLIM LINE TWIN",
    "954": "FIN-WINDOW 77 STEP LINE CRISTAL",
    "954K": "FIN-WINDOW 77 STEP LINE CRISTAL",
    "C979": "FIN-WINDOW 77 SLIM-LINE CRISTAL TWIN",
    "C979K": "FIN-WINDOW 77 SLIM-LINE CRISTAL TWIN",
    "C779": "FIN-WINDOW 77 SLIM-LINE CRISTAL TWIN",
    "C779K": "FIN-WINDOW 77 SLIM-LINE CRISTAL TWIN",
    "953": "FIN-WINDOW 77 NOVA LINE",
    "971": "FIN-WINDOW 77 NOVA LINE",
    "N989": "FIN-WINDOW 77 NOVA LINE PLUS",
    "A27": "FIN-PROJECT CLASSIC LINE",
    "A26": "FIN-PROJECT CLASSIC LINE",
    "7A27": "FIN-PROJECT CLASSIC LINE",
    "9A27": "FIN-LIGNA CLASSIC LINE",
    "9Z27": "FIN-LIGNA CLASSIC LINE",
    "9A26": "FIN-LIGNA CLASSIC LINE",
    "A57": "FIN-PROJECT CLASSIC LINE CRISTAL",
    "812": "FIN-PROJECT CLASSIC LINE DOOR",
    "815": "FIN-PROJECT CLASSIC LINE DOOR",
    "A18": "FIN-PROJECT FERRO LINE",
    "A14": "FIN-PROJECT FERRO LINE",
    "7A18": "FIN-PROJECT FERRO LINE",
    "9S18": "FIN-LIGNA FERRO LINE",
    "9A14": "FIN-LIGNA FERRO LINE",
    "9A18": "FIN-LIGNA FERRO LINE",
    "A55": "FIN-PROJECT FERRO LINE CRISTAL",
    "A11": "FIN-PROJECT NOVA LINE",
    "9A10": "FIN-PROJECT NOVA LINE",
    "9A11": "FIN-LIGNA NOVA LINE",
    "A34": "FIN-PROJECT NOVA LINE CRISTAL TWIN",
    "A29": "FIN-PROJECT NOVA LINE PLUS",
    "7A24": "FIN-PROJECT NOVA LINE PLUS",
    "A24": "FIN-PROJECT NOVA LINE PLUS",
    "9Z24": "FIN-LIGNA NOVA LINE PLUS",
    "9A24": "FIN-LIGNA NOVA LINE PLUS",
    "9A29": "FIN-LIGNA NOVA LINE PLUS",
    "7A32": "FIN-PROJECT NOVA LINE TWIN",
    "A32": "FIN-PROJECT NOVA LINE TWIN",
    "9A32": "FIN-LIGNA NOVA LINE TWIN",
    "A17": "FIN-PROJECT SLIM LINE",
    "A16": "FIN-PROJECT SLIM LINE",
    "7A17": "FIN-PROJECT SLIM LINE",
    "9A16": "FIN-LIGNA SLIM LINE",
    "9A17": "FIN-LIGNA SLIM LINE",
    "9S17": "FIN-LIGNA SLIM LINE",
    "A36": "FIN-PROJECT SLIM LINE CRISTAL",
    "A35": "FIN-PROJECT SLIM LINE CRISTAL TWIN",
    "A31": "FIN-PROJECT SLIM LINE TWIN",
    "7A31": "FIN-PROJECT SLIM LINE TWIN",
    "9A31": "FIN-LIGNA SLIM LINE TWIN",
    "7A25": "FIN-PROJECT STEP LINE",
    "A25": "FIN-PROJECT STEP LINE",
    "9Z25": "FIN-LIGNA STEP LINE",
    "9A25": "FIN-LIGNA STEP LINE",
    "A23": "FIN-PROJECT STEP LINE CRISTAL"
}


canaline_interno_vetro = {
    "01": "CANALINA VETRO BIANCA 01",
    "02": "CANALINA VETRO BIANCA 02",
    "03": "CANALINA VETRO BIANCA 03"
}


fermovetro_infisso = {
    "66": "FERMAVETRO CLASSIC",
    "33": "FERMAVETRO IN STILE",
    "20RC2": "FERMAVETRO NOVA",
    "66RC2": "FERMAVETRO CLASSIC SICUREZZA",
    "33RC2": "FERMAVETRO IN STILE SICUREZZA"
}

nodo_centrale_pattern = r'^[0-79][0-79]/[0-79][0-79]$'
Modello_finestra__cerniere_codice_vetro_infissi_pattern = r'^\d{1,3}$'

soglia_infissi = {
    "9": "SOGLIA STANDARD (Non ribassata)",
    "733": "SOGLIA RIBASSATA",
    "54": "LAMA PARAFREDDO SENZA SOGLIA"
}


tipologia_guarnizione = {
    "3a guarn.": "TERZA GUARNIZIONE",
    "3a e 4a guarn.": "TERZA E QUARTA GUARNIZIONE",
    "nullo": "QUARTA GUARNIZIONE DI BATTUTA"
}

cerniere = {
    "4": "CERNIERE A VISTA",
    "2": "CERNIERE A SCOMPARSA"
}

final_form = {
    "Tipologia_infissi": "",
    "Materiale_infissi": "",
    "Modello_Finestra": "",
    "Colore_PVC": "",
    "Maniglie_infissi": "",
    "Colore_Maniglie_Infissi": "",
    "Nodo_centrale": "",
    "Azionamento": "",
    "Codice_vetro_infissi": "",
    "Vetri_Ornamentali": "",
    "Canalina_interno_vetro_Infisso": "",
    "Fermavetro_Infisso": "",
    "Cerniere": "",
    "Guarnizioni": ""
}