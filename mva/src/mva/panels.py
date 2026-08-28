"""Gene panels for the MVA hackathon Track 1 candidate search.

Panels are deliberately broad. The prior is biallelic BUB1B, but the search must
be able to refute it, so the differentials get equal treatment in the region scan.
"""

# --- Mosaic variegated aneuploidy itself, and the machinery it breaks.
MVA_CORE = ["BUB1B", "CEP57", "TRIP13", "CENPE"]

SPINDLE_ASSEMBLY_CHECKPOINT = [
    "BUB1", "BUB3", "MAD1L1", "MAD2L1", "MAD2L2", "TTK", "AURKA", "AURKB",
    "CDC20", "ZW10", "ZWILCH", "ZWINT", "KNTC1", "ESPL1", "PTTG1", "PLK1",
    "NDC80", "NUF2", "SPC24", "SPC25", "CENPA", "CENPC", "CENPE", "CENPF",
    "ANAPC1", "ANAPC2", "CDC27", "SGO1", "SKA1", "SKA2", "SKA3", "RZZ",
]

# --- Chromosomal instability / cohesinopathy differentials.
CHROMOSOMAL_INSTABILITY = [
    "NIPBL", "SMC1A", "SMC3", "RAD21", "HDAC8", "ESCO2", "PDS5B", "STAG2",
    "BLM", "NBN", "MRE11", "RAD50", "ATM", "ATR", "RECQL4", "WRN",
    "FANCA", "FANCB", "FANCC", "FANCD2", "FANCE", "FANCF", "FANCG", "FANCI",
    "FANCL", "FANCM", "BRCA1", "BRCA2", "PALB2", "BRIP1", "RAD51C", "SLX4",
]

# --- Rhabdomyosarcoma and general childhood cancer predisposition.
CANCER_PREDISPOSITION = [
    "TP53", "DICER1", "HRAS", "KRAS", "NRAS", "PTPN11", "SOS1", "RAF1",
    "NF1", "RB1", "FBXW7", "MYOD1", "TSC1", "TSC2", "WT1", "CDKN1C",
    "APC", "PTCH1", "SUFU", "SMARCB1", "SMARCA4", "CDKN2A", "MSH2", "MLH1",
    "MSH6", "PMS2", "POLE", "POLD1", "GPC3", "NSD1", "EZH2",
]

# --- Nephrocalcinosis: probably prematurity-related here, but it must be
#     excluded rather than assumed away.
NEPHROCALCINOSIS = [
    "SLC34A1", "SLC34A3", "CLDN16", "CLDN19", "CYP24A1", "ATP6V0A4",
    "ATP6V1B1", "SLC4A1", "CASR", "VDR", "AGXT", "HOGA1", "GRHPR",
    "SLC12A1", "KCNJ1", "BSND", "CLCNKB", "SLC9A3R1", "FAM20A", "CLCN5",
    "OCRL", "SLC7A9", "SLC3A1", "ADCY10",
]

PANELS = {
    "mva_core": MVA_CORE,
    "sac": SPINDLE_ASSEMBLY_CHECKPOINT,
    "cin": CHROMOSOMAL_INSTABILITY,
    "cancer_predisposition": CANCER_PREDISPOSITION,
    "nephrocalcinosis": NEPHROCALCINOSIS,
}

ALL_GENES = sorted({g for genes in PANELS.values() for g in genes})

# HPO terms transcribed from Challenge_Clinical_Phenotype_1.docx.
HPO_TERMS = {
    "HP:0002859": "Rhabdomyosarcoma",
    "HP:0000121": "Nephrocalcinosis",
    "HP:0004322": "Short stature",
    "HP:0001508": "Failure to thrive",
    "HP:0003202": "Skeletal muscle atrophy",
    "HP:0001622": "Premature birth",
    "HP:0001518": "Small for gestational age",
    "HP:0200067": "Recurrent spontaneous abortion",
}
