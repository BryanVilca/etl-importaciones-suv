import streamlit as st
import pandas as pd
import re
import io

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="ETL Importaciones SUV · Astara",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# ASTARA BRAND CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --astara-black:   #1E1932;
    --astara-dark:    #160F28;
    --astara-card:    #261D3E;
    --astara-border:  #3A2F5A;
    --astara-lime:    #F0B74D;
    --astara-lime-dim:#C9912A;
    --astara-white:   #FFFFFF;
    --astara-muted:   #9B8FBB;
    --astara-gray:    #D4C9F0;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--astara-black) !important;
    color: var(--astara-white) !important;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background-color: var(--astara-dark) !important;
    border-right: 1px solid var(--astara-border) !important;
}
[data-testid="stSidebar"] * { color: var(--astara-white) !important; }

.astara-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid var(--astara-border);
    margin-bottom: 2rem;
}
.astara-logo-box { display: none; }
.astara-title {
    font-size: 1.65rem; font-weight: 800;
    letter-spacing: -0.03em; color: var(--astara-white);
    line-height: 1.1; margin: 0;
}
.astara-title span { color: var(--astara-lime); }
.astara-header img { filter: brightness(0) invert(1); }
.astara-subtitle {
    font-size: 0.72rem; color: var(--astara-muted);
    margin: 4px 0 0; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
}

.sidebar-label {
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--astara-lime) !important;
    margin: 1.4rem 0 0.4rem;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin: 1.5rem 0 2rem;
}
.metric-card {
    background: var(--astara-card);
    border: 1px solid var(--astara-border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: var(--astara-lime);
    border-radius: 12px 12px 0 0;
}
.metric-label {
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--astara-muted); margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem; font-weight: 800;
    letter-spacing: -0.03em; color: var(--astara-white); line-height: 1;
}
.metric-value span { color: var(--astara-lime); }

.section-title {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--astara-muted); margin: 2rem 0 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: var(--astara-border);
}

.astara-info {
    background: rgba(240,183,77,0.06);
    border: 1px solid rgba(240,183,77,0.25);
    border-radius: 10px; padding: 1.2rem 1.4rem;
    margin: 1rem 0; font-size: 0.9rem; color: var(--astara-gray);
}
.astara-info strong { color: var(--astara-lime); }

.astara-success {
    background: rgba(240,183,77,0.08);
    border: 1px solid var(--astara-lime);
    border-radius: 10px; padding: 1rem 1.4rem;
    margin: 1rem 0; font-size: 0.9rem; color: var(--astara-white);
    display: flex; align-items: center; gap: 0.6rem;
}

.astara-warning {
    background: rgba(255,180,0,0.07);
    border: 1px solid rgba(255,180,0,0.3);
    border-radius: 10px; padding: 0.8rem 1.2rem;
    font-size: 0.85rem; color: #FFC107; margin: 0.5rem 0;
}

.steps-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin: 1.5rem 0;
}
.step-card {
    background: var(--astara-card);
    border: 1px solid var(--astara-border);
    border-radius: 12px; padding: 1.4rem;
}
.step-number {
    font-size: 2.2rem; font-weight: 800;
    color: var(--astara-lime); line-height: 1;
    margin-bottom: 0.6rem; opacity: 0.45;
}
.step-text { font-size: 0.88rem; color: var(--astara-gray); line-height: 1.5; }
.step-text strong {
    color: var(--astara-white); display: block;
    margin-bottom: 0.25rem; font-size: 0.95rem;
}

.stButton > button {
    background: var(--astara-lime) !important;
    color: var(--astara-black) !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 700 !important; font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--astara-lime-dim) !important;
    box-shadow: 0 4px 20px rgba(240,183,77,0.25) !important;
}

.stDownloadButton > button {
    background: var(--astara-lime) !important;
    color: var(--astara-black) !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 800 !important; font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: var(--astara-lime-dim) !important;
    box-shadow: 0 6px 28px rgba(240,183,77,0.3) !important;
}

[data-testid="stFileUploader"] {
    background: var(--astara-card) !important;
    border: 1.5px dashed var(--astara-border) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--astara-lime) !important; }

[data-testid="stCheckbox"] label { color: var(--astara-gray) !important; font-size: 0.84rem !important; }
[data-testid="stCheckbox"] label:hover { color: var(--astara-white) !important; }

[data-testid="stMultiSelect"] > div > div {
    background: var(--astara-card) !important;
    border-color: var(--astara-border) !important;
    border-radius: 8px !important;
}
[data-baseweb="tag"] {
    background: rgba(240,183,77,0.15) !important;
    color: var(--astara-lime) !important;
    border-radius: 4px !important;
}

[data-testid="stExpander"] {
    background: var(--astara-card) !important;
    border: 1px solid var(--astara-border) !important;
    border-radius: 10px !important;
}

hr { border-color: var(--astara-border) !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="collapsedControl"] { visibility: visible !important; display: flex !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--astara-dark); }
::-webkit-scrollbar-thumb { background: var(--astara-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--astara-lime); }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MARCAS CONFIG
# ──────────────────────────────────────────────
MARCAS_CONFIG = {
    "KIA":        "KIA IMPORT PERU S.A.C.",
    "DFSK":       "INCHCAPE AUTOMOTRIZ PERU S.A.",
    "HYUNDAI":    "AUTOMOTORES GILDEMEISTER PERU S.A.C.",
    "GEELY":      "MOTOR MUNDO S.A.C.",
    "SUBARU":     "INCHCAPE AUTOMOTRIZ PERU S.A.",
    "CHANGAN":    "DERCO PERU S.A.",
    "NISSAN":     "NISSAN PERU S.A.C.",
    "VOLKSWAGEN": "EURO MOTORS S.A.",
    "JAC":        "DERCO PERU S.A.",
    "CHEVROLET":  "GENERAL MOTORS PERU S A",
    "HONDA":      "HONDA DEL PERU S.A",
    "MAZDA":      "DERCO PERU S.A.",
    "SUZUKI":     "DERCO PERU S.A.",
    "GREAT WALL": "DERCO PERU S.A.",
    "MITSUBISHI": "MC AUTOS DEL PERU S.A.C.",
    "RENAULT":    "DERCO PERU S.A.",
    "HAVAL":      "DERCO PERU S.A.",
    "JETOUR":     "ALTOS ANDES S.A.C",
    "PEUGEOT":    "AUTOMOTORES FRANCIA PERÚ S.A.C.",
    "JEEP":       "DIVEIMPORT S.A.",
    "BYD":        "MOTORYSA PERU S.A.C.",
    "SWM":        "AMBACAR S.A.C.",
    "AUDI":       "EURO MOTORS S.A.",
    "BMW":        "INCHCAPE MOTORS PERU SA",
    "DONGFENG":   "DONGFENG MOTOR PERU S.A.C.",
    "JAECOO":     "CHERY OMODA&JAECOO MOTOR, SUCURSAL DEL PERU",
    "OMODA":      "CHERY OMODA&JAECOO MOTOR, SUCURSAL DEL PERU",
}

# ──────────────────────────────────────────────
# PARSE FUNCTIONS
# ──────────────────────────────────────────────

def parse_changan(text):
    result = {}
    m = re.search(r"MODELO:\s*([^,]+)", text)
    result["modelo"] = m.group(1).strip() if m else None
    m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    m = re.search(r"VERSION:\s*([^,]+)", text)
    result["version"] = m.group(1).strip() if m else None
    return result

def parse_geely(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"Modelo:\s*([^,]+)", text)
    modelo = m.group(1).strip() if m else None
    if modelo:
        modelo = re.sub(r"\bNEW\b", "", modelo)
        modelo = re.sub(r"\s+", " ", modelo).strip()
    result["modelo"] = modelo
    m = re.search(r"VE:\s*([^,]+)", text)
    version = m.group(1).strip() if m else None
    if version and modelo:
        version = version.replace(modelo, "").strip()
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"Año Mod\.\s*:\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_haval(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text)
    result["modelo"] = m.group(1).strip() if m else None
    m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    m = re.search(r"VERSION:\s*([^,]+)", text)
    version = m.group(1).strip() if m else None
    if version:
        version = re.sub(r"\bCC[0-9A-Z_]*\b", "", version)
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    return result

def parse_omoda_desc1(text):
    result = {"modelo": None, "version": None}
    if not isinstance(text, str): return result
    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 5:
        result["modelo"] = parts[3].replace("OMODA", "").strip()
        result["version"] = re.sub(r"\(.*?\)", "", parts[4]).strip()
    return result

def parse_omoda_desc3(text):
    if not isinstance(text, str): return None
    m = re.search(r"Año\s*Mod[:\.]?\s*(\d{4})", text)
    return m.group(1) if m else None

def parse_jaecoo_desc1(text):
    result = {"modelo": None, "version": None}
    if not isinstance(text, str): return result
    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 5:
        result["modelo"] = parts[3].strip()
        result["version"] = re.sub(r"Año Fab\..*", "", parts[4]).strip()
    return result

def parse_jaecoo_desc3(text):
    if not isinstance(text, str): return None
    m = re.search(r"Año\s*Mod[:\.]?\s*(\d{4})", text)
    return m.group(1) if m else None

def parse_jetour(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    text = text.strip()
    if "VE:" in text and "AÑO MOD" in text:
        m = re.search(r"MODELO:\s*([^,]+)", text)
        result["modelo"] = m.group(1).strip() if m else None
        m = re.search(r"VE:\s*([^,]+)", text)
        version = m.group(1).strip() if m else None
        if version:
            version = re.sub(r"\s*,?\s*[A-Z0-9]{5,}$", "", version)
            version = re.sub(r"\s+", " ", version).strip()
        result["version"] = version
        m = re.search(r"AÑO\s*MOD[:\.]?\s*(\d{4})", text, re.IGNORECASE)
        result["anio_modelo"] = m.group(1) if m else None
    else:
        m = re.search(r"MODELO:\s*([^,]+)", text)
        result["modelo"] = m.group(1).strip() if m else None
        m = re.search(r"VERSION:\s*([^,]+)", text)
        version = m.group(1).strip() if m else None
        if version:
            version = re.sub(r"\s*,?\s*[A-Z0-9]{5,}$", "", version)
            version = re.sub(r"\s+", " ", version).strip()
        result["version"] = version
        m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
        result["anio_modelo"] = m.group(1) if m else None
    return result

def _parse_version_anio(text, version_key="VERSION:"):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    modelo = m.group(1).strip() if m else None
    if not modelo:
        partes = [p.strip() for p in text.split(";")]
        if len(partes) >= 3: modelo = partes[-1]
    if modelo: modelo = re.sub(r"\s+", " ", modelo).strip()
    result["modelo"] = modelo
    key_pat = version_key.replace(":", ":\\s*")
    m = re.search(key_pat + r"([^,]+)", text, re.IGNORECASE)
    version = m.group(1).strip() if m else None
    if version:
        version = re.sub(r"\bNEW\b", "", version, flags=re.IGNORECASE)
        if modelo:
            version = re.sub(rf"^{re.escape(modelo)}\s*", "", version, flags=re.IGNORECASE)
        version = re.sub(r"\s*,?\s*[A-Z0-9\._-]{6,}$", "", version)
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_jac(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text)
    result["modelo"] = m.group(1).strip() if m else None
    m = re.search(r"VERSION:\s*([^,]+)", text)
    version = m.group(1).strip() if m else None
    if version:
        version = re.sub(r"\s*,?\s*[A-Z0-9\._-]{6,}$", "", version)
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_hyundai(text):    return _parse_version_anio(text, "VERSION:")
def parse_volkswagen(text): return _parse_version_anio(text, "VERSION:")
def parse_suzuki(text):     return _parse_version_anio(text, "VERSION:")
def parse_jeep(text):       return _parse_version_anio(text, "VERSION:")
def parse_audi(text):       return _parse_version_anio(text, "VERSION:")
def parse_greatwall(text):  return _parse_version_anio(text, "VERSION:")
def parse_dfsk(text):       return _parse_version_anio(text, "VERSION:")
def parse_bmw(text):        return _parse_version_anio(text, "VERSION:")
def parse_subaru(text):     return _parse_version_anio(text, "VERSION:")
def parse_mazda(text):      return _parse_version_anio(text, "VERSION:")
def parse_byd(text):        return _parse_version_anio(text, "VERSION:")

def parse_renault(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    modelo = m.group(1).strip() if m else None
    if not modelo:
        partes = [p.strip() for p in text.split(";")]
        if len(partes) >= 3: modelo = partes[-1]
    if modelo: modelo = re.sub(r"\s+", " ", modelo).strip()
    result["modelo"] = modelo
    m = re.search(r"VERSION:\s*([^,]+)", text, re.IGNORECASE)
    version = m.group(1).strip() if m else None
    if version:
        version = re.sub(r"\bNEW\b", "", version, flags=re.IGNORECASE)
        if modelo:
            version = re.sub(rf"^{re.escape(modelo)}\s*", "", version, flags=re.IGNORECASE)
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"Año\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def _parse_ve_aniomed(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    modelo = m.group(1).strip() if m else None
    if modelo: modelo = re.sub(r"\s+", " ", modelo).strip()
    result["modelo"] = modelo
    m = re.search(r"VE:\s*([^,]+)", text, re.IGNORECASE)
    version = m.group(1).strip() if m else None
    if version and modelo:
        version = re.sub(re.escape(modelo), "", version, flags=re.IGNORECASE).strip()
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"AÑO MOD:\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_dongfeng(text):  return _parse_ve_aniomed(text)
def parse_swm(text):       return _parse_ve_aniomed(text)
def parse_honda(text):     return _parse_ve_aniomed(text)
def parse_chevrolet(text): return _parse_ve_aniomed(text)

def _parse_split_format(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    if not m:
        parts = [p.strip() for p in text.split(",")]
        modelo = parts[2] if len(parts) >= 3 else None
    else:
        modelo = m.group(1).strip()
    result["modelo"] = modelo
    m = re.search(r"VE:\s*([^,]+)", text, re.IGNORECASE)
    if m:
        version = m.group(1).strip()
    else:
        parts = [p.strip() for p in text.split(",")]
        version = parts[3] if len(parts) >= 4 else None
    if version:
        version = re.sub(r"\s+", " ", version).strip()
        version = re.sub(r",\s*[A-Z0-9\-\.]+$", "", version)
    result["version"] = version
    m = re.search(r"AÑO\s*:?\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_peugeot(text):    return _parse_split_format(text)
def parse_mitsubishi(text): return _parse_split_format(text)

def parse_kia(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str): return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    if not m:
        m = re.search(r"M1\s*,?\s*KIA\s*,\s*([^,]+)", text, re.IGNORECASE)
    modelo = m.group(1).strip() if m else None
    if modelo: modelo = re.sub(r"\s+", " ", modelo).strip()
    result["modelo"] = modelo
    m = re.search(r"VE:\s*([^,]+)", text, re.IGNORECASE)
    if not m:
        m = re.search(r"M1\s*,?\s*KIA\s*,\s*[^,]+\s*,\s*([^,]+)", text, re.IGNORECASE)
    version = m.group(1).strip() if m else None
    if version: version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"AÑO MOD:\s*(\d{4})", text, re.IGNORECASE)
    if not m: m = re.search(r"AÑO:\s*(\d{4})", text, re.IGNORECASE)
    result["anio_modelo"] = m.group(1) if m else None
    return result

def parse_nissan_desc1(text):
    result = {"modelo": None, "version": None}
    if not isinstance(text, str): return result
    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 5:
        result["modelo"] = parts[3].replace("NISSAN", "").strip()
        result["version"] = re.sub(r"\(.*?\)", "", parts[4]).strip()
    return result

def parse_nissan_desc3(text):
    if not isinstance(text, str): return None
    m = re.search(r"Año\s*Mod[:\.]?\s*(\d{4})", text)
    return m.group(1) if m else None

PARSE_FN = {
    "CHANGAN": parse_changan, "GEELY": parse_geely, "HAVAL": parse_haval,
    "JETOUR": parse_jetour, "JAC": parse_jac, "HYUNDAI": parse_hyundai,
    "VOLKSWAGEN": parse_volkswagen, "SUZUKI": parse_suzuki, "HONDA": parse_honda,
    "RENAULT": parse_renault, "DONGFENG": parse_dongfeng, "DFSK": parse_dfsk,
    "SWM": parse_swm, "JEEP": parse_jeep, "KIA": parse_kia, "AUDI": parse_audi,
    "PEUGEOT": parse_peugeot, "GREAT WALL": parse_greatwall, "CHEVROLET": parse_chevrolet,
    "MITSUBISHI": parse_mitsubishi, "BMW": parse_bmw, "SUBARU": parse_subaru,
    "MAZDA": parse_mazda, "BYD": parse_byd,
}

# ──────────────────────────────────────────────
# PIPELINE
# ──────────────────────────────────────────────

def procesar_marca(df_final_limpio, marca):
    importador = MARCAS_CONFIG.get(marca)
    mask_marca = df_final_limpio["MARCA"].str.upper() == marca.upper()
    if importador:
        mask_imp = df_final_limpio["Importador"].str.upper() == importador.upper()
        df_marca = df_final_limpio[mask_marca & mask_imp].copy()
    else:
        df_marca = df_final_limpio[mask_marca].copy()
    if df_marca.empty: return df_marca

    if marca == "OMODA":
        p1 = df_marca["Descripcion1"].apply(parse_omoda_desc1).apply(pd.Series)
        anio = df_marca["Descripcion3"].apply(parse_omoda_desc3)
        df_marca[["modelo", "version"]] = p1[["modelo", "version"]].values
        df_marca["anio_modelo"] = anio.values
    elif marca == "JAECOO":
        p1 = df_marca["Descripcion1"].apply(parse_jaecoo_desc1).apply(pd.Series)
        anio = df_marca["Descripcion3"].apply(parse_jaecoo_desc3)
        df_marca[["modelo", "version"]] = p1[["modelo", "version"]].values
        df_marca["anio_modelo"] = anio.values
    elif marca == "NISSAN":
        p1 = df_marca["Descripcion1"].apply(parse_nissan_desc1).apply(pd.Series)
        anio = df_marca["Descripcion3"].apply(parse_nissan_desc3)
        df_marca[["modelo", "version"]] = p1[["modelo", "version"]].values
        df_marca["anio_modelo"] = anio.values
    else:
        fn = PARSE_FN.get(marca)
        if fn:
            parsed = df_marca["Descripcion1"].apply(fn).apply(pd.Series)
            for col in ["modelo", "version", "anio_modelo"]:
                if col in parsed.columns:
                    df_marca[col] = parsed[col].values
    return df_marca


def etl_pipeline(df_raw, marcas_seleccionadas):
    df_raw = df_raw.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df_raw["DESC_UP"] = df_raw["Descripcion Comercial"].astype(str).str.upper().str.strip()
    df_suv = df_raw[df_raw["DESC_UP"].str.contains(r"\bSUV\b", case=False, na=False)].copy()

    todas_marcas = list(MARCAS_CONFIG.keys())
    df_suv["MARCA"] = df_suv["DESC_UP"].apply(
        lambda x: next((m for m in todas_marcas if m in x), None)
    )
    df_suv["TRACCION"]    = df_suv["DESC_UP"].str.extract(r"(4X2|4X4|AWD|FWD|RWD|2WD)")
    df_suv["COMBUSTIBLE"] = df_suv["DESC_UP"].str.extract(
        r"(GASOLINA|DIESEL|HIBRIDO|ELECTRICO|HEV|EV|PHEV|MHEV|GNV|GLP|FLEXFUEL|BI GNV|BI-GNV)"
    )
    df_suv["TRANSMISION"] = df_suv["DESC_UP"].str.extract(
        r"(MT|CVT|A/T|AT|AMT|MANUAL|TRANSMISION VARIABLE CONTINUA|AUTOMATICA|MEC|AUT|DCT|SEMI AUTOMATICA)"
    )
    df_suv = df_suv.drop(columns=["DESC_UP"])
    df_suv["Fecha"] = pd.to_datetime(df_suv["Fecha"], errors="coerce")
    df_suv["anio"]  = df_suv["Fecha"].dt.year
    df_suv["mes"]   = df_suv["Fecha"].dt.month

    dfs, errores = [], []
    for marca in marcas_seleccionadas:
        try:
            df_m = procesar_marca(df_suv, marca)
            if not df_m.empty: dfs.append(df_m)
        except Exception as e:
            errores.append(f"{marca}: {e}")

    if not dfs: return pd.DataFrame(), errores

    df_import = pd.concat(dfs, ignore_index=True)
    columnas_numericas = ["U$ FOB Tot", "U$ Flete Tot", "U$ Seguro Tot"]
    cols_existentes = [c for c in columnas_numericas if c in df_import.columns]

    agg_dict = {}
    for col in cols_existentes:
        df_import[col] = pd.to_numeric(df_import[col], errors="coerce")
        agg_dict[f"{col}_avg"] = (col, "mean")
        agg_dict[f"{col}_min"] = (col, "min")
        agg_dict[f"{col}_max"] = (col, "max")

    group_cols = [c for c in ["anio", "mes", "MARCA", "modelo", "version"] if c in df_import.columns]
    if "DUA / DAM" in df_import.columns:
        agg_dict["cantidad_importaciones"] = ("DUA / DAM", "count")

    if agg_dict:
        df_final = df_import.groupby(group_cols, as_index=False).agg(**agg_dict)
    else:
        df_final = df_import[group_cols].drop_duplicates().copy()

    df_final["periodo"] = (
        df_final["anio"].astype(int).astype(str) + "-"
        + df_final["mes"].astype(int).astype(str).str.zfill(2)
    )
    df_final = df_final.sort_values(["anio", "mes", "MARCA", "modelo"]).reset_index(drop=True)
    return df_final, errores


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1rem; border-bottom:1px solid #3A2F5A; margin-bottom:0.5rem;">
        <img src="data:image/png;base64,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" style="height:26px; filter:brightness(0) invert(1); display:block; margin-bottom:6px;" />
        <div style="font-size:0.65rem;color:#9B8FBB;text-transform:uppercase;
                    letter-spacing:0.12em;">Intelligence · ETL SUV</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">📂 Dataset</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Dataset",
        type=["xlsx", "xls", "csv"],
        label_visibility="collapsed",
        help="Consolidado Veritrade en .xlsx o .csv"
    )

    st.markdown('<p class="sidebar-label">🏷️ Marcas a procesar</p>', unsafe_allow_html=True)

    todas_marcas_lista = sorted(MARCAS_CONFIG.keys())

    # Inicializar cada checkbox en session_state
    if "marcas_initialized" not in st.session_state:
        for m in todas_marcas_lista:
            st.session_state[f"cb_{m}"] = True
        st.session_state.marcas_initialized = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Todas", use_container_width=True):
            for m in todas_marcas_lista:
                st.session_state[f"cb_{m}"] = True
    with col2:
        if st.button("❌ Ninguna", use_container_width=True):
            for m in todas_marcas_lista:
                st.session_state[f"cb_{m}"] = False

    marcas_seleccionadas = []
    for marca in todas_marcas_lista:
        if st.checkbox(marca, key=f"cb_{marca}"):
            marcas_seleccionadas.append(marca)

    st.markdown("---")
    procesar_btn = st.button("🚀  Procesar ETL", type="primary", use_container_width=True)

    n_sel = len(marcas_seleccionadas)
    st.markdown(f"""
    <div style="text-align:center;margin-top:0.5rem;font-size:0.75rem;color:#555;">
        <span style="color:#F0B74D;font-weight:700">{n_sel}</span> / {len(todas_marcas_lista)} marcas seleccionadas
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:2rem;padding-top:1rem;border-top:1px solid #3A2F5A;
                font-size:0.65rem;color:#444;text-align:center;letter-spacing:0.06em;'>
        <img src='data:image/png;base64,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' style='height:16px; filter:brightness(0) invert(1); opacity:0.4; margin-bottom:4px; display:block; margin: 0 auto 4px;' /><br>
        <span style='color:#F0B74D'>●</span> Perú
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# MAIN HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div class="astara-header">
    <div>
        <img src="data:image/png;base64,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" style="height:40px; filter:brightness(0) invert(1); display:block; margin-bottom:6px;" />
        <p class="astara-subtitle">ETL Importaciones SUV &nbsp;·&nbsp; Veritrade &nbsp;·&nbsp; Mercado Peruano</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════
if uploaded_file is None:
    st.markdown("""
    <div class="astara-info">
        <strong>👈 Subí el dataset consolidado</strong> desde el panel lateral para comenzar el procesamiento ETL.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">Cómo funciona</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-number">01</div>
            <div class="step-text">
                <strong>Cargá el dataset</strong>
                Subí el consolidado Veritrade en formato .xlsx o .csv desde el sidebar.
            </div>
        </div>
        <div class="step-card">
            <div class="step-number">02</div>
            <div class="step-text">
                <strong>Seleccioná marcas</strong>
                Elegí una o todas las marcas que querés incluir en el procesamiento.
            </div>
        </div>
        <div class="step-card">
            <div class="step-number">03</div>
            <div class="step-text">
                <strong>Ejecutá el ETL</strong>
                La app filtra SUVs, aplica el parser específico de cada marca y consolida el resultado.
            </div>
        </div>
        <div class="step-card">
            <div class="step-number">04</div>
            <div class="step-text">
                <strong>Descargá el CSV</strong>
                Exportá el dataset limpio con MARCA, MODELO, VERSION, AÑO, FOB, FLETE y SEGURO.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">Marcas soportadas</p>', unsafe_allow_html=True)
    marcas_html = "".join([
        f'<span style="background:#261D3E;border:1px solid #3A2F5A;border-radius:6px;'
        f'padding:4px 14px;font-size:0.78rem;color:#AAA;margin:3px;display:inline-block;'
        f'letter-spacing:0.04em;font-weight:500;">{m}</span>'
        for m in sorted(MARCAS_CONFIG.keys())
    ])
    st.markdown(f'<div style="line-height:2.4">{marcas_html}</div>', unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════
# LEER ARCHIVO
# ══════════════════════════════════════════════
@st.cache_data(show_spinner="Leyendo archivo...")
def leer_archivo(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    buf = io.BytesIO(file_bytes)
    if file_name.endswith(".csv"):
        return pd.read_csv(buf, encoding="latin1", on_bad_lines="skip")
    return pd.read_excel(buf, engine="openpyxl", skiprows=5)

if uploaded_file is None:
    st.stop()

nombre_archivo = uploaded_file.name
df_raw = leer_archivo(uploaded_file.getvalue(), nombre_archivo)

with st.expander("🔍  Vista previa del dataset cargado"):
    st.markdown(f"""
    <div style='font-size:0.78rem;color:#666;margin-bottom:0.6rem;'>
        <span style='color:#F0B74D'>■</span>&nbsp;{df_raw.shape[0]:,} filas &nbsp;·&nbsp;
        <span style='color:#F0B74D'>■</span>&nbsp;{df_raw.shape[1]} columnas &nbsp;·&nbsp;
        <span style='color:#555'>{nombre_archivo}</span>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_raw.head(10), use_container_width=True)


# ══════════════════════════════════════════════
# PROCESAMIENTO
# ══════════════════════════════════════════════
if procesar_btn:
    if not marcas_seleccionadas:
        st.markdown('<div class="astara-warning">⚠️ Seleccioná al menos una marca para continuar.</div>', unsafe_allow_html=True)
        st.stop()

    with st.spinner("Ejecutando pipeline ETL..."):
        df_resultado, errores = etl_pipeline(df_raw.copy(), marcas_seleccionadas)

    if errores:
        with st.expander("⚠️  Advertencias"):
            for e in errores:
                st.markdown(f'<div class="astara-warning">{e}</div>', unsafe_allow_html=True)

    if df_resultado.empty:
        st.markdown('<div class="astara-warning">❌ No se generaron datos. Verificá la estructura del dataset.</div>', unsafe_allow_html=True)
        st.stop()

    # Success
    st.markdown(f"""
    <div class="astara-success">
        ✅&nbsp;&nbsp;<strong>ETL completado</strong> —
        {df_resultado.shape[0]:,} registros procesados para
        <strong style="color:#F0B74D">{len(marcas_seleccionadas)}</strong> marca(s).
    </div>
    """, unsafe_allow_html=True)

    # Métricas
    n_marcas   = df_resultado["MARCA"].nunique()   if "MARCA"   in df_resultado.columns else "—"
    n_modelos  = df_resultado["modelo"].nunique()  if "modelo"  in df_resultado.columns else "—"
    n_periodos = df_resultado["periodo"].nunique() if "periodo" in df_resultado.columns else "—"

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">Registros</div>
            <div class="metric-value">{df_resultado.shape[0]:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Marcas</div>
            <div class="metric-value"><span>{n_marcas}</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Modelos únicos</div>
            <div class="metric-value"><span>{n_modelos}</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Períodos</div>
            <div class="metric-value"><span>{n_periodos}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Explorar
    st.markdown('<p class="section-title">Explorar resultado</p>', unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        marcas_res = sorted(df_resultado["MARCA"].dropna().unique()) if "MARCA" in df_resultado.columns else []
        marca_filtro = st.multiselect("Marca", marcas_res, default=marcas_res)
    with col_f2:
        modelos_disp = sorted(
            df_resultado[df_resultado["MARCA"].isin(marca_filtro)]["modelo"].dropna().unique()
        ) if "modelo" in df_resultado.columns and marca_filtro else []
        modelo_filtro = st.multiselect("Modelo", modelos_disp)
    with col_f3:
        periodos_disp = sorted(df_resultado["periodo"].dropna().unique()) if "periodo" in df_resultado.columns else []
        periodo_filtro = st.multiselect("Período", periodos_disp)

    df_vista = df_resultado.copy()
    if marca_filtro:   df_vista = df_vista[df_vista["MARCA"].isin(marca_filtro)]
    if modelo_filtro:  df_vista = df_vista[df_vista["modelo"].isin(modelo_filtro)]
    if periodo_filtro: df_vista = df_vista[df_vista["periodo"].isin(periodo_filtro)]

    st.markdown(
        f'<div style="font-size:0.75rem;color:#444;margin-bottom:0.4rem;">'
        f'{len(df_vista):,} registros visibles</div>',
        unsafe_allow_html=True
    )
    st.dataframe(df_vista, use_container_width=True, height=420)

    # Descarga
    st.markdown('<p class="section-title">Exportar</p>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns([3, 1])

    with col_d1:
        buffer = io.BytesIO()
        df_resultado.to_csv(buffer, index=False, encoding="utf-8-sig")
        buffer.seek(0)
        st.download_button(
            label="⬇️  Descargar dataset limpio (.csv)",
            data=buffer,
            file_name="dataset_importaciones_limpio.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_d2:
        st.markdown(f"""
        <div style='background:#261D3E;border:1px solid #3A2F5A;border-radius:10px;
                    padding:0.9rem 1rem;font-size:0.78rem;color:#666;text-align:center;height:100%;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;'>
            <span>{df_resultado.shape[0]:,} filas</span>
            <span style='color:#F0B74D;font-weight:700;font-size:1rem'>{df_resultado.shape[1]} cols</span>
        </div>
        """, unsafe_allow_html=True)
