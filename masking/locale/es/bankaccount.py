#!/usr/bin/env python

"""

Each country has a specific IBAN structure.

Spain example:

IBAN                ES91 2100 0418 4502 0005 1332
ISO Country Code    ES (Spain)
IBAN Check Digits   91
BBAN                2100 0418 4502 0005 1332
Bank Identifier     2100
Branch Identifier   0418
Account Number      0200051332
BBAN Check Digit(s) 45
SEPA Member         Yes


See:
    https://en.wikipedia.org/wiki/International_Bank_Account_Number
    https://www.iban.es/codigos-de-entidades-bancarias.html


Usage:

    import masking.locale.es.bankaccount as bankaccount

    bank = bankaccount.Bank("1465")
    print bankaccount.IBAN.generate(bank.code, bank.branch)
    print bankaccount.BBAN.generate(bank.code, bank.branch)

"""


import random
import string


class IBANInvalidLength(Exception):
    """When an IBAN is != 24 chars."""
    pass

class IBANInvalidCountry(Exception):
    """When an IBAN is instanced with the wrong country."""
    pass

class IBANInvalidBankCode(Exception):
    """When the bank code can't be found in our list."""
    pass

class IBANInvalidCheckDigit(Exception):
    """When the IBAN's check digit is incorrect."""
    pass

class BBANInvalidLength(Exception):
    """When a BBAN is != 20 chars."""
    pass

class BBANInvalidBankCode(Exception):
    """WHen the bank code can't be found in our list."""
    pass

class BBANInvalidBankBranchCheckDigit(Exception):
    """When the first check digit is invalid."""
    pass

class BBANInvalidAccountCheckDigit(Exception):
    """When the second check digit is invalid."""
    pass


BANKS = {
  "0136": {
    "name": "ARESBANK",
    "bic": "AREBESMMXXX"
  },
  "0238": {
    "name": "BANCO-PASTOR",
    "bic": "POPUESMMXXX"
  },
  "0130": {
    "name": "BANCO-CAIXA-GRAL",
    "bic": "CGDIESMMXXX"
  },
  "0038": {
    "name": "SANTANDER-BANCO-EMISIONES",
    "bic": "BSCHESMMXXX"
  },
  "0132": {
    "name": "BANCO-PROMOCION-NEGOCIOS",
    "bic": "PRNEESM1XXX"
  },
  "0133": {
    "name": "NUEVO-MICROBANK",
    "bic": "MIKBESB1XXX"
  },
  "0233": {
    "name": "POPULAR-BANCA-PRIVADA",
    "bic": "POPIESMMXXX"
  },
  "0232": {
    "name": "BANCO-INVERSIS",
    "bic": "INVLESMMXXX"
  },
  "0231": {
    "name": "DEXIA-SABADELL",
    "bic": "DSBLESMMXXX"
  },
  "0036": {
    "name": "SANTANDER-IVESTMENT",
    "bic": "SABNESMMXXX"
  },
  "0138": {
    "name": "BANKOA",
    "bic": "BKOAES22XXX"
  },
  "0239": {
    "name": "EVO-BANK",
    "bic": "EVOBESMMXXX"
  },
  "0235": {
    "name": "BANCO-PICHINCHA",
    "bic": "PIESESM1XXX"
  },
  "0234": {
    "name": "BANCO-CAMINOS",
    "bic": "CCOCESMMXXX"
  },
  "2095": {
    "name": "KUTXABANK",
    "bic": "BASKES2BXXX"
  },
  "2096": {
    "name": "CAJA-ESPANA-NVERSIONES",
    "bic": "CSPAES2LXXX"
  },
  "3095": {
    "name": "CAJA-RURAL-SANROQUE",
    "bic": "BCOEESMM095"
  },
  "2013": {
    "name": "CATALUNYA-BANK",
    "bic": "CESCESBBXXX"
  },
  "3045": {
    "name": "CAIXA-RURAL-ALTEA",
    "bic": "BCOEESMM045"
  },
  "0131": {
    "name": "BANCO-ESPIRITO-SANTO",
    "bic": "BESMESMMXXX"
  },
  "1546": {
    "name": "CNH-CAPITAL",
    "bic": "CNCUFRP1XXX"
  },
  "1544": {
    "name": "ANDBANK",
    "bic": "BACAESMMXXX"
  },
  "1545": {
    "name": "CREDIT-ACRICOLE-LUXEMBURGO",
    "bic": "AGRIESMMXXX"
  },
  "1535": {
    "name": "AKF-BANK",
    "bic": "AKFBDE33XXX"
  },
  "3121": {
    "name": "CAJA-RURAL-CHESTE",
    "bic": "BCOEESMM121"
  },
  "3127": {
    "name": "CAJA-RURAL-CASASIBANEZ",
    "bic": "BCOEESMM127"
  },
  "1549": {
    "name": "MAINFIRST",
    "bic": "MAIFDFFXXX"
  },
  "0144": {
    "name": "BNP-PARIBAS-SECURITES",
    "bic": "PARBESMXXXX"
  },
  "2401": {
    "name": "CAJA-PENSIONES-BARCELONA",
    "bic": "CAIXESBBXXX"
  },
  "1465": {
    "name": "ING-DIRECT",
    "bic": "INGDESMMXXX"
  },
  "1467": {
    "name": "HYPOTHEKENBANK-FRNAKFURT",
    "bic": "EHYPESMXXXX"
  },
  "3190": {
    "name": "CAJA-RURAL-ALBACETE",
    "bic": "BCOEESMM190"
  },
  "1460": {
    "name": "CREDIT-SUISSE-AG",
    "bic": "CRESESMMXXX"
  },
  "1463": {
    "name": "BANQUE-PSA-FINANCE",
    "bic": "PSABESM1XXX"
  },
  "0049": {
    "name": "BANCO-SANTANDER",
    "bic": "BSCHESMMXXX"
  },
  "0125": {
    "name": "BANCOFAR",
    "bic": "BAOFESM1XXX"
  },
  "0122": {
    "name": "CITIBANK",
    "bic": "CITIES2XXXX"
  },
  "0121": {
    "name": "BANCO-OCCIDENTAL",
    "bic": "OCBAESM1XXX"
  },
  "0031": {
    "name": "BANCO-ETCHEVARRIA",
    "bic": "ETCHES2GXXX"
  },
  "3183": {
    "name": "CAJA-ARQUITECTOS-COOP",
    "bic": "CASDESBBXXX"
  },
  "0046": {
    "name": "BANCO-GALLEGO",
    "bic": "GALEES2GXXX"
  },
  "0128": {
    "name": "BANKINTER",
    "bic": "BKBKESMMXXX"
  },
  "1490": {
    "name": "SELF-TRADE-BANK",
    "bic": "SELFESMMXXX"
  },
  "1491": {
    "name": "TRIODOS-BANK",
    "bic": "TRIOESMMXXX"
  },
  "1492": {
    "name": "BNP-PARIBAS-LEASE",
    "bic": "ESSIESMMXXX"
  },
  "1493": {
    "name": "CAIXA-BANCO-INVESTIMENTO",
    "bic": "CXBIPTPLXXX"
  },
  "1494": {
    "name": "INTESA-SANPAOLO",
    "bic": "BCITESMMXXX"
  },
  "3130": {
    "name": "CAJA-RURAL-ALMASSORA",
    "bic": "BCOEESMM130"
  },
  "1496": {
    "name": "GENEFIM",
    "bic": "GENFFRP1XXX"
  },
  "1499": {
    "name": "CLAAS-FINANCIAL",
    "bic": "CLAAFRP1XXX"
  },
  "3138": {
    "name": "CAJA-RURAL-BETXI",
    "bic": "BCOEESMM138"
  },
  "3035": {
    "name": "CAJA-LABORAL-POPULAR",
    "bic": "CLPEES2MXXX"
  },
  "2415": {
    "name": "CAJA-EXTREMADURA",
    "bic": "CECAESMM099"
  },
  "2105": {
    "name": "BANCO-CASTILLA-MANCHA",
    "bic": "CECAESMM105"
  },
  "2416": {
    "name": "CAJA-CANTABRIA",
    "bic": "CECAESMM066"
  },
  "2038": {
    "name": "BANKIA",
    "bic": "CAHMESMMXXX"
  },
  "0113": {
    "name": "BANCO-INDUSTRIAL-BILBAO",
    "bic": "INBBESM1XXX"
  },
  "0059": {
    "name": "BANCO-MADRID",
    "bic": "MADRESMMXXX"
  },
  "0058": {
    "name": "BNP-PARIBAS",
    "bic": "BNPAESMMXXX"
  },
  "0115": {
    "name": "BANCO-CASTILLA-LAMANCHA",
    "bic": "CECAESMM115"
  },
  "0057": {
    "name": "BANCO-DEPOSITARIO-BBVA",
    "bic": "BVADESMMXXX"
  },
  "3140": {
    "name": "CAJA-RURAL-GUISSONA",
    "bic": "BCOEESMM140"
  },
  "1482": {
    "name": "JOHN-DEERE-BANK",
    "bic": "CHASESM3XXX"
  },
  "1481": {
    "name": "BANCO-MAIS",
    "bic": "ESMMES64XXX"
  },
  "1480": {
    "name": "VOLKSWAGEN-BANK",
    "bic": "VOWAES21XXX"
  },
  "1487": {
    "name": "TOYOTA-KREDITBANK",
    "bic": "TKGTFR21XXX"
  },
  "1485": {
    "name": "BANK-OF-AMERICA",
    "bic": "BOFAES2XXXX"
  },
  "1488": {
    "name": "PICTET-CIE",
    "bic": "PICTESMMXXX"
  },
  "3134": {
    "name": "CAJA-RURAL-SRAESPERANZA",
    "bic": "BCOEESMM134"
  },
  "3165": {
    "name": "CAJA-RURAL-SANISIDROVILAFAMES",
    "bic": "BCOEESMM165"
  },
  "3029": {
    "name": "CAJA-CREDITO-PETREL",
    "bic": "BCOEESMM029"
  },
  "3162": {
    "name": "CAJA-RURAL-BENICARLO",
    "bic": "BCOEESMM162"
  },
  "3025": {
    "name": "CAIXA-CREDIT-ENGINYERS",
    "bic": "CDENESBBXXX"
  },
  "3023": {
    "name": "CAJA-RURAL-GRANADA",
    "bic": "BCOEESMM023"
  },
  "3020": {
    "name": "CAJA-RURAL-UTRERA",
    "bic": "BCOEESMM020"
  },
  "1524": {
    "name": "UBI-BANCA",
    "bic": "UBIBESMMXXX"
  },
  "1525": {
    "name": "BANQUE-CHAABI-MAROC",
    "bic": "BCDMESMMXXX"
  },
  "2108": {
    "name": "BANCO-CAJAESPANA-SALAMANCASORIA",
    "bic": "CSPAES2L108"
  },
  "3160": {
    "name": "CAIXA-RURAL-SANTJOSEPCOOP",
    "bic": "BCOEESMM160"
  },
  "0200": {
    "name": "PRIVAT-BANK-DEGROOF",
    "bic": "PRVBESB1XXX"
  },
  "1523": {
    "name": "MERCEDES-BENZ-BANK",
    "bic": "DEUTESBBXXX"
  },
  "0444": {
    "name": "SISTEMA-4B",
    "bic": ""
  },
  "1528": {
    "name": "JCB-FINANCE",
    "bic": "ES1528"
  },
  "1530": {
    "name": "SOFINLOC",
    "bic": "FIOFESM1XXX"
  },
  "0108": {
    "name": "SOCIETE-GENERALE",
    "bic": "SOGEESMMXXX"
  },
  "3152": {
    "name": "CAJA-RURAL-VILLAR",
    "bic": "BCOEESMM152"
  },
  "3150": {
    "name": "CAJA-RURAL-ALBALCOOP",
    "bic": "BCOEESMM150"
  },
  "3157": {
    "name": "CAJA-RURAL-JUNQUERA",
    "bic": "BCOEESMM157"
  },
  "9000": {
    "name": "BANCO-DE-ESPANA",
    "bic": "ESPBESMMXXX"
  },
  "3159": {
    "name": "CAIXA-POPULAR-SDADCOOP",
    "bic": "BCOEESMM159"
  },
  "0237": {
    "name": "CAJASUR-BANCO",
    "bic": "CSURES2CXXX"
  },
  "3018": {
    "name": "CAJA-RURAL-SANAGUSTIN",
    "bic": "BCOEESMM018"
  },
  "2045": {
    "name": "CAIXA-DESTALVIS-ONTINENT",
    "bic": "CECAESMM045"
  },
  "2056": {
    "name": "CAIXA-DESTALVIS-POLLENSA",
    "bic": "CECAESMM056"
  },
  "3016": {
    "name": "CAJA-RURAL-SALAMANCA",
    "bic": "BCOEESMM016"
  },
  "3017": {
    "name": "CAJA-RURAL-SORIA",
    "bic": "BCOEESMM017"
  },
  "2048": {
    "name": "LEBERBANK",
    "bic": "CECAESMM048"
  },
  "1510": {
    "name": "SAXO-BANK",
    "bic": "SAXODKKKXXX"
  },
  "0211": {
    "name": "EBN-BANCO-NEGOCIOS",
    "bic": "PROAESMMXXX"
  },
  "1536": {
    "name": "OREY-FINANCIAL",
    "bic": "OVSCPTP1XXX"
  },
  "0198": {
    "name": "BANCO-COOPERATIVO-ESPANOL",
    "bic": "BCOEESMMXXX"
  },
  "3096": {
    "name": "CAIXA-RURAL-LALCUDIA",
    "bic": "BCOEESMM096"
  },
  "1532": {
    "name": "BNP-PARIBAS-FACTOR",
    "bic": "BNPAESMSXXX"
  },
  "1531": {
    "name": "CREDIT-SUISSE",
    "bic": "CSROESM1XXX"
  },
  "0216": {
    "name": "TARGOBANK",
    "bic": "POHIESMMXXX"
  },
  "0219": {
    "name": "BANQUE-MAROCAINE-COMMERCE",
    "bic": "BMCEESMMXXX"
  },
  "0218": {
    "name": "FCE-BANK-PLC",
    "bic": "FCEFESM1XXX"
  },
  "0190": {
    "name": "BANCO-BPI",
    "bic": "BBPIESMMXXX"
  },
  "0236": {
    "name": "SABADELL-SOLBANK",
    "bic": "LOYIESMMXXX"
  },
  "1000": {
    "name": "ICO",
    "bic": "ICROESMMXXX"
  },
  "3115": {
    "name": "CAJA-RURAL-MADRESOL",
    "bic": "BCOEESMM115"
  },
  "3123": {
    "name": "CAIXA-RURAL-TURIS",
    "bic": "BCOEESMM123"
  },
  "1522": {
    "name": "EFG-BANK",
    "bic": "EFGBESMMXXX"
  },
  "3005": {
    "name": "CAJA-RURAL-CENTRAL",
    "bic": "BCOEESMM005"
  },
  "3007": {
    "name": "CAJA-RURAL-GIJON",
    "bic": "BCOEESMM007"
  },
  "3001": {
    "name": "CAJA-RURAL-ALMENDRALEJO",
    "bic": "BCOEESMM001"
  },
  "3166": {
    "name": "CAIXA-RURAL-LESCOVESVINROMAS",
    "bic": "BCOEESMM166"
  },
  "2000": {
    "name": "CECABANK",
    "bic": "CECAESMMXXX"
  },
  "3009": {
    "name": "CAJA-RURAL-EXTREMADURA",
    "bic": "BCOEESMM009"
  },
  "3008": {
    "name": "CAJA-RURAL-NAVARRA",
    "bic": "BCOEESMM008"
  },
  "3113": {
    "name": "CAJA-RURAL-SANJOSEALCORA",
    "bic": "BCOEESMM113"
  },
  "2414": {
    "name": "CAJA-ASTURIAS",
    "bic": "CECAESMMO48"
  },
  "0184": {
    "name": "BANCO-EUROPEO-FINANZAS",
    "bic": "BEDFESM1XXX"
  },
  "3144": {
    "name": "CAJA-RURAL-VILLAMALEA",
    "bic": "BCOEESMM144"
  },
  "0186": {
    "name": "BANDO-MEDIOLANUM",
    "bic": "BFIVESBBXXX"
  },
  "0182": {
    "name": "BBVA",
    "bic": "BBVAESMMXXX"
  },
  "0188": {
    "name": "BANCO-ALCALA",
    "bic": "ALCLESMMXXX"
  },
  "1502": {
    "name": "IKB-DEUTSCHE-INDUSTRIEBANK",
    "bic": "IKBDESM1XXX"
  },
  "1500": {
    "name": "NATIXIS-LEASE",
    "bic": "NALEFRP1XXX"
  },
  "0065": {
    "name": "BLARCLAYS-BANK",
    "bic": "BARCESMMXXX"
  },
  "3089": {
    "name": "CAJA-RURAL-BAENA",
    "bic": "BCOEESMM089"
  },
  "1504": {
    "name": "HONDA-BANK",
    "bic": "HONDDEF1XXX"
  },
  "0061": {
    "name": "BANCA-MARCH",
    "bic": "BMARES2MXXX"
  },
  "3085": {
    "name": "CAJA-RURAL-ZAMORA",
    "bic": "BCOEESMM085"
  },
  "1508": {
    "name": "RCI-BANQUE",
    "bic": "RCIDDE31XXX"
  },
  "1509": {
    "name": "BANCO-PRIMUS",
    "bic": "PRUUPTP1XXX"
  },
  "3081": {
    "name": "CAJA-RURAL-CASTILLALAMANCHA",
    "bic": "BCOEESMM081"
  },
  "3080": {
    "name": "CAJA-RURAL-TERUEL",
    "bic": "BCOEESMM080"
  },
  "0488": {
    "name": "BANCO-FINANCIERO",
    "bic": "BFASESMMXXX"
  },
  "2429": {
    "name": "CAJA-BADAJOZ",
    "bic": "CECAESMM429"
  },
  "0169": {
    "name": "BANCO-NACION-ARGENTINA",
    "bic": "NACNESMMXXX"
  },
  "0168": {
    "name": "ING-BELGIUM",
    "bic": "BBRUESMXXXX"
  },
  "0003": {
    "name": "BANCO-DEPOSITOS",
    "bic": "BDEPESM1XXX"
  },
  "2420": {
    "name": "IBERCAJA",
    "bic": "CAZRES2ZXXX"
  },
  "0162": {
    "name": "HSBC-BANK",
    "bic": "MIDLESMMXXX"
  },
  "0161": {
    "name": "DEUTSCHE-BANK-AMERICAS",
    "bic": "BKTRESM1XXX"
  },
  "0160": {
    "name": "BANK-OF-TOKYO",
    "bic": "BOTKESMXXXX"
  },
  "0167": {
    "name": "BNP-PARIBAS-FORTIS",
    "bic": "GEBAESMMXXX"
  },
  "2426": {
    "name": "CAJA-RONDA",
    "bic": "UCJAES2MXXX"
  },
  "0487": {
    "name": "BANCO-MARE-NOSTRUM",
    "bic": "GBMNESMMXXX"
  },
  "3070": {
    "name": "CAIXA-RURAL-GALEGA",
    "bic": "BCOEESMM070"
  },
  "0149": {
    "name": "BNP-SUCURSLA-ESPANA",
    "bic": "BNPAESMSXXX"
  },
  "3076": {
    "name": "CAJA-RURAL-CAJASIETE",
    "bic": "BCOEESMM076"
  },
  "3174": {
    "name": "CAIXA-RURAL-VINAROS",
    "bic": "BCOEESMM174"
  },
  "3179": {
    "name": "CAJA-RURAL-ALGINET",
    "bic": "BCOEESMM179"
  },
  "0073": {
    "name": "OPEN-BANK",
    "bic": "OPENESMMXXX"
  },
  "1457": {
    "name": "DELAGE-LANDEN-INTB",
    "bic": "LLISESM1XXX"
  },
  "0075": {
    "name": "BANCO-POPULAR",
    "bic": "POPUESMMXXX"
  },
  "1451": {
    "name": "CAISSE-REGIONALE-SUDMEDITERRANEE",
    "bic": "CRCGESB1XXX"
  },
  "3116": {
    "name": "CAJA-RURAL-MOTACUERVO",
    "bic": "BCOEESMM116"
  },
  "2103": {
    "name": "UNICAJA-BANCO",
    "bic": "UCJAES2MXXX"
  },
  "0078": {
    "name": "BANCO-PUEYO",
    "bic": "BAPUES22XXX"
  },
  "2100": {
    "name": "CAIXABANK",
    "bic": "CAIXESBBXXX"
  },
  "1459": {
    "name": "COPERATIVE-RAIFFEISEN",
    "bic": "PRABESMMXXX"
  },
  "1513": {
    "name": "CAIXA-GERAL-DEPOSITOS",
    "bic": "CGDIES21XXX"
  },
  "2104": {
    "name": "CAJA-SALAMANCA-SORIA",
    "bic": "CSSOES2SXXX"
  },
  "2428": {
    "name": "CAJA-CIRCULO-BUROS",
    "bic": "CECAESMM428"
  },
  "3146": {
    "name": "CAJA-CREDITO-COOPERATIVO",
    "bic": "CCCVESM1XXX"
  },
  "0011": {
    "name": "ALLFUNDS-BANK",
    "bic": "ALLFESMMXXX"
  },
  "1475": {
    "name": "CORTAL-CONSORS",
    "bic": "CCSEESM1XXX"
  },
  "2433": {
    "name": "CECA",
    "bic": "CECAESMMXXX"
  },
  "2432": {
    "name": "CAJA-VITORIA-ALAVA",
    "bic": "CECAESMM097"
  },
  "2431": {
    "name": "CAJA-GUIPUZOCA",
    "bic": "CGGKES22XXX"
  },
  "2430": {
    "name": "BILBAO-BIZKAIA-KUTXA",
    "bic": "BASKES2BXXX"
  },
  "0019": {
    "name": "DEUTSCHE-BANK",
    "bic": "DEUTESBBXXX"
  },
  "3063": {
    "name": "CAJA-RURAL-CORDOBA",
    "bic": "BCOEESMM063"
  },
  "3060": {
    "name": "CAJA-RURAL-FUENTESEGOVIA",
    "bic": "BCOEESMM060"
  },
  "3067": {
    "name": "CAJA-RURAL-JAEN",
    "bic": "BCOEESMM067"
  },
  "3110": {
    "name": "CAJA-RURAL-CATOLICOAGRARIA",
    "bic": "BCOESSMM110"
  },
  "1472": {
    "name": "CREDIT-AGRICOLE-FACTORING",
    "bic": "UCSSESM1XXX"
  },
  "3104": {
    "name": "CAJA-RURAL-CANETETORRES",
    "bic": "BCOEESMM104"
  },
  "3105": {
    "name": "CAIXA-RURAL-CALLOSA",
    "bic": "BCOEESMM105"
  },
  "1470": {
    "name": "BANCO-PORTUGUES-INVESTIMENTO",
    "bic": "BPIPESM1XXX"
  },
  "3102": {
    "name": "CAIXA-SANTFERRER-DUIXO",
    "bic": "BCOEESMM102"
  },
  "1538": {
    "name": "INDUSTRIAL-COMMERCIAL-CHINA",
    "bic": "ICBKESMMXXX"
  },
  "3186": {
    "name": "CAIXA-RURAL-ALBALAT",
    "bic": "BCOEESMM186"
  },
  "3187": {
    "name": "CAJA-RURAL-DELSUR",
    "bic": "BCOEESMM187"
  },
  "1505": {
    "name": "EUROPE-ARAB-BANK",
    "bic": "ARABESMMXXX"
  },
  "2421": {
    "name": "CAJA-GRANADA",
    "bic": "CECAESMM031"
  },
  "0081": {
    "name": "BANCO-SABADELL",
    "bic": "BSABESBBXXX"
  },
  "0083": {
    "name": "RENTA4",
    "bic": "RENBESMMXXX"
  },
  "0229": {
    "name": "BANCO-POPULAR-ESA",
    "bic": "POPLESMMXXX"
  },
  "3191": {
    "name": "CAJA-RURAL-ARAGON",
    "bic": "BCOEESMM191"
  },
  "0220": {
    "name": "BANCO-FINANTIA-CAPITAL",
    "bic": "FIOFESM1XXX"
  },
  "2424": {
    "name": "CAJA-BALEARES",
    "bic": "CECAESMM051"
  },
  "0223": {
    "name": "GENERAL-ELECTRIC-BANK",
    "bic": "GEECESB1XXX"
  },
  "0224": {
    "name": "SANTANDER-CONSUMER",
    "bic": "SCFBESMMXXX"
  },
  "0225": {
    "name": "BANCO-CETELEM",
    "bic": "FIEIESM1XXX"
  },
  "0226": {
    "name": "UBS-BANK",
    "bic": "UBSWESMMXXX"
  },
  "0227": {
    "name": "UNOE-BANK",
    "bic": "UNOEESM1XXX"
  },
  "3058": {
    "name": "CAJAS-RURALES-UNIDAS CAJAMAR",
    "bic": "CCRIES2AXXX"
  },
  "3059": {
    "name": "CAJA-RURAL-ASTURIAS",
    "bic": "BCOEESMM059"
  },
  "1501": {
    "name": "DEUTSCHE-PFANDBRIEFBANK",
    "bic": "DPBBESM1XXX"
  },
  "2427": {
    "name": "CAJA-INMACULADA",
    "bic": "CECAESMM427"
  },
  "2422": {
    "name": "CAJA-MURCIA",
    "bic": "CECAESMM043"
  },
  "3098": {
    "name": "CAJA-RURAL-NTRASE\u00d1ORAROSARIO",
    "bic": "BCOEESMM098"
  },
  "3135": {
    "name": "CAJA-RURAL-SANJOSENULES",
    "bic": "BCOEESMM135"
  },
  "1479": {
    "name": "NATIXIS",
    "bic": "NATXESMMXXX"
  },
  "3119": {
    "name": "CAJA-RURAL-SANJAIME",
    "bic": "BCOEESMM119"
  },
  "3118": {
    "name": "CAIXA-RURAL-TORRENT",
    "bic": "BCOEESMM118"
  },
  "3117": {
    "name": "CAIXA-RURAL-DALGEMESI",
    "bic": "BCOEESMM117"
  },
  "0196": {
    "name": "PORTIGON-AG",
    "bic": "WELAESMMXXX"
  },
  "2080": {
    "name": "NGC-BANCO",
    "bic": "CAGLESMMVIG"
  },
  "2086": {
    "name": "BANCO-GRUPO-CAJATRES",
    "bic": "CECAESMM086"
  },
  "3112": {
    "name": "CAJA-RURAL-SANJOSEBURRIANA",
    "bic": "BCOEESMM112"
  },
  "3111": {
    "name": "CAJA-RURAL-LAVALLSISIDRO",
    "bic": "BCOEESMM111"
  },
  "2085": {
    "name": "IBERCAJA-BANCO",
    "bic": "CAZRES2ZXXX"
  },
  "0156": {
    "name": "ROYAL-BANK-SCOTLAND",
    "bic": "ABNAESMMXXX"
  },
  "1473": {
    "name": "BANQUE-PREIVEE EDMOND",
    "bic": "PRIBESMXXXX"
  },
  "0154": {
    "name": "CREDIT-AGRICOLE-INVETBANK",
    "bic": "BSUIESMMXXX"
  },
  "0155": {
    "name": "BANCO-DO-BRASIL",
    "bic": "BRASESMMXXX"
  },
  "0152": {
    "name": "BARCLAYS-BANK",
    "bic": "BPLCESMMXXX"
  },
  "1474": {
    "name": "CITIBANK-INTERNACIONAL",
    "bic": "CITIESMXXXX"
  },
  "0151": {
    "name": "JPMORGAN",
    "bic": "CHASESM3XXX"
  },
  "0094": {
    "name": "RBC-INVESTOR",
    "bic": "BVALESMMXXX"
  },
  "0159": {
    "name": "COMMERZBANK",
    "bic": "COBAESMXXXX"
  }
}


class BBAN(object):
    """
        Basic Bank Account Number

        The Basic Bank Account Number (BBAN) format is decided by the national
        central bank or designated payment authority of each country. There is
        no consistency between the formats adopted.
    """

    @staticmethod
    def generate(bank="1465", branch="0000", account=None):
        if account is None:
            number = str(random.randrange(9999999999))
            account = number.zfill(10)
            first_cd = BBAN._first_check_digit(bank, branch)
            second_cd = BBAN._second_check_digit(account)
        return BBAN(bank + branch + first_cd + second_cd + account)

    @staticmethod
    def validate(number):

        if len(number) != 20:
            msg = "Spanish BBAN always contains exactly 20 chars, current: %i (%s)" % (len(number), number)
            raise BBANInvalidLength(msg)

        bank = number[0:4]
        branch = number[4:8]
        first_check_digit = number[8]
        second_check_digit = number[9]
        account = number[10:]

        if not bank in BANKS:
            raise BBANInvalidBankCode("Unknown bank code: %s" % (bank))

        real_first_check_digit = BBAN._first_check_digit(bank, branch)
        if first_check_digit != real_first_check_digit:
            msg = "The bank/branch check digit is incorrect: %s (expected: %s)" % (first_check_digit, real_first_check_digit)
            raise BBANInvalidBankBranchCheckDigit(msg)

        real_second_check_digit = BBAN._second_check_digit(account)
        if second_check_digit != real_second_check_digit:
            msg = "The account check digit is incorrect: %s (expected: %s)" % (second_check_digit, real_second_check_digit)
            raise BBANInvalidAccountCheckDigit(msg)

        return number

    @staticmethod
    def _first_check_digit(bank, branch):
        """
            The first digit is obtained by the following algorithm:
            1. Concatenate the digits of both the bank code and the branch code.
            2. Multiply each digit respectively by: 4, 8, 5, 10, 9, 7, 3 6
            3. Sum all the results into a single integer.
            4. Obtain the modulus 11 (remainder of the division by 11) of the
               integer obtained in 3.
            5. Subtract the remainder from 11 (11 is a magic number).
               Note: if the result of the subtraction is 10, it should be converted to "1".
               If the result of the subtraction is 11, it should be converted to "0".
        """
        #1
        concat = map(int, list(bank + branch))
        #2
        multi_seq = [4, 8, 5, 10, 9, 7, 3, 6]
        multi_result = [x*y for x, y in zip(concat, multi_seq)]
        #3
        multi_sum = sum(multi_result)
        #4
        remainder = multi_sum % 11
        #5
        digit = 11 - remainder
        if digit == 10:
            digit = 1
        elif digit == 11:
            digit = 0
        return str(digit)


    @staticmethod
    def _second_check_digit(account):
        """
            The first digit is obtained by the following algorithm:
            1. Concatenate the digits of the account number.
            2. Multiply each digit respectively by: 1, 2, 4, 8, 5, 10, 9, 7, 3, 6
            3. Sum all the results into a single integer.
            4. Obtain the modulus 11 (remainder of the division by 11) of the
               integer obtained in 3.
            5. Subtract the remainder from 11 (11 is a magic number).
               Note: if the result of the subtraction is 10, it should be converted to "1".
               If the result of the subtraction is 11, it should be converted to "0".
        """
        #1
        concat = map(int, list(account))
        #2
        multi_seq = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        multi_result = [x*y for x, y in zip(concat, multi_seq)]
        #3
        multi_sum = sum(multi_result)
        #4
        remainder = multi_sum % 11
        #5
        digit = 11 - remainder
        if digit == 10:
            digit = 1
        elif digit == 11:
            digit = 0

        return str(digit)

    def __init__(self, number):
        BBAN.validate(number)
        self.bank = number[0:4]
        self.branch = number[4:8]
        self.account = number[10:]

    @property
    def check_digit(self):
        """
            Calculate both check digits for a bank account.

            Assuming the BBAN is
                bank code = 1465
                branch code = 0000
                check digit = ?? <- This is what we need.
                account number = 1234567890

            See: https://csharp.com.es/cuenta-corriente-dc-iban-y-numero-de-tarjeta/

            _first_check_digit and _second_check_digit contain the algorithm
            details.
        """
        return BBAN._first_check_digit(self.bank, self.branch) + BBAN._second_check_digit(self.account)

    @property
    def number(self):
        return BBAN.validate(self.bank + self.branch + self.check_digit + self.account)

    def __repr__(self):
        return " ".join([self.bank, self.branch, self.check_digit, self.account])


class IBAN(object):

    @staticmethod
    def generate(bank="1465", branch="0000", account=None):
        bban = BBAN.generate(bank, branch, account).number
        country = "ES"
        check_digit = IBAN._calc_check_digit(country + "00" + bban)
        return IBAN(country + check_digit + bban)

    @staticmethod
    def validate(number):
        if len(number) != 24:
            msg = "Spanish IBAN always contains exactly 24 chars, current: %i" % len(number)
            raise IBANInvalidLength(msg)

        country = number[0:2]
        check_digit = number[2:4]
        bank = number[4:8]

        if country.upper() != "ES":
            raise IBANInvalidCountry("This IBAN should be only for ES (Spain) accounts.")

        real_check_digit = IBAN._calc_check_digit(number)
        if check_digit != real_check_digit:
            raise IBANInvalidCheckDigit("The check digit is incorrect: %s (expected: %s)" % (check_digit, real_check_digit))

        if not bank in BANKS:
            raise IBANInvalidBankCode("Unknown bank code: %s" % (bank))

        return number

    @staticmethod
    def _calc_check_digit(number):
        """
            Example, we use the bank code 10010010 of Postbank in Berlin
            (BIC: PBNKDEFFXXX) and the account number 987654321.

            1. The bank code and account number are merged to form the
                so-called BBAN. In our example, the BBAN is
                "1001 0010 0987 6543 21".
            2. Now the country code and the check digit set to 00 are placed in
                front of the BBAN. Thereby we get the IBAN
                "DE00 1001 0010 0987 6543 21", but still with empty check digit.
            3. Next, the IBAN is changed so that the country code and check
               digit are set to the end.
            4. Now all letters must be replaced by numbers. For A = 10, B = 11
                etc. up to Z = 35. In our case DE becomes the number 13 14.
                After replacing the letters with the numbers, we get the number
                sequence 100100100987654321131400
            5. This number is divided by 97 (Modulo 97 method) and the integer
                remainder of 98 (*98 is a magic number*) is subtracted.
                If the result is a single digit number, pad it with a leading 0
                to make a two-digit number.
        """

        #1
        bban = number[4:8]
        #2
        country = number[0:2] + "00"
        #3
        bban += country
        #4
        alphabet_seq = list(string.ascii_uppercase)
        new_number = ""
        for number in bban:
            if number.isalpha():
                number = str(alphabet_seq.index(number) + 10)
            new_number += number
        #5
        return str(98 - int(new_number) % 97).zfill(2)

    def __init__(self, number=None):
        IBAN.validate(number)
        self.country = number[0:2]
        self.bban = BBAN(number[4:])

    @property
    def check_digit(self):
        return IBAN._calc_check_digit(self.country + "00" + self.bban.number)

    @property
    def number(self):
        return IBAN.validate(self.country + self.check_digit + self.bban.number)

    def __repr__(self):
        return " ".join([self.country + self.check_digit, self.bban.__repr__()])


class Bank(object):

    def __init__(self, code, branch="000"):
        self.country = "ES"
        self.code = code
        self.branch = branch
        self.name = BANKS[code]["name"]
        self.bic = BANKS[code]["bic"] # BIC/ISO 9362


def random_bank():
    entity = random.choice(BANKS.keys())

if __name__ == "__main__":
    print IBAN.generate("0238")

