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
    justify-content: space-between;
    padding: 1.2rem 0 1.5rem;
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
    "FORD":       "FORD PERU S.R.L.",
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
    if not isinstance(text, str):
        return result

    text = text.strip()
    parts = [p.strip() for p in text.split(",")]

    # ── Formato: M1,MARCA:PEUGEOT,MODELO:xxx,VE:yyy,AÑO MOD:yyyy
    if re.search(r"MODELO:", text, re.IGNORECASE):
        m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
        modelo = m.group(1).strip() if m else None
        # Descartar códigos internos tipo SC1035SPCD5
        if modelo and re.match(r'^[A-Z0-9]{6,}$', modelo):
            modelo = None
        m = re.search(r"VE:\s*([^,]+)", text, re.IGNORECASE)
        version = m.group(1).strip() if m else None
        if version and version.upper() == "SIN VERSION":
            version = None
        # Si modelo es código interno, usar VE como modelo
        if not modelo and version:
            result["modelo"] = version
            result["version"] = None
        else:
            result["modelo"] = modelo
            result["version"] = version
        m = re.search(r"AÑO\s*MOD[:\s]*(\d{4})", text, re.IGNORECASE)
        if not m:
            m = re.search(r"AÑO\s*:?\s*(\d{4})", text, re.IGNORECASE)
        if not m:
            for p in reversed(parts):
                if re.match(r'^\d{4}$', p.strip()):
                    result["anio_modelo"] = p.strip()
                    break
        else:
            result["anio_modelo"] = m.group(1)
        return result

    # ── Formato: campo[2] contiene "VE:" embebido
    # Ej: M1,PEUGEOT,208 VE:R4,2025  /  M1,PEUGEOT,2008 VE:GT LINE...,version, AÑO:2026
    if len(parts) >= 3 and "VE:" in parts[2].upper():
        m = re.match(r"(.+?)\s+VE:\s*(.+)", parts[2], re.IGNORECASE)
        if m:
            result["modelo"] = m.group(1).strip()
            version = m.group(2).strip()
            result["version"] = None if version.upper() == "SIN VERSION" else version
        m = re.search(r"AÑO\s*:?\s*(\d{4})", text, re.IGNORECASE)
        if not m:
            for p in reversed(parts):
                if re.match(r'^\d{4}$', p.strip()):
                    result["anio_modelo"] = p.strip()
                    break
        else:
            result["anio_modelo"] = m.group(1)
        return result

    # ── Formato estándar: N1/M1,PEUGEOT,MODELO,VERSION, AÑO:yyyy
    result["modelo"] = parts[2] if len(parts) >= 3 else None
    version = parts[3] if len(parts) >= 4 else None
    if version:
        version = re.sub(r"\s*AÑO\s*:?\s*\d{4}", "", version, flags=re.IGNORECASE).strip()
        version = re.sub(r"\s+", " ", version).strip()
        version = version if version else None
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

def parse_ford(text):
    result = {"modelo": None, "version": None, "anio_modelo": None}
    if not isinstance(text, str):
        return result
    m = re.search(r"MODELO:\s*([^,]+)", text, re.IGNORECASE)
    result["modelo"] = m.group(1).strip() if m else None
    m = re.search(r"VE:\s*([^,]+)", text, re.IGNORECASE)
    version = m.group(1).strip() if m else None
    if version:
        version = re.sub(r"\s+", " ", version).strip()
    result["version"] = version
    m = re.search(r"AÑO\s*MOD[:\s]*(\d{4})", text, re.IGNORECASE)
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
    "MAZDA": parse_mazda, "BYD": parse_byd, "FORD": parse_ford,
}

# ──────────────────────────────────────────────
# PIPELINE
# ──────────────────────────────────────────────

def procesar_marca(df_final_limpio, marca):
    importador = MARCAS_CONFIG.get(marca)
    mask_marca = df_final_limpio["MARCA"].str.upper() == marca.upper()
    if importador:
        if "Importador" in df_final_limpio.columns:
            mask_imp = df_final_limpio["Importador"].str.upper() == importador.upper()
            df_marca = df_final_limpio[mask_marca & mask_imp].copy()
        else:
            df_marca = df_final_limpio[mask_marca].copy()
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
    df_raw = df_raw.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    # ── Normalizar nombres de columna a string (evita int columns tras concat)
    df_raw.columns = [str(c).strip() for c in df_raw.columns]

    # ── Detectar columna "Descripcion Comercial" con tolerancia a variantes
    col_desc = next(
        (c for c in df_raw.columns
         if "descripcion" in c.lower() and "comercial" in c.lower()),
        None
    )
    if col_desc is None:
        st.error(
            f"❌ No se encontró la columna 'Descripcion Comercial'. "
            f"Columnas disponibles: {list(df_raw.columns[:15])}"
        )
        st.stop()
    df_raw["DESC_UP"] = df_raw[col_desc].astype(str).str.upper().str.strip()
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
        <img src="data:image/png;base64,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" style="height:32px; display:block; margin-bottom:6px;" />
        <div style="font-size:0.65rem;color:#9B8FBB;text-transform:uppercase;
                    letter-spacing:0.12em;">Market View · Perú</div>
    </div>
    """, unsafe_allow_html=True)

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
        <p class="astara-title">Astara <span>Market View</span></p>
        <p class="astara-subtitle">Inteligencia Competitiva &nbsp;·&nbsp; Mercado Peruano</p>
    </div>
    <div>
        <img src="data:image/png;base64,/9j/4AAQSkZJRgABAQAASABIAAD/4QBMRXhpZgAATU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAyKADAAQAAAABAAAAyAAAAAD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgAyADIAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMAAQEBAQEBAgEBAgMCAgIDBAMDAwMEBgQEBAQEBgcGBgYGBgYHBwcHBwcHBwgICAgICAkJCQkJCwsLCwsLCwsLC//bAEMBAgICAwMDBQMDBQsIBggLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLC//dAAQADf/aAAwDAQACEQMRAD8A/wA/+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//0P8AP/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9H/AD/6KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP//S/wA/+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//0/8AP/or/QU/4gadA/6OZuP/AAkF/wDlrR/xA06B/wBHM3H/AISC/wDy1oA/z66K/wBBT/iBp0D/AKOZuP8AwkF/+WtH/EDToH/RzNx/4SC//LWgD/Pror/QU/4gadA/6OZuP/CQX/5a0f8AEDToH/RzNx/4SC//AC1oA/z66K/0FP8AiBp0D/o5m4/8JBf/AJa0f8QNOgf9HM3H/hIL/wDLWgD/AD66K/0FP+IGnQP+jmbj/wAJBf8A5a0f8QNOgf8ARzNx/wCEgv8A8taAP8+uiv8AQU/4gadA/wCjmbj/AMJBf/lrR/xA06B/0czcf+Egv/y1oA/z66K/0FP+IGnQP+jmbj/wkF/+WtH/ABA06B/0czcf+Egv/wAtaAP8+uiv9BT/AIgadA/6OZuP/CQX/wCWtH/EDToH/RzNx/4SC/8Ay1oA/wA+uiv9BT/iBp0D/o5m4/8ACQX/AOWtH/EDToH/AEczcf8AhIL/APLWgD/Pror/AEFP+IGnQP8Ao5m4/wDCQX/5a0f8QNOgf9HM3H/hIL/8taAP8+uiv9BT/iBp0D/o5m4/8JBf/lrR/wAQNOgf9HM3H/hIL/8ALWgD/Pror/QU/wCIGnQP+jmbj/wkF/8AlrR/xA06B/0czcf+Egv/AMtaAP8APror/QU/4gadA/6OZuP/AAkF/wDlrR/xA06B/wBHM3H/AISC/wDy1oA//9T+/iiiqeoahZaTYT6pqUqw29tG0ssjHCoiDLMfYAZNAGR4u8YeE/AHhu88ZeOtTtdG0jT4zNdXt7MtvbwxjqzyOQqj3Jr8mfF//Bf/AP4I9+CPEz+E9Y+OOkz3SOYzJp1nf6ja5Ayf9JtLaWAj3EmCeM5r+VHx/wCMf2tv+DnP/goTqfwW+Hmtz+FfgH4EuHn3oC1ra2Cu0Ud5LHlRcaheAEQoSViUkD5VkZ/6KPAH/BsL/wAEj/CPgtPDXibwdqvijUBHtfVr/WryK5L8ZYJaywQDnoPKIA9etdzoUqdlWbv2XQD9jf2ff2r/ANmn9q7w4/iz9m7x1ovjWwh2+c+k3cdw0JboJUU74z7OqmvoKv8AP+/4Kaf8Ef8A40/8ETtf0v8A4KP/APBM7xrrFv4d0C8hTVLW5dZbvSxM2xGlYKsd3YzMwhljljyrMud4YtH/AFP/ALI//BSm0/bI/wCCW9/+3R8OtPT/AISTSfD2rS6ho9uC/ka7pNu7yWyh+SruqvFk8xyISec1nVw6UVOm7xf4PzA9i/aw/wCCp3/BPv8AYe1tfC37T/xQ0vw3rLRrKdMRJ9Q1BY2GVZrWyinnVWHKlkAPbNfFn/ESp/wRW/6LJL/4THiD/wCVtfzE/wDBvj/wTy/Zl/4KxeO/i3+0L+3pe3nj3xFp9/bTS6XJqE9s91LqYlklvLiSB47hgXXam2RVBBzngV/Ub/xDi/8ABGL/AKIwn/g/1v8A+WFa1KWHpy5JuTflawH15+xl/wAFSP2FP+Cg2ua94b/ZE8cN4rvfDNvDdalE+lajpxhiuGZY2BvrW3D5ZGBCFiO+MjPxaf8Ag5U/4IqZO34zOw9V8M6+yn3BGmkEehHBr7d/Y8/4Ji/sN/sC65rniT9krwMvhK98SW8NrqMo1G/vjNFAzMi4vLicLhmJygUnvnAr45b/AINxv+CMJYkfBaJQTnamva0qj2AF+AB6AAAVivq/M781um3zuBj/APESp/wRW/6LJL/4THiD/wCVtKP+DlT/AIIqEgN8ZnUHu/hnX1Ue5J00AD1J4FfyWx/sAfshH/g5eP7Ah8HL/wAKjGqm1/sD7de48r/hHftuPtP2j7X/AMfP7zPndfl+58tf10r/AMG43/BGFWDH4LRMAc7X13WmU+xU35BHqCCD3roq0sNC1+bVX6DP22nngtYHubl1jjjUs7scKqjkkk8AAV+Vnxo/4Lhf8EofgD4gm8K/Ej42aH/aFs2yaDSkudZaNt23a/8AZ0NyFYHqDggcnjmv5y/+C2v7cf7VP/BQf9u20/4IvfsJ3hstOS9j07xHcQStAL+9CiadbqZQWSxsY/mmRAWd1YEOQiH9L/2aP+DV7/gmv8KfA1rpvx8s9U+KHiFoVF5fXV9c6Za+dj5jBb2UsTIuTwJJZTwMk81kqFOEVKs3r0W4j9iP2Y/+CjX7DP7ZU50/9mf4n6F4rv1Uu2nwT+Tfqo6sbWcRzge5jxX2rX8VP/BTX/g2Y8HfB/4dX/7U/wDwTA1XWdA8VeDVOrf8I8968rSxW2ZHbT7okXEVzGBujR3fzCuAysRn9Rf+Der/AIKseLf+Cjf7OOr+Cvjpcx3PxN+G721tqt0EWJ9Ss7lW+z3jRqFVZGaORJgihd67gF3AUqlCPJ7Sk7rr3QH6P+MP+Cm37D/gH9r3TP2DfFnjb7J8VtYaBLTRP7N1CRZGuYzNEDdpbNaKWQE4acY6HBIFN/aU/wCCof8AwT6/ZB1WTw9+0T8WdA8ParEdsmm+ebu/Q8fetbZZZxjIySmB3r+D/wD4L/eIfjH4X/4LuX+qfs9XV9ZeOXg8P2mhS6WcXwvry1S3iW3I5ErmTYhX5gxBUhgCP3X/AGKv+DUn9mPw14LsPGf7eesap488b6giXOpWFnevaabBM/zPF5seLmcjOGl81NxBIABFayw1GEIznJ6rbqM/qO+Cvxm+Gn7RHwn8P/HH4N6oNa8LeKbKPUNMvlikhE9vKMq3lzIkiE91dFYHggGvlv8AaX/4Kgf8E/f2PdWfw5+0Z8V9B8O6tGQH03zmu79M9C1rbLLOo9ygFfhb/wAF1P2+3/4JRfsyeAP+Ccn/AAT9gbwx4l8R6WLTTmtHluLvR9DifyENs8pdzcXEm+KOV2Z12uy/PtZfN/8Agnh/wax/BKL4caf8Wf8AgpHeal4t8ca9Et7d6Da3sltaWBmXd5U9xGRcXFwuR5rrIiBwVXeo3tnGhTUfaVG0nsurEfuj8Av+Cz//AAS6/ab1+Dwp8H/jNoVzqt0ypBZ6j5+j3EzvwFjj1CK2d2/2VBPtX6eV/Lr+19/waqfsE/FTwBfN+yaL/wCF/i6GJn092vrjUtMkmAJVLiO6eaYITgF4pAyDna5GD8j/APBvl/wUW/aZ+EX7Terf8Eb/ANuyWeTW9A+2WvhuW/kEt1aT6am+TT/NBIntzAjzWz5O1FwpMZQISoU5Rc6Lem6e4H9oVFFFcYBRRRQB/9X+/ivjn/gol/wkv/DAHxw/4Qzd/bH/AAgPiT7Ds3bvtH9nz+XjZ82d2MbefSvsaqeo6fZavp8+lalEs1tdRtFLG3KujghlPsQcU4uzTA/j2/4M7P8AhC/+GZPi5/Z23+3f+EksvtfTd9l+y/uPfG7zfbNf2K1/ni+N/C37WX/BsR/wUM1P4v8AgTQ5vFPwD8e3DwKiErbXenl2kjtJJMMLfULIE+U7DbKuSPlZ1T+jT4f/APBzl/wSL8YeDU8S+JvG2p+Fr8oGfStR0W+luQ3dQ9pDcQHnofNGfau/FUZzn7Wmrp9gP0N/4Kpr4Jb/AIJp/HsfEMKdK/4QLXy+7bnzRZy+Ts3ceZ52zy8/x7a/nU/4M79Zv9U/Zn+NXgfUmE2m2/iSwuVgbLR+ZeWhjlO08fMsEYPHIHOeMfDv/BVb/gsh8V/+CwnhrVf2MP8AgnZ4O1UeANMsbnxH4t1e+VYZ7uw0hDdN5ihmjtrSLyxId7mWeURoqqRtl+wf+DPDULbTPgJ8d9VuyRDb6xpMrkDJCrbTk8fSr9jKnhZc291oB1H7UX/Bsf8AGb4fftAXf7SH/BJf4uSfC+7v5JZTpFzeXenGy807nitL6yDyNbuQB9nmjIGMGRlwF8o/4Zn/AODtz4JqW8MfEiHxlbW4+VG1DTbwyY563sEcp6Y5Yda/Ui4/4Okv+CT1tcSWz6x4kLRsVJGjSYyDj+/VC7/4OoP+CUFtbPPDqXii4ZBkRx6MwZvYbpFX8yKFLE2tKF/VAfNH/BJ//gu1+0144/a/f/gm7/wU88KxeG/iJLNJZabqcdv9hka/iQy/Zru3yYiZowWgnhIR/lAVg4ev60q/z1/2d/Ffi7/gtx/wcHeH/wBsH4K+Fr7QvAHgDUNK1a9vrhQWis9DANv9odcxrPeTIESIMWEeSCQjEf6FFYYyEYyVlZtarswP4IIv+VyFv+w6f/UTr+9+v4IIv+VyFv8AsOn/ANROv736eN/5d/4UNn8Cn/BvyYpP+C+/7QMnxbCDxVjxoYxcZEo1M63F9o2553eX52f9nNf311/Db/wW3/Yj/am/4J4ft32n/BaL9hu0N5pkl7HqHiKCKJplsL9lEM7XUKFWexvk+WV1YFJHbJUsj1+nv7M//B03/wAE0viz4ItdR+PWoan8LvEAiX7XZXlhc6nbCXHzCGeximZ0z0Lxxn1FaYmnKty1aaurfcxH9Kpxjmv8+7/g258RaDpn/Bcb406D8L5SPCeqaH4pFlECdjWkGs2b2r4HBZYzhSc4DtjrX23/AMFF/wDg5L0D4++EZ/2Pf+CUOi614s8cePD/AGNDrxs3gMKXf7thY27gTSXDhtqSSLGsRO/DECvzQ/4Nffh74q+En/BZXxv8KfHcaw654Y8JeI9J1FEfzVW7stRsYZgHHDAOjAN361dGhKFGo56XWwH0r+2fp9nqf/B2p8ObW/jEsY1Tw5KFPTfDYmRD/wABZQR7iv70K/g7/bA/5W3Ph1/2EdA/9Nz1/eJWGM2p/wCFAfwGf8FV8N/wdHfCRfjECPD39o+BhY+cf3RsvtHGd/y+V9s87fj5fvd81/fnX8wn/Bx//wAEofiZ+2j8PvD/AO1l+y/ZvffEz4Z28kUlhbErd6jpSuZwttj71xbSl5Yo+rh3C5cqrfOv/BOz/g6b+BN58NtO+FP/AAUgt9Q8IeOdBjWxvNft7KW5sr8wjb508EKtcW9w2P3qLE6F8suwMI1upB1qUJU9baNAf2C1/n2/8FKvEGheFf8Ag6m+FerfDyXy76Txd4AtNUKHaPPvZra2mXKkfetZEDZ6kkEEZB/ZL9rz/g6k/YE+FXgO8T9k+S++Kni6eIrp0QsbnTdNSduFNxJdRwzFVJyViiJfGAy53V/H78KdI/aml/4LIfs/fFb9sa3ubfxt8SfiJ4K8XSi8URTtbalrMHks0Ix5KsqZjiwNke0YHStcHh5x5pTVtGB/rBUUUV5QBRRRQB//1v7+KK/gc/4jlfD3/Rs9x/4Vy/8Ayqo/4jlfD3/Rs9x/4Vy//KqgD+7zxn4J8G/Ebwzd+DPiBpNnrmkX6GO5sr+BLi3mQ9njkDKw+or8k/Fv/Bvp/wAEdfGviV/Fmr/BDTLe5d2cx6df6jp1rl8A4trS6htwOOFEYA7Ac1/Nf/xHK+Hv+jZ7j/wrl/8AlVR/xHK+Hv8Ao2e4/wDCuX/5VVcak4/C2gP7U/hL+x7+yx8B/hdqHwV+Dvw+0Hw54V1e3ktdQ0yyso44LyGVDG63AxmbejFWMhYsCc9TUP7O37G/7LH7JXhzVfCX7NXgLRvBem65Ks2oQaXbLCty6LsUyd2wpIAJwMn1NfxZf8Ryvh7/AKNnuP8Awrl/+VVH/Ecr4e/6NnuP/CuX/wCVVLnlrqB/VHcf8EVf+CT93cSXU/wC8HNJKxdj/Z6jJY5PA4p1r/wRW/4JPWdwl1F+z/4LZozkCTTUkU/VXypHsQRX8rX/ABHK+Hv+jZ7j/wAK5f8A5VUf8Ryvh7/o2e4/8K5f/lVVe2qfzP7wuf3N/Cr4OfCb4GeEovAXwX8M6X4U0SAlo7HSbSOzt1Y9TsiVVycDnGa9Ir+Bz/iOV8Pf9Gz3H/hXL/8AKqj/AIjlfD3/AEbPcf8AhXL/APKqobvqwP7Ox+w9+yEP2kf+GwB8OdC/4WgTu/4Sb7In9o7vs/2Xd5vXd9n/AHW7rs4zivqiv4HP+I5Xw9/0bPcf+Fcv/wAqqP8AiOV8Pf8ARs9x/wCFcv8A8qqHJvdgf3u3Fvb3lvJaXcayxSqUdHAZWVhggg8EEdRX5S/Gr/ghn/wSc/aB8RzeLviR8FNGGo3LF5ptImu9FMrk5LONOntgzE9SwJP41/L5/wARyvh7/o2e4/8ACuX/AOVVH/Ecr4e/6NnuP/CuX/5VU4zlH4XYD+xn9l7/AIJ5/sS/sXCSX9mH4aaJ4Ru5lKSX1tAZb6RG6q11MZLhl/2TIRXR/DD9iD9kP4K/GjXf2i/hN8OtC8P+OfE/2oarrdlaJFeXX22VZ7jfIOf3sqrJJj7zAE5Nfxh/8Ryvh7/o2e4/8K5f/lVR/wARyvh7/o2e4/8ACuX/AOVVDnJ3be4H9n/iL9iP9kfxb+0HY/tXeJvh5od98SNM8s2viKa1Vr+IwoY4ysnXKoSqnqBwK+pK/gc/4jlfD3/Rs9x/4Vy//Kqj/iOV8Pf9Gz3H/hXL/wDKqk5N7sD++OvgH9pv/glj/wAE9P2xdXfxJ+0X8J9D1/VpDmTUkjexv5P9+6tHhnYc9GcjPNfyNf8AEcr4e/6NnuP/AArl/wDlVR/xHK+Hv+jZ7j/wrl/+VVOMnF3i7Af1Y/s6f8Ebv+CY37KXiODxj8EPg7othrFqyvb39+0+r3UDr0aKbUJbl4290YGvon4h/sPfshfFn45aL+0v8SvhzoWt+PvDj2smma9d2iSXts9jIZbdkkPO6GQ74z1VuRggV/GL/wARyvh7/o2e4/8ACuX/AOVVH/Ecr4e/6NnuP/CuX/5VU3Um3dt3A/vjor+Bz/iOV8Pf9Gz3H/hXL/8AKqj/AIjlfD3/AEbPcf8AhXL/APKqoA/vjor+Bz/iOV8Pf9Gz3H/hXL/8qqP+I5Xw9/0bPcf+Fcv/AMqqAP/X/wA/+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//0P8AP/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9H/AD/6KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP//S/wA/+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//0/8AP/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9k=" style="height:48px; display:block;" />
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB STYLING
# ══════════════════════════════════════════════
st.markdown("""
<style>
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0px;
    border-bottom: 1px solid #3A2F5A;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #9B8FBB !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.4rem !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #F0B74D !important;
    border-bottom: 2px solid #F0B74D !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: #D4C9F0 !important;
    background: rgba(240,183,77,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📦  Importaciones SUV", "💲  Precios Nyvus", "🚘  Inmatriculaciones", "🔗  Catálogo Maestro"])

with tab1:

    col_up, col_btn = st.columns([3, 1])
    with col_up:
        uploaded_files = st.file_uploader(
            "📂 Dataset(s) Veritrade — podés subir varios a la vez (.xlsx o .csv)",
            type=["xlsx", "xls", "csv"],
            key="uploader_importaciones",
            accept_multiple_files=True,
            help="Seleccioná uno o varios archivos Veritrade. Se consolidan automáticamente."
        )
        uploaded_file = uploaded_files[0] if uploaded_files and len(uploaded_files) == 1 else None
    with col_btn:
        st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
        procesar_btn = st.button("🚀 Procesar ETL", type="primary", use_container_width=True, key="btn_etl")
        st.markdown("</div>", unsafe_allow_html=True)

    if not uploaded_files:
        st.markdown("""
        <div class="astara-info">
            <strong>⬆️ Subí el dataset consolidado Veritrade</strong> para comenzar el procesamiento ETL.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="section-title">Cómo funciona</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="steps-grid">
            <div class="step-card"><div class="step-number">01</div><div class="step-text"><strong>Cargá el dataset</strong>Subí el consolidado Veritrade en .xlsx o .csv.</div></div>
            <div class="step-card"><div class="step-number">02</div><div class="step-text"><strong>Seleccioná marcas</strong>Elegí las marcas desde el panel lateral.</div></div>
            <div class="step-card"><div class="step-number">03</div><div class="step-text"><strong>Ejecutá el ETL</strong>La app filtra SUVs, parsea cada marca y consolida.</div></div>
            <div class="step-card"><div class="step-number">04</div><div class="step-text"><strong>Descargá el CSV</strong>Exportá el dataset limpio listo para análisis.</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="section-title">Marcas soportadas</p>', unsafe_allow_html=True)
        marcas_html = "".join([
            f'<span style="background:#261D3E;border:1px solid #3A2F5A;border-radius:6px;padding:4px 14px;font-size:0.78rem;color:#AAA;margin:3px;display:inline-block;">{m}</span>'
            for m in sorted(MARCAS_CONFIG.keys())
        ])
        st.markdown(f'<div style="line-height:2.4">{marcas_html}</div>', unsafe_allow_html=True)

    else:
        @st.cache_data(show_spinner="Leyendo archivo...")
        def leer_archivo(file_bytes: bytes, file_name: str) -> pd.DataFrame:
            buf = io.BytesIO(file_bytes)
            if file_name.endswith(".csv"):
                return pd.read_csv(buf, encoding="latin1", on_bad_lines="skip")
            return pd.read_excel(buf, engine="openpyxl", skiprows=5)

        # ── Leer y consolidar todos los archivos subidos
        dfs_raw = []
        nombres = []
        for uf in uploaded_files:
            df_tmp = leer_archivo(uf.getvalue(), uf.name)
            dfs_raw.append(df_tmp)
            nombres.append(uf.name)

        if len(dfs_raw) == 1:
            df_raw = dfs_raw[0]
        else:
            df_raw = pd.concat(dfs_raw, ignore_index=True)

        with st.expander(f"🔍  Vista previa — {len(uploaded_files)} archivo(s) consolidado(s)"):
            st.markdown(f"""
            <div style='font-size:0.78rem;color:#666;margin-bottom:0.6rem;'>
                <span style='color:#F0B74D'>■</span>&nbsp;{df_raw.shape[0]:,} filas totales &nbsp;·&nbsp;
                <span style='color:#F0B74D'>■</span>&nbsp;{df_raw.shape[1]} columnas &nbsp;·&nbsp;
                <span style='color:#555'>{" · ".join(nombres)}</span>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_raw.head(10), use_container_width=True)

        if procesar_btn:
            if not marcas_seleccionadas:
                st.markdown('<div class="astara-warning">⚠️ Seleccioná al menos una marca para continuar.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Ejecutando pipeline ETL..."):
                    df_resultado, errores = etl_pipeline(df_raw.copy(), marcas_seleccionadas)

                if errores:
                    with st.expander("⚠️  Advertencias"):
                        for e in errores:
                            st.markdown(f'<div class="astara-warning">{e}</div>', unsafe_allow_html=True)

                if df_resultado.empty:
                    st.markdown('<div class="astara-warning">❌ No se generaron datos. Verificá la estructura del dataset.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="astara-success">
                        ✅&nbsp;&nbsp;<strong>ETL completado</strong> —
                        {df_resultado.shape[0]:,} registros procesados para
                        <strong style="color:#F0B74D">{len(marcas_seleccionadas)}</strong> marca(s).
                    </div>
                    """, unsafe_allow_html=True)

                    n_marcas   = df_resultado["MARCA"].nunique()   if "MARCA"   in df_resultado.columns else "—"
                    n_modelos  = df_resultado["modelo"].nunique()  if "modelo"  in df_resultado.columns else "—"
                    n_periodos = df_resultado["periodo"].nunique() if "periodo" in df_resultado.columns else "—"

                    st.markdown(f"""
                    <div class="metric-row">
                        <div class="metric-card"><div class="metric-label">Registros</div><div class="metric-value">{df_resultado.shape[0]:,}</div></div>
                        <div class="metric-card"><div class="metric-label">Marcas</div><div class="metric-value"><span>{n_marcas}</span></div></div>
                        <div class="metric-card"><div class="metric-label">Modelos únicos</div><div class="metric-value"><span>{n_modelos}</span></div></div>
                        <div class="metric-card"><div class="metric-label">Períodos</div><div class="metric-value"><span>{n_periodos}</span></div></div>
                    </div>
                    """, unsafe_allow_html=True)

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

                    st.markdown(f'<div style="font-size:0.75rem;color:#444;margin-bottom:0.4rem;">{len(df_vista):,} registros visibles</div>', unsafe_allow_html=True)
                    st.dataframe(df_vista, use_container_width=True, height=420)

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
                        <div style='background:#1A1A1A;border:1px solid #2A2A2A;border-radius:10px;
                                    padding:0.9rem 1rem;font-size:0.78rem;color:#666;text-align:center;'>
                            {df_resultado.shape[0]:,} filas<br>
                            <span style='color:#F0B74D;font-weight:700;font-size:1rem'>{df_resultado.shape[1]} cols</span>
                        </div>
                        """, unsafe_allow_html=True)

with tab2:
    import numpy as np
    import re as _re
    import plotly.graph_objects as go
    import plotly.express as px

    # ── helpers de paleta
    LIME   = "#F0B74D"
    PURPLE = "#1E1932"
    CARD   = "#261D3E"
    BORDER = "#3A2F5A"
    MUTED  = "#9B8FBB"

    PLOTLY_COLORS = [
        "#F0B74D","#7B6FE8","#4FC3C3","#E86F9A","#6FC87B",
        "#E8A06F","#6FA8E8","#C36FD4","#E8D46F","#6FD4C3",
        "#E87B7B","#9AE86F","#6F8CE8","#E8C36F","#C36FA8",
    ]

    st.markdown('<p class="section-title">Cargar dataset de precios</p>', unsafe_allow_html=True)

    uploaded_precios = st.file_uploader(
        "Dataset Nyvus",
        type=["xlsx", "xls"],
        key="uploader_precios",
        label_visibility="collapsed",
        help="Reporte exportado de Nyvus (.xlsx)"
    )

    if uploaded_precios is None:
        st.markdown("""
        <div class="astara-info">
            <strong>👈 Subí el reporte Nyvus (.xlsx)</strong> para transformar el dataset de precios y explorar gráficos dinámicos.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="section-title">Qué vas a poder hacer</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">01</div>
                <div class="step-text"><strong>ETL automático</strong>Detecta columnas lista y bonificado sin importar cuántos meses tenga el reporte</div>
            </div>
            <div class="step-card">
                <div class="step-number">02</div>
                <div class="step-text"><strong>Métricas derivadas</strong>Calcula variación mensual, descuento lista vs bonificado y más</div>
            </div>
            <div class="step-card">
                <div class="step-number">03</div>
                <div class="step-text"><strong>Gráficos dinámicos</strong>Filtrá por marca, modelo y versión y explorá evolución de precios, descuentos y variaciones</div>
            </div>
            <div class="step-card">
                <div class="step-number">04</div>
                <div class="step-text"><strong>Descarga</strong>CSV detalle por versión y CSV agregado por marca + modelo + mes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        @st.cache_data(show_spinner="Transformando dataset de precios...")
        def etl_precios_v2(file_bytes: bytes) -> tuple:
            import io, numpy as np, re as _re
            df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0)

            columnas_fijas_ok = [
                'ID', 'Código', 'MARCA', 'Modelo', 'Versión',
                'Categoría', 'Segmento', 'Tracción',
                'Tipo De Motor - Combustible Principal',
                'Tipo De Motor - Combustible Alternativo',
                'Transmisión'
            ]
            columnas_fijas = [c for c in columnas_fijas_ok if c in df.columns]

            # ── Bloques de precios
            fechas_lista = [
                col for col in df.columns
                if ('2024' in str(col) or '2025' in str(col) or '2026' in str(col))
                and not str(col).endswith('.1')
                and not str(col).startswith('Unnamed')
            ]
            fechas_bonif = [col for col in df.columns if str(col).endswith('.1')]

            if not fechas_lista or not fechas_bonif:
                return None, None, None, "No se detectaron columnas de precios. Verificá que el archivo sea un reporte Nyvus válido."

            df_lista = df[columnas_fijas + fechas_lista].copy()
            df_bonif = df[columnas_fijas + fechas_bonif].copy()
            df_bonif = df_bonif.rename(columns=lambda x: x.replace('.1', '') if x.endswith('.1') else x)

            df_long = pd.melt(df_lista, id_vars=columnas_fijas, var_name='MES', value_name='PRECIO_LISTA')
            df_bonif_long = pd.melt(df_bonif, id_vars=columnas_fijas, var_name='MES', value_name='PRECIO_BONIFICADO')

            df_final = df_long.merge(
                df_bonif_long[['ID', 'MES', 'PRECIO_BONIFICADO']],
                on=['ID', 'MES'], how='left'
            )

            for col in ['PRECIO_LISTA', 'PRECIO_BONIFICADO']:
                df_final[col] = pd.to_numeric(df_final[col].replace('-', np.nan), errors='coerce')

            mes_map = {
                'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,
                'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,
                'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12
            }
            df_final['MES_NUM'] = df_final['MES'].str.split(' ').str[0].map(mes_map)
            df_final['ANIO']    = pd.to_numeric(df_final['MES'].str.split(' ').str[1], errors='coerce')
            df_final['FECHA']   = pd.to_datetime(
                df_final['ANIO'].astype(str) + '-' + df_final['MES_NUM'].astype(str) + '-01',
                errors='coerce'
            )
            df_final = df_final.sort_values(['ID', 'ANIO', 'MES_NUM']).reset_index(drop=True)

            # ── Filtro SUV
            if 'Segmento' in df_final.columns:
                df_final = df_final[
                    df_final['Segmento'].str.contains(r'\bSUV\b', case=False, na=False)
                ].copy()

            # ── Métricas
            df_final['DIF_LB_NOM']  = df_final['PRECIO_LISTA'] - df_final['PRECIO_BONIFICADO']
            df_final['DIF_LB_PCT']  = df_final['DIF_LB_NOM'] / df_final['PRECIO_LISTA']
            df_final['VAR_LISTA_NOM'] = df_final.groupby('ID')['PRECIO_LISTA'].diff()
            df_final['VAR_LISTA_PCT'] = df_final.groupby('ID')['PRECIO_LISTA'].pct_change()
            df_final['VAR_BONIF_NOM'] = df_final.groupby('ID')['PRECIO_BONIFICADO'].diff()
            df_final['VAR_BONIF_PCT'] = df_final.groupby('ID')['PRECIO_BONIFICADO'].pct_change()

            # ── Agregado por MARCA + Modelo + Versión + MES
            grp = [c for c in ['MARCA','Modelo','Versión','MES','MES_NUM','ANIO','FECHA'] if c in df_final.columns]
            agg_cols = ['PRECIO_LISTA','PRECIO_BONIFICADO','DIF_LB_NOM','DIF_LB_PCT',
                        'VAR_LISTA_NOM','VAR_LISTA_PCT','VAR_BONIF_NOM','VAR_BONIF_PCT']
            agg_cols_ok = [c for c in agg_cols if c in df_final.columns]

            df_agg = df_final.groupby(grp, as_index=False).agg(
                {c: ['mean','min','max'] for c in agg_cols_ok}
            )
            df_agg.columns = [
                '_'.join(col).upper().strip('_') if col[1] else col[0]
                for col in df_agg.columns
            ]

            meses = sorted(fechas_lista)
            return df_final, df_agg, meses, None

        # ── Ejecutar ETL
        precios_bytes = uploaded_precios.getvalue()
        df_pf, df_agg, meses_det, err = etl_precios_v2(precios_bytes)

        if err:
            st.markdown(f'<div class="astara-warning">❌ {err}</div>', unsafe_allow_html=True)
            st.stop()

        # ── Métricas header
        n_vers   = df_pf['ID'].nunique() if 'ID' in df_pf.columns else len(df_pf)
        n_marcas = df_pf['MARCA'].nunique() if 'MARCA' in df_pf.columns else '—'
        n_mod    = df_pf['Modelo'].nunique() if 'Modelo' in df_pf.columns else '—'
        n_meses  = len(meses_det)

        st.markdown(f"""
        <div class="astara-success">
            ✅&nbsp;&nbsp;<strong>Dataset transformado</strong> —
            {len(df_pf):,} registros · <strong style="color:#F0B74D">{n_meses}</strong> meses detectados
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-label">Registros</div>
                <div class="metric-value">{len(df_pf):,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Marcas</div>
                <div class="metric-value"><span>{n_marcas}</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Modelos</div>
                <div class="metric-value"><span>{n_mod}</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Meses</div>
                <div class="metric-value"><span>{n_meses}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ══════════════════════════════════════════════
        # FILTROS GLOBALES
        # ══════════════════════════════════════════════
        st.markdown('<p class="section-title">Filtros</p>', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns(3)

        with fc1:
            marcas_disp = sorted(df_agg['MARCA'].dropna().unique()) if 'MARCA' in df_agg.columns else []
            marcas_sel = st.multiselect("Marca", marcas_disp, default=marcas_disp, key="g_marca")

        df_f1 = df_agg[df_agg['MARCA'].isin(marcas_sel)] if marcas_sel else df_agg.copy()

        with fc2:
            modelos_disp = sorted(df_f1['Modelo'].dropna().unique()) if 'Modelo' in df_f1.columns else []
            modelos_sel = st.multiselect("Modelo", modelos_disp, key="g_modelo")

        df_f2 = df_f1[df_f1['Modelo'].isin(modelos_sel)] if modelos_sel else df_f1.copy()

        with fc3:
            versiones_disp = sorted(df_f2['Versión'].dropna().unique()) if 'Versión' in df_f2.columns else []
            versiones_sel = st.multiselect("Versión", versiones_disp, key="g_version")

        df_graf = df_f2[df_f2['Versión'].isin(versiones_sel)].copy() if versiones_sel else df_f2.copy()

        if 'FECHA' in df_graf.columns:
            df_graf['FECHA'] = pd.to_datetime(df_graf['FECHA'], errors='coerce')
            df_graf = df_graf.sort_values('FECHA')

        df_graf['ETIQUETA'] = df_graf['MARCA'] + ' · ' + df_graf['Modelo'] + ' · ' + df_graf['Versión']

        if df_graf.empty:
            st.markdown('<div class="astara-warning">⚠️ Sin datos para los filtros seleccionados.</div>', unsafe_allow_html=True)
        else:
            etiquetas = sorted(df_graf['ETIQUETA'].dropna().unique())
            color_map = {e: PLOTLY_COLORS[i % len(PLOTLY_COLORS)] for i, e in enumerate(etiquetas)}

            PLOTLY_LAYOUT = dict(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#D4C9F0', size=12),
                legend=dict(
                    bgcolor='rgba(38,29,62,0.9)',
                    bordercolor='#3A2F5A',
                    borderwidth=1,
                    font=dict(size=10),
                ),
                xaxis=dict(gridcolor='#3A2F5A', linecolor='#3A2F5A', tickfont=dict(size=10)),
                yaxis=dict(gridcolor='#3A2F5A', linecolor='#3A2F5A', tickfont=dict(size=10)),
                margin=dict(l=50, r=20, t=50, b=60),
                hoverlabel=dict(bgcolor='#261D3E', bordercolor='#F0B74D', font_color='#D4C9F0'),
            )

            # ══════════════════════════════════════════════
            # GRÁFICO 1 — EVOLUCIÓN PRECIO LISTA Y BONIFICADO
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Evolución mensual · Precio lista vs bonificado</p>', unsafe_allow_html=True)

            precio_tipo = st.radio(
                "Mostrar",
                ["Ambos", "Solo Lista", "Solo Bonificado"],
                horizontal=True, key="r_precio_tipo"
            )

            fig1 = go.Figure()
            for etiq in etiquetas:
                df_e = df_graf[df_graf['ETIQUETA'] == etiq]
                color = color_map[etiq]
                if precio_tipo in ["Ambos", "Solo Lista"] and 'PRECIO_LISTA_MEAN' in df_e.columns:
                    fig1.add_trace(go.Scatter(
                        x=df_e['FECHA'], y=df_e['PRECIO_LISTA_MEAN'],
                        name=f"{etiq} · Lista",
                        line=dict(color=color, width=2),
                        mode='lines+markers', marker=dict(size=5),
                        hovertemplate='<b>%{fullData.name}</b><br>Fecha: %{x|%b %Y}<br>Precio Lista: $%{y:,.0f}<extra></extra>'
                    ))
                if precio_tipo in ["Ambos", "Solo Bonificado"] and 'PRECIO_BONIFICADO_MEAN' in df_e.columns:
                    fig1.add_trace(go.Scatter(
                        x=df_e['FECHA'], y=df_e['PRECIO_BONIFICADO_MEAN'],
                        name=f"{etiq} · Bonif.",
                        line=dict(color=color, width=2, dash='dot'),
                        mode='lines+markers', marker=dict(size=5, symbol='diamond'),
                        hovertemplate='<b>%{fullData.name}</b><br>Fecha: %{x|%b %Y}<br>Precio Bonif: $%{y:,.0f}<extra></extra>'
                    ))

            fig1.update_layout(**PLOTLY_LAYOUT, title=dict(text="Evolución de Precios", font=dict(color='#F0B74D', size=14)), height=420)
            fig1.update_yaxes(tickprefix="$", tickformat=",.0f")
            st.plotly_chart(fig1, use_container_width=True)

            # ══════════════════════════════════════════════
            # GRÁFICO 2 — DESCUENTO % (Lista vs Bonificado)
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Descuento mensual · % lista vs bonificado</p>', unsafe_allow_html=True)

            if 'DIF_LB_PCT_MEAN' in df_graf.columns:
                fig2 = go.Figure()
                for etiq in etiquetas:
                    df_e = df_graf[df_graf['ETIQUETA'] == etiq]
                    fig2.add_trace(go.Scatter(
                        x=df_e['FECHA'],
                        y=(df_e['DIF_LB_PCT_MEAN'] * 100).round(2),
                        name=etiq,
                        line=dict(color=color_map[etiq], width=2),
                        mode='lines+markers', marker=dict(size=5),
                        hovertemplate='<b>%{fullData.name}</b><br>Fecha: %{x|%b %Y}<br>Descuento: %{y:.2f}%<extra></extra>'
                    ))
                fig2.update_layout(**PLOTLY_LAYOUT, title=dict(text="% Descuento sobre Precio Lista", font=dict(color='#F0B74D', size=14)), height=380)
                fig2.update_yaxes(ticksuffix="%", tickformat=".1f")
                fig2.add_hline(y=0, line_dash="dot", line_color="#3A2F5A")
                st.plotly_chart(fig2, use_container_width=True)

            # ══════════════════════════════════════════════
            # GRÁFICOS 3 y 4 — VARIACIONES MENSUALES
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Variación mensual de precios</p>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                if 'VAR_LISTA_PCT_MEAN' in df_graf.columns:
                    fig3 = go.Figure()
                    for etiq in etiquetas:
                        df_e = df_graf[df_graf['ETIQUETA'] == etiq]
                        fig3.add_trace(go.Bar(
                            x=df_e['FECHA'],
                            y=(df_e['VAR_LISTA_PCT_MEAN'] * 100).round(2),
                            name=etiq,
                            marker_color=color_map[etiq],
                            hovertemplate='<b>%{fullData.name}</b><br>%{x|%b %Y}<br>Var: %{y:.2f}%<extra></extra>'
                        ))
                    fig3.update_layout(
                        **PLOTLY_LAYOUT, barmode='group',
                        title=dict(text="Var. % Mensual · Precio Lista", font=dict(color='#F0B74D', size=13)),
                        height=350, showlegend=False
                    )
                    fig3.update_yaxes(ticksuffix="%")
                    fig3.add_hline(y=0, line_dash="dot", line_color="#3A2F5A")
                    st.plotly_chart(fig3, use_container_width=True)

            with col_g2:
                if 'VAR_BONIF_PCT_MEAN' in df_graf.columns:
                    fig4 = go.Figure()
                    for etiq in etiquetas:
                        df_e = df_graf[df_graf['ETIQUETA'] == etiq]
                        fig4.add_trace(go.Bar(
                            x=df_e['FECHA'],
                            y=(df_e['VAR_BONIF_PCT_MEAN'] * 100).round(2),
                            name=etiq,
                            marker_color=color_map[etiq],
                            hovertemplate='<b>%{fullData.name}</b><br>%{x|%b %Y}<br>Var: %{y:.2f}%<extra></extra>'
                        ))
                    fig4.update_layout(
                        **PLOTLY_LAYOUT, barmode='group',
                        title=dict(text="Var. % Mensual · Precio Bonificado", font=dict(color='#F0B74D', size=13)),
                        height=350, showlegend=False
                    )
                    fig4.update_yaxes(ticksuffix="%")
                    fig4.add_hline(y=0, line_dash="dot", line_color="#3A2F5A")
                    st.plotly_chart(fig4, use_container_width=True)

            # ══════════════════════════════════════════════
            # GRÁFICO 5 — SNAPSHOT ÚLTIMO MES
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Snapshot último mes · Precio lista vs bonificado</p>', unsafe_allow_html=True)

            ult_anio = df_graf['ANIO'].max()
            ult_mes  = df_graf[df_graf['ANIO'] == ult_anio]['MES_NUM'].max()
            df_ult   = df_graf[(df_graf['ANIO'] == ult_anio) & (df_graf['MES_NUM'] == ult_mes)].copy()
            df_ult   = df_ult.sort_values('PRECIO_LISTA_MEAN')

            if not df_ult.empty and 'PRECIO_LISTA_MEAN' in df_ult.columns:
                fig5 = go.Figure()
                fig5.add_trace(go.Bar(
                    y=df_ult['ETIQUETA'], x=df_ult['PRECIO_LISTA_MEAN'],
                    name='Precio Lista', orientation='h',
                    marker_color=LIME, opacity=0.85,
                    hovertemplate='<b>%{y}</b><br>Lista: $%{x:,.0f}<extra></extra>'
                ))
                if 'PRECIO_BONIFICADO_MEAN' in df_ult.columns:
                    fig5.add_trace(go.Bar(
                        y=df_ult['ETIQUETA'], x=df_ult['PRECIO_BONIFICADO_MEAN'],
                        name='Precio Bonificado', orientation='h',
                        marker_color='#7B6FE8', opacity=0.85,
                        hovertemplate='<b>%{y}</b><br>Bonif.: $%{x:,.0f}<extra></extra>'
                    ))
                fig5.update_layout(
                    **PLOTLY_LAYOUT, barmode='group',
                    title=dict(
                        text=f"Precios · {int(ult_mes):02d}/{int(ult_anio)}",
                        font=dict(color='#F0B74D', size=14)
                    ),
                    height=max(350, len(df_ult) * 45),
                    xaxis_tickprefix="$", xaxis_tickformat=",.0f",
                )
                st.plotly_chart(fig5, use_container_width=True)

            # ══════════════════════════════════════════════
            # TABLA + DESCARGA
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Tabla de datos filtrados</p>', unsafe_allow_html=True)

            pct_cols = [c for c in df_graf.columns if 'PCT' in c]
            df_show = df_graf.copy()
            for c in pct_cols:
                df_show[c] = df_show[c].map(lambda x: f"{x:.2%}" if pd.notna(x) else "")

            st.markdown(f'<div style="font-size:0.75rem;color:#444;margin-bottom:0.4rem;">{len(df_graf):,} registros</div>', unsafe_allow_html=True)
            st.dataframe(df_show.drop(columns=['ETIQUETA'], errors='ignore'), use_container_width=True, height=360)

            st.markdown('<p class="section-title">Exportar</p>', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                buf1 = io.BytesIO()
                df_pf.to_csv(buf1, index=False, encoding='utf-8-sig')
                buf1.seek(0)
                st.download_button(
                    label="⬇️  Detalle por versión (.csv)",
                    data=buf1, file_name="precios_detalle.csv",
                    mime="text/csv", use_container_width=True, key="dl_det"
                )
            with col_d2:
                buf2 = io.BytesIO()
                df_agg.to_csv(buf2, index=False, encoding='utf-8-sig')
                buf2.seek(0)
                st.download_button(
                    label="⬇️  Agregado marca·modelo·versión (.csv)",
                    data=buf2, file_name="precios_agregado.csv",
                    mime="text/csv", use_container_width=True, key="dl_agg"
                )

with tab3:
    import plotly.graph_objects as go
    import plotly.express as px

    LIME   = "#F0B74D"
    PURPLE = "#1E1932"
    CARD   = "#261D3E"
    BORDER = "#3A2F5A"
    MUTED  = "#9B8FBB"
    PLOTLY_COLORS = [
        "#F0B74D","#7B6FE8","#4FC3C3","#E86F9A","#6FC87B",
        "#E8A06F","#6FA8E8","#C36FD4","#E8D46F","#6FD4C3",
        "#E87B7B","#9AE86F","#6F8CE8","#E8C36F","#C36FA8",
    ]
    PLOTLY_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#D4C9F0", size=12),
        xaxis=dict(gridcolor="#3A2F5A", linecolor="#3A2F5A", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#3A2F5A", linecolor="#3A2F5A", tickfont=dict(size=10)),
        margin=dict(l=50, r=20, t=50, b=60),
        hoverlabel=dict(bgcolor="#261D3E", bordercolor="#F0B74D", font_color="#D4C9F0"),
    )
    LEGEND_STYLE = dict(bgcolor="rgba(38,29,62,0.9)", bordercolor="#3A2F5A", borderwidth=1, font=dict(size=10))

    MARCAS_DISPONIBLES = ['KIA', 'DFSK', 'HYUNDAI', 'GEELY', 'SUBARU', 'CHANGAN', 'NISSAN', 'VOLKSWAGEN', 'JAC', 'CHERY', 'CHEVROLET', 'HONDA', 'MAZDA', 'SUZUKI', 'GREAT WALL', 'MITSUBISHI', 'RENAULT', 'HAVAL', 'JETOUR', 'PEUGEOT', 'GAC', 'JEEP', 'BYD', 'SWM', 'DONGFENG', 'JAECOO', 'OMODA', 'FORD']

    st.markdown('<p class="section-title">Cargar dataset de inmatriculaciones</p>', unsafe_allow_html=True)

    uploaded_inmat = st.file_uploader(
        "Dataset Inmatriculaciones",
        type=["csv", "xlsx", "xls"],
        key="uploader_inmat",
        label_visibility="collapsed",
        help="Archivo Market_Results en .csv (recomendado) o .xlsx"
    )

    if uploaded_inmat is None:
        st.markdown("""
        <div class="astara-info">
            <strong>⬆️ Subí el archivo de inmatriculaciones</strong> en formato <strong>.csv</strong> (recomendado) o .xlsx para explorar el volumen de ventas por marca, modelo y versión.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="section-title">Qué vas a poder explorar</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="steps-grid">
            <div class="step-card"><div class="step-number">01</div><div class="step-text"><strong>Volumen por marca</strong>Ranking de marcas SUV por unidades inmatriculadas en el período seleccionado</div></div>
            <div class="step-card"><div class="step-number">02</div><div class="step-text"><strong>Evolución mensual</strong>Comportamiento mes a mes de inmatriculaciones por marca y modelo</div></div>
            <div class="step-card"><div class="step-number">03</div><div class="step-text"><strong>Mix de modelos</strong>Participación de modelos dentro de cada marca y share de mercado</div></div>
            <div class="step-card"><div class="step-number">04</div><div class="step-text"><strong>Detalle por versión</strong>Desglose hasta nivel de versión con filtros dinámicos</div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        @st.cache_data(show_spinner="Procesando inmatriculaciones...")
        def etl_inmatriculaciones(file_bytes: bytes, file_name: str, marcas_filtro: tuple) -> tuple:
            import io
            buf = io.BytesIO(file_bytes)
            if file_name.endswith(".csv"):
                try:
                    df = pd.read_csv(buf, encoding="utf-8")
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(file_bytes), encoding="latin1")
            else:
                df = pd.read_excel(buf)

            # Filtrar SUV
            col_carr = next((c for c in df.columns if "carroceria" in c.lower()), None)
            col_marca = next((c for c in df.columns if "marca" in c.lower()), None)
            col_modelo = next((c for c in df.columns if "modelo" in c.lower()), None)
            col_anio = next((c for c in df.columns if c.upper() in ["AÑO", "ANO", "YEAR"]), None)
            col_mes = next((c for c in df.columns if c.upper() == "MES"), None)
            col_acum = next((c for c in df.columns if "acum" in c.lower()), None)
            col_version = next((c for c in df.columns if "version" in c.lower()), None)
            col_cat = next((c for c in df.columns if "categor" in c.lower()), None)

            missing = [n for n, c in [
                ("CARROCERIA", col_carr), ("MARCA", col_marca),
                ("MODELO", col_modelo), ("ACUM", col_acum)
            ] if c is None]
            if missing:
                return None, None, None, f"Columnas no encontradas: {missing}. Columnas disponibles: {list(df.columns[:20])}"

            # Filtro SUV
            df_suv = df[df[col_carr].astype(str).str.upper().str.contains("SUV", na=False)].copy()

            # Filtro marcas
            df_suv = df_suv[
                df_suv[col_marca].astype(str).str.upper().apply(
                    lambda x: any(m in x for m in marcas_filtro)
                )
            ].copy()

            # Extraer mes número
            if col_mes:
                df_suv["MES_NUM"] = pd.to_numeric(
                    df_suv[col_mes].astype(str).str.extract(r"(\d+)")[0],
                    errors="coerce"
                )
            else:
                df_suv["MES_NUM"] = 1

            # Periodo
            if col_anio:
                df_suv["PERIODO"] = pd.to_datetime(dict(
                    year=pd.to_numeric(df_suv[col_anio], errors="coerce"),
                    month=df_suv["MES_NUM"].fillna(1).astype(int),
                    day=1
                ), errors="coerce")
                df_suv["PERIODO_YM"] = df_suv["PERIODO"].dt.strftime("%Y-%m")
                df_suv["AÑO"] = pd.to_numeric(df_suv[col_anio], errors="coerce")
            else:
                df_suv["PERIODO"] = pd.NaT
                df_suv["PERIODO_YM"] = "N/A"
                df_suv["AÑO"] = None

            # Normalizar columnas clave
            df_suv["MARCA"]   = df_suv[col_marca].astype(str).str.upper().str.strip()
            df_suv["MODELO"]  = df_suv[col_modelo].astype(str).str.upper().str.strip()
            df_suv["VERSION"] = df_suv[col_version].astype(str).str.strip() if col_version else "—"
            df_suv["CATEGORIA"] = df_suv[col_cat].astype(str).str.strip() if col_cat else "—"
            df_suv["UNIDADES"] = pd.to_numeric(df_suv[col_acum], errors="coerce").fillna(0)

            # Resumen agrupado
            grp_cols = ["AÑO", "MES_NUM", "PERIODO", "PERIODO_YM", "CATEGORIA", "MARCA", "MODELO", "VERSION"]
            grp_cols_ok = [c for c in grp_cols if c in df_suv.columns]

            df_resumen = (
                df_suv.groupby(grp_cols_ok, as_index=False)["UNIDADES"].sum()
            )
            df_resumen = df_resumen.sort_values(["MARCA", "MODELO", "VERSION", "AÑO", "MES_NUM"])

            # Variación mensual por marca+modelo+version
            df_resumen["VAR_UNID_NOM"] = df_resumen.groupby(["MARCA", "MODELO", "VERSION"])["UNIDADES"].diff()
            df_resumen["VAR_UNID_PCT"] = df_resumen.groupby(["MARCA", "MODELO", "VERSION"])["UNIDADES"].pct_change()

            return df_suv, df_resumen, grp_cols_ok, None

        # ── Filtro de marcas antes de cargar
        st.markdown('<p class="section-title">Filtro de marcas</p>', unsafe_allow_html=True)
        col_ma, col_mb = st.columns([4, 1])
        with col_ma:
            marcas_inmat_sel = st.multiselect(
                "Marcas a incluir",
                options=sorted(MARCAS_DISPONIBLES),
                default=sorted(MARCAS_DISPONIBLES),
                key="inmat_marcas",
                label_visibility="collapsed"
            )
        with col_mb:
            anios_disp = [2023, 2024, 2025, 2026]
            anio_sel = st.multiselect("Año", anios_disp, default=[2025], key="inmat_anio")

        if not marcas_inmat_sel:
            st.markdown('<div class="astara-warning">⚠️ Seleccioná al menos una marca.</div>', unsafe_allow_html=True)
        else:
            inmat_bytes = uploaded_inmat.getvalue()
            df_raw_i, df_res, grp_cols_ok, err = etl_inmatriculaciones(
                inmat_bytes, uploaded_inmat.name, tuple(sorted(marcas_inmat_sel))
            )

            if err:
                st.markdown(f'<div class="astara-warning">❌ {err}</div>', unsafe_allow_html=True)
            else:
                # Filtro por año
                if anio_sel and "AÑO" in df_res.columns:
                    df_res_f = df_res[df_res["AÑO"].isin(anio_sel)].copy()
                else:
                    df_res_f = df_res.copy()

                # ── KPIs
                total_u  = int(df_res_f["UNIDADES"].sum())
                n_marcas = df_res_f["MARCA"].nunique()
                n_mod    = df_res_f["MODELO"].nunique()
                n_meses  = df_res_f["PERIODO_YM"].nunique()

                st.markdown(f"""
                <div class="astara-success">
                    ✅&nbsp;&nbsp;<strong>Dataset procesado</strong> —
                    <strong style="color:#F0B74D">{total_u:,}</strong> unidades inmatriculadas ·
                    {n_marcas} marcas · {n_mod} modelos
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card"><div class="metric-label">Unidades totales</div><div class="metric-value">{total_u:,}</div></div>
                    <div class="metric-card"><div class="metric-label">Marcas</div><div class="metric-value"><span>{n_marcas}</span></div></div>
                    <div class="metric-card"><div class="metric-label">Modelos</div><div class="metric-value"><span>{n_mod}</span></div></div>
                    <div class="metric-card"><div class="metric-label">Períodos</div><div class="metric-value"><span>{n_meses}</span></div></div>
                </div>
                """, unsafe_allow_html=True)

                # ══════════════════════════════════════════
                # GRÁFICO 1 — RANKING MARCAS (barras)
                # ══════════════════════════════════════════
                st.markdown('<p class="section-title">Ranking de marcas · unidades totales</p>', unsafe_allow_html=True)

                df_rank = (
                    df_res_f.groupby("MARCA", as_index=False)["UNIDADES"].sum()
                    .sort_values("UNIDADES", ascending=True)
                )
                color_map_m = {m: PLOTLY_COLORS[i % len(PLOTLY_COLORS)] for i, m in enumerate(df_rank["MARCA"])}

                fig_rank = go.Figure(go.Bar(
                    y=df_rank["MARCA"],
                    x=df_rank["UNIDADES"],
                    orientation="h",
                    marker_color=[color_map_m[m] for m in df_rank["MARCA"]],
                    text=df_rank["UNIDADES"].apply(lambda x: f"{x:,.0f}"),
                    textposition="outside",
                    textfont=dict(color="#D4C9F0", size=10),
                    hovertemplate="<b>%{y}</b><br>Unidades: %{x:,.0f}<extra></extra>"
                ))
                fig_rank.update_layout(
                    **PLOTLY_LAYOUT,
                    title=dict(text="Inmatriculaciones por Marca", font=dict(color=LIME, size=14)),
                    height=max(350, len(df_rank) * 32),
                    xaxis_title="Unidades",
                    showlegend=False,
                )
                st.plotly_chart(fig_rank, use_container_width=True)

                # ══════════════════════════════════════════
                # GRÁFICO 2 — EVOLUCIÓN MENSUAL POR MARCA
                # ══════════════════════════════════════════
                st.markdown('<p class="section-title">Evolución mensual por marca</p>', unsafe_allow_html=True)

                marcas_evo = st.multiselect(
                    "Seleccioná marcas para el gráfico de evolución",
                    sorted(df_res_f["MARCA"].dropna().unique()),
                    default=sorted(df_res_f["MARCA"].dropna().unique())[:8],
                    key="inmat_evo_marcas"
                )

                df_evo = (
                    df_res_f[df_res_f["MARCA"].isin(marcas_evo)]
                    .groupby(["PERIODO", "MARCA"], as_index=False)["UNIDADES"].sum()
                    .sort_values("PERIODO")
                )
                df_evo["PERIODO"] = pd.to_datetime(df_evo["PERIODO"], errors="coerce")

                fig_evo = go.Figure()
                for i, marca in enumerate(marcas_evo):
                    df_m = df_evo[df_evo["MARCA"] == marca]
                    fig_evo.add_trace(go.Scatter(
                        x=df_m["PERIODO"], y=df_m["UNIDADES"],
                        name=marca,
                        mode="lines+markers",
                        line=dict(color=PLOTLY_COLORS[i % len(PLOTLY_COLORS)], width=2),
                        marker=dict(size=5),
                        hovertemplate="<b>%{fullData.name}</b><br>%{x|%b %Y}<br>Unidades: %{y:,.0f}<extra></extra>"
                    ))
                fig_evo.update_layout(
                    **PLOTLY_LAYOUT,
                    title=dict(text="Evolución Mensual de Inmatriculaciones", font=dict(color=LIME, size=14)),
                    height=420, xaxis_title="Mes", yaxis_title="Unidades"
                )
                st.plotly_chart(fig_evo, use_container_width=True)

                # ══════════════════════════════════════════
                # GRÁFICO 3 — SHARE DE MERCADO (pie/donut)
                # ══════════════════════════════════════════
                st.markdown('<p class="section-title">Share de mercado por marca</p>', unsafe_allow_html=True)

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    df_share = df_res_f.groupby("MARCA", as_index=False)["UNIDADES"].sum().sort_values("UNIDADES", ascending=False)
                    fig_pie = go.Figure(go.Pie(
                        labels=df_share["MARCA"],
                        values=df_share["UNIDADES"],
                        hole=0.5,
                        marker=dict(colors=PLOTLY_COLORS[:len(df_share)], line=dict(color="#1E1932", width=2)),
                        textfont=dict(size=10, color="#D4C9F0"),
                        hovertemplate="<b>%{label}</b><br>Unidades: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
                    ))
                    fig_pie.update_layout(
                        **PLOTLY_LAYOUT,
                        legend=dict(bgcolor="rgba(38,29,62,0.9)", bordercolor="#3A2F5A", borderwidth=1, font=dict(size=9)),
                        title=dict(text="Share por Marca", font=dict(color=LIME, size=13)),
                        height=380, showlegend=True,
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_g2:
                    # Top 10 modelos
                    df_top_mod = (
                        df_res_f.groupby("MODELO", as_index=False)["UNIDADES"].sum()
                        .sort_values("UNIDADES", ascending=False).head(10)
                    )
                    fig_mod = go.Figure(go.Bar(
                        y=df_top_mod["MODELO"],
                        x=df_top_mod["UNIDADES"],
                        orientation="h",
                        marker_color=PLOTLY_COLORS[:len(df_top_mod)],
                        text=df_top_mod["UNIDADES"].apply(lambda x: f"{x:,.0f}"),
                        textposition="outside",
                        textfont=dict(color="#D4C9F0", size=10),
                        hovertemplate="<b>%{y}</b><br>Unidades: %{x:,.0f}<extra></extra>"
                    ))
                    fig_mod.update_layout(
                        **PLOTLY_LAYOUT,
                        title=dict(text="Top 10 Modelos", font=dict(color=LIME, size=13)),
                        height=380, showlegend=False
                    )
                    st.plotly_chart(fig_mod, use_container_width=True)

                # ══════════════════════════════════════════
                # GRÁFICO 4 — DETALLE POR MODELO (filtrado)
                # ══════════════════════════════════════════
                st.markdown('<p class="section-title">Evolución mensual · detalle por modelo</p>', unsafe_allow_html=True)

                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    marcas_det = sorted(df_res_f["MARCA"].dropna().unique())
                    marca_det_sel = st.multiselect("Marca", marcas_det, key="inmat_det_marca")
                with col_d2:
                    df_det_tmp = df_res_f[df_res_f["MARCA"].isin(marca_det_sel)] if marca_det_sel else df_res_f
                    modelos_det = sorted(df_det_tmp["MODELO"].dropna().unique())
                    modelo_det_sel = st.multiselect("Modelo", modelos_det, key="inmat_det_modelo")
                with col_d3:
                    df_det_tmp2 = df_det_tmp[df_det_tmp["MODELO"].isin(modelo_det_sel)] if modelo_det_sel else df_det_tmp
                    vers_det = sorted(df_det_tmp2["VERSION"].dropna().unique())
                    version_det_sel = st.multiselect("Versión", vers_det, key="inmat_det_version")

                df_det = df_det_tmp2.copy()
                if version_det_sel:
                    df_det = df_det[df_det["VERSION"].isin(version_det_sel)]

                if not df_det.empty:
                    df_det["ETIQUETA"] = df_det["MARCA"] + " · " + df_det["MODELO"] + " · " + df_det["VERSION"]
                    df_det_evo = df_det.groupby(["PERIODO", "ETIQUETA"], as_index=False)["UNIDADES"].sum().sort_values("PERIODO")
                    df_det_evo["PERIODO"] = pd.to_datetime(df_det_evo["PERIODO"], errors="coerce")
                    etiquetas_det = sorted(df_det_evo["ETIQUETA"].dropna().unique())

                    fig_det = go.Figure()
                    for i, etiq in enumerate(etiquetas_det):
                        df_e = df_det_evo[df_det_evo["ETIQUETA"] == etiq]
                        fig_det.add_trace(go.Scatter(
                            x=df_e["PERIODO"], y=df_e["UNIDADES"],
                            name=etiq,
                            mode="lines+markers",
                            line=dict(color=PLOTLY_COLORS[i % len(PLOTLY_COLORS)], width=2),
                            marker=dict(size=5),
                            hovertemplate="<b>%{fullData.name}</b><br>%{x|%b %Y}<br>Unidades: %{y:,.0f}<extra></extra>"
                        ))
                    fig_det.update_layout(
                        **PLOTLY_LAYOUT,
                        title=dict(text="Evolución Mensual por Versión", font=dict(color=LIME, size=14)),
                        height=420
                    )
                    st.plotly_chart(fig_det, use_container_width=True)

                    # ── Acumulado por versión (barras apiladas)
                    df_acum_ver = (
                        df_det.groupby(["ETIQUETA"], as_index=False)["UNIDADES"].sum()
                        .sort_values("UNIDADES", ascending=True)
                    )
                    fig_acum = go.Figure(go.Bar(
                        y=df_acum_ver["ETIQUETA"],
                        x=df_acum_ver["UNIDADES"],
                        orientation="h",
                        marker_color=[PLOTLY_COLORS[i % len(PLOTLY_COLORS)] for i in range(len(df_acum_ver))],
                        text=df_acum_ver["UNIDADES"].apply(lambda x: f"{x:,.0f}"),
                        textposition="outside",
                        textfont=dict(color="#D4C9F0", size=10),
                        hovertemplate="<b>%{y}</b><br>Unidades: %{x:,.0f}<extra></extra>"
                    ))
                    fig_acum.update_layout(
                        **PLOTLY_LAYOUT,
                        title=dict(text="Acumulado por Versión", font=dict(color=LIME, size=13)),
                        height=max(300, len(df_acum_ver) * 35),
                        showlegend=False
                    )
                    st.plotly_chart(fig_acum, use_container_width=True)

                # ══════════════════════════════════════════
                # TABLA + DESCARGA
                # ══════════════════════════════════════════
                st.markdown('<p class="section-title">Tabla de datos</p>', unsafe_allow_html=True)

                pct_cols_i = [c for c in df_res_f.columns if "PCT" in c]
                df_show_i = df_res_f.copy()
                for c in pct_cols_i:
                    df_show_i[c] = df_show_i[c].map(lambda x: f"{x:.1%}" if pd.notna(x) else "")

                st.markdown(f'<div style="font-size:0.75rem;color:#444;margin-bottom:0.4rem;">{len(df_res_f):,} registros</div>', unsafe_allow_html=True)
                st.dataframe(df_show_i.drop(columns=["PERIODO"], errors="ignore"), use_container_width=True, height=360)

                st.markdown('<p class="section-title">Exportar</p>', unsafe_allow_html=True)
                buf_i = io.BytesIO()
                df_res_f.to_csv(buf_i, index=False, encoding="utf-8-sig")
                buf_i.seek(0)
                st.download_button(
                    label="⬇️  Descargar inmatriculaciones (.csv)",
                    data=buf_i,
                    file_name="inmatriculaciones_suv.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="dl_inmat"
                )

with tab4:
    import io as _io
    import hashlib

    st.markdown("""
    <div class="astara-info">
        <strong>🔗 Matching Manual</strong> — Cargá los CSVs de las 3 fuentes,
        seleccioná los registros que son el mismo vehículo y asignales un ID común.
        Al final descargás un CSV unificado listo para el clustering.
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # CARGA DE LAS 3 FUENTES
    # ══════════════════════════════════════════════
    st.markdown('<p class="section-title">Cargar datasets procesados</p>', unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown('<div style="font-size:0.78rem;color:#9B8FBB;margin-bottom:4px;">📦 Importaciones SUV</div>', unsafe_allow_html=True)
        f_imp = st.file_uploader("Importaciones", type=["csv"], key="cat_imp", label_visibility="collapsed")
    with col_c2:
        st.markdown('<div style="font-size:0.78rem;color:#9B8FBB;margin-bottom:4px;">💲 Precios Nyvus</div>', unsafe_allow_html=True)
        f_pre = st.file_uploader("Precios", type=["csv"], key="cat_pre", label_visibility="collapsed")
    with col_c3:
        st.markdown('<div style="font-size:0.78rem;color:#9B8FBB;margin-bottom:4px;">🚘 Inmatriculaciones</div>', unsafe_allow_html=True)
        f_inm = st.file_uploader("Inmatriculaciones", type=["csv"], key="cat_inm", label_visibility="collapsed")

    # badges de estado
    badges = ""
    for name, f in [("Importaciones", f_imp), ("Precios", f_pre), ("Inmatriculaciones", f_inm)]:
        color = "#F0B74D" if f else "#3A2F5A"
        icon  = "✅" if f else "⬜"
        badges += f'<span style="background:#261D3E;border:1px solid {color};border-radius:6px;padding:4px 12px;font-size:0.78rem;color:{color};margin:3px;display:inline-block;">{icon} {name}</span>'
    st.markdown(f'<div style="margin:0.5rem 0 1rem">{badges}</div>', unsafe_allow_html=True)

    loaded_any = any([f_imp, f_pre, f_inm])

    if not loaded_any:
        st.markdown("""
        <div class="steps-grid">
            <div class="step-card"><div class="step-number">01</div><div class="step-text"><strong>Exportá los CSVs</strong>Desde cada tab procesá y descargá el CSV correspondiente</div></div>
            <div class="step-card"><div class="step-number">02</div><div class="step-text"><strong>Cargalos acá</strong>Podés subir 1, 2 o las 3 fuentes</div></div>
            <div class="step-card"><div class="step-number">03</div><div class="step-text"><strong>Seleccioná y asigná</strong>Marcá los registros que son el mismo vehículo y asignales un ID</div></div>
            <div class="step-card"><div class="step-number">04</div><div class="step-text"><strong>Descargá el catálogo</strong>CSV con VEHICLE_ID listo para el JOIN y clustering</div></div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ══════════════════════════════════════════════
        # EXTRAER VALORES ÚNICOS DE CADA FUENTE
        # ══════════════════════════════════════════════
        @st.cache_data(show_spinner="Leyendo fuentes...")
        def extraer_unicos(imp_b, pre_b, inm_b):
            import io
            registros = []

            if imp_b:
                df = pd.read_csv(io.BytesIO(imp_b), encoding="utf-8")
                col_m  = next((c for c in df.columns if c.upper() == "MARCA"), None)
                col_mo = next((c for c in df.columns if c.upper() == "MODELO"), None)
                col_v  = next((c for c in df.columns if c.lower() == "version"), None)
                if col_m and col_mo:
                    sub = df[[col_m, col_mo] + ([col_v] if col_v else [])].copy()
                    sub.columns = ["MARCA","MODELO"] + (["VERSION"] if col_v else [])
                    if "VERSION" not in sub.columns: sub["VERSION"] = ""
                    sub = sub.dropna(subset=["MARCA","MODELO"]).drop_duplicates()
                    sub["FUENTE"] = "IMP"
                    registros.append(sub)

            if pre_b:
                df = pd.read_csv(io.BytesIO(pre_b), encoding="utf-8")
                col_m  = next((c for c in df.columns if c.upper() == "MARCA"), None)
                col_mo = next((c for c in df.columns if "modelo" in c.lower()), None)
                col_v  = next((c for c in df.columns if "versi" in c.lower()), None)
                if col_m and col_mo:
                    sub = df[[col_m, col_mo] + ([col_v] if col_v else [])].copy()
                    sub.columns = ["MARCA","MODELO"] + (["VERSION"] if col_v else [])
                    if "VERSION" not in sub.columns: sub["VERSION"] = ""
                    sub = sub.dropna(subset=["MARCA","MODELO"]).drop_duplicates()
                    sub["FUENTE"] = "PRE"
                    registros.append(sub)

            if inm_b:
                df = pd.read_csv(io.BytesIO(inm_b), encoding="utf-8")
                col_m  = next((c for c in df.columns if "marca" in c.lower()), None)
                col_mo = next((c for c in df.columns if "modelo" in c.lower()), None)
                col_v  = next((c for c in df.columns if "version" in c.lower()), None)
                if col_m and col_mo:
                    sub = df[[col_m, col_mo] + ([col_v] if col_v else [])].copy()
                    sub.columns = ["MARCA","MODELO"] + (["VERSION"] if col_v else [])
                    if "VERSION" not in sub.columns: sub["VERSION"] = ""
                    sub = sub.dropna(subset=["MARCA","MODELO"]).drop_duplicates()
                    sub["FUENTE"] = "INM"
                    registros.append(sub)

            if not registros:
                return pd.DataFrame()

            df_all = pd.concat(registros, ignore_index=True)
            df_all["MARCA"]   = df_all["MARCA"].astype(str).str.upper().str.strip()
            df_all["MODELO"]  = df_all["MODELO"].astype(str).str.upper().str.strip()
            df_all["VERSION"] = df_all["VERSION"].astype(str).str.strip()
            df_all["VERSION"] = df_all["VERSION"].replace({"nan":"","None":"","(en blanco)":"","SIN VERSION":""})
            df_all = df_all.drop_duplicates(subset=["FUENTE","MARCA","MODELO","VERSION"])
            df_all = df_all.sort_values(["MARCA","MODELO","VERSION","FUENTE"]).reset_index(drop=True)
            df_all["ROW_ID"] = df_all.index
            df_all["VEHICLE_ID"] = ""
            return df_all

        imp_b = f_imp.getvalue() if f_imp else None
        pre_b = f_pre.getvalue() if f_pre else None
        inm_b = f_inm.getvalue() if f_inm else None

        df_all = extraer_unicos(imp_b, pre_b, inm_b)

        if df_all.empty:
            st.markdown('<div class="astara-warning">❌ No se pudieron extraer registros.</div>', unsafe_allow_html=True)
        else:
            # Inicializar estado de IDs en session_state
            if "vehicle_ids" not in st.session_state:
                st.session_state.vehicle_ids = {}
            if "id_counter" not in st.session_state:
                st.session_state.id_counter = 1

            # ── KPIs
            n_total    = len(df_all)
            n_asignados = sum(1 for rid in df_all["ROW_ID"] if st.session_state.vehicle_ids.get(rid, "") != "")
            n_pendientes = n_total - n_asignados

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card"><div class="metric-label">Registros totales</div><div class="metric-value">{n_total:,}</div></div>
                <div class="metric-card"><div class="metric-label">Asignados</div><div class="metric-value"><span>{n_asignados}</span></div></div>
                <div class="metric-card"><div class="metric-label">Pendientes</div><div class="metric-value">{n_pendientes}</div></div>
                <div class="metric-card"><div class="metric-label">IDs únicos</div><div class="metric-value"><span>{len(set(v for v in st.session_state.vehicle_ids.values() if v))}</span></div></div>
            </div>
            """, unsafe_allow_html=True)

            # ══════════════════════════════════════════════
            # FILTROS
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Filtros</p>', unsafe_allow_html=True)
            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                marcas_disp = ["Todas"] + sorted(df_all["MARCA"].dropna().unique())
                marca_sel = st.selectbox("Marca", marcas_disp, key="match_marca")
            with col_f2:
                estado_sel = st.selectbox("Estado", ["Todos", "Sin asignar", "Asignados"], key="match_estado")
            with col_f3:
                fuente_sel = st.multiselect(
                    "Fuente", ["IMP","PRE","INM"],
                    default=["IMP","PRE","INM"], key="match_fuente"
                )

            # Aplicar filtros
            df_view = df_all.copy()
            if marca_sel != "Todas":
                df_view = df_view[df_view["MARCA"] == marca_sel]
            if fuente_sel:
                df_view = df_view[df_view["FUENTE"].isin(fuente_sel)]
            if estado_sel == "Sin asignar":
                df_view = df_view[df_view["ROW_ID"].apply(lambda r: st.session_state.vehicle_ids.get(r, "") == "")]
            elif estado_sel == "Asignados":
                df_view = df_view[df_view["ROW_ID"].apply(lambda r: st.session_state.vehicle_ids.get(r, "") != "")]

            st.markdown(f'<div style="font-size:0.75rem;color:#555;margin-bottom:0.5rem;">{len(df_view)} registros visibles</div>', unsafe_allow_html=True)

            # ══════════════════════════════════════════════
            # TABLA DE MATCHING
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Asignación de IDs</p>', unsafe_allow_html=True)

            # Leyenda de fuentes
            st.markdown("""
            <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
                <span style="background:#261D3E;border:1px solid #F0B74D;border-radius:4px;padding:2px 10px;font-size:0.72rem;color:#F0B74D;">IMP = Importaciones</span>
                <span style="background:#261D3E;border:1px solid #7B6FE8;border-radius:4px;padding:2px 10px;font-size:0.72rem;color:#7B6FE8;">PRE = Precios</span>
                <span style="background:#261D3E;border:1px solid #4FC3C3;border-radius:4px;padding:2px 10px;font-size:0.72rem;color:#4FC3C3;">INM = Inmatriculaciones</span>
            </div>
            """, unsafe_allow_html=True)

            # Render tabla fila por fila
            FUENTE_COLORS = {"IMP": "#F0B74D", "PRE": "#7B6FE8", "INM": "#4FC3C3"}

            # Agrupar por marca para separar visualmente
            marcas_en_vista = df_view["MARCA"].unique()

            for marca in sorted(marcas_en_vista):
                df_marca = df_view[df_view["MARCA"] == marca]

                with st.expander(f"**{marca}** — {len(df_marca)} registros", expanded=(len(marcas_en_vista) <= 3)):
                    # Selector múltiple de filas + botón asignar
                    col_sel, col_btn = st.columns([4, 1])

                    with col_sel:
                        opciones = []
                        for _, row in df_marca.iterrows():
                            vid = st.session_state.vehicle_ids.get(row["ROW_ID"], "")
                            ver = f" · {row['VERSION']}" if row["VERSION"] else ""
                            tag_id = f" [{vid}]" if vid else " [sin ID]"
                            opciones.append(f"{row['FUENTE']} · {row['MODELO']}{ver}{tag_id}")

                        seleccion = st.multiselect(
                            "Seleccioná los registros que son el mismo vehículo:",
                            options=list(range(len(opciones))),
                            format_func=lambda i: opciones[i],
                            key=f"sel_{marca}",
                            label_visibility="visible"
                        )

                    with col_btn:
                        st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)

                        # Botón asignar nuevo ID
                        if st.button("➕ Nuevo ID", key=f"new_{marca}", use_container_width=True):
                            if seleccion:
                                nuevo_id = f"VEH_{st.session_state.id_counter:04d}"
                                st.session_state.id_counter += 1
                                rows_marca = list(df_marca["ROW_ID"])
                                for idx_sel in seleccion:
                                    st.session_state.vehicle_ids[rows_marca[idx_sel]] = nuevo_id
                                st.rerun()

                        # Botón asignar a ID existente
                        ids_existentes = sorted(set(v for v in st.session_state.vehicle_ids.values() if v))
                        if ids_existentes:
                            id_existente = st.selectbox(
                                "O asignar a:",
                                ["—"] + ids_existentes,
                                key=f"existing_{marca}",
                                label_visibility="collapsed"
                            )
                            if st.button("Asignar", key=f"assign_existing_{marca}", use_container_width=True):
                                if seleccion and id_existente != "—":
                                    rows_marca = list(df_marca["ROW_ID"])
                                    for idx_sel in seleccion:
                                        st.session_state.vehicle_ids[rows_marca[idx_sel]] = id_existente
                                    st.rerun()

                        st.markdown("</div>", unsafe_allow_html=True)

                    # Botón quitar ID
                    if st.button("🗑 Quitar ID seleccionados", key=f"clear_{marca}", use_container_width=False):
                        if seleccion:
                            rows_marca = list(df_marca["ROW_ID"])
                            for idx_sel in seleccion:
                                st.session_state.vehicle_ids.pop(rows_marca[idx_sel], None)
                            st.rerun()

            # ══════════════════════════════════════════════
            # EXPORTAR
            # ══════════════════════════════════════════════
            st.markdown('<p class="section-title">Exportar catálogo</p>', unsafe_allow_html=True)

            # Construir df final con IDs asignados
            df_export = df_all.copy()
            df_export["VEHICLE_ID"] = df_export["ROW_ID"].apply(
                lambda r: st.session_state.vehicle_ids.get(r, "")
            )

            n_con_id = (df_export["VEHICLE_ID"] != "").sum()
            n_sin_id = (df_export["VEHICLE_ID"] == "").sum()

            col_e1, col_e2 = st.columns(2)

            with col_e1:
                buf_all = _io.BytesIO()
                df_export[["VEHICLE_ID","FUENTE","MARCA","MODELO","VERSION"]].to_csv(
                    buf_all, index=False, encoding="utf-8-sig"
                )
                buf_all.seek(0)
                st.download_button(
                    label=f"⬇️  Catálogo completo ({n_total} registros)",
                    data=buf_all,
                    file_name="catalogo_maestro.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="dl_cat_all"
                )

            with col_e2:
                df_solo_id = df_export[df_export["VEHICLE_ID"] != ""]
                buf_id = _io.BytesIO()
                df_solo_id[["VEHICLE_ID","FUENTE","MARCA","MODELO","VERSION"]].to_csv(
                    buf_id, index=False, encoding="utf-8-sig"
                )
                buf_id.seek(0)
                st.download_button(
                    label=f"⬇️  Solo con ID asignado ({n_con_id} registros)",
                    data=buf_id,
                    file_name="catalogo_con_id.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="dl_cat_id"
                )

            if n_sin_id > 0:
                st.markdown(
                    f'<div style="font-size:0.78rem;color:#9B8FBB;margin-top:0.5rem;">⚠️ {n_sin_id} registros aún sin ID asignado</div>',
                    unsafe_allow_html=True
                )

            # Reset
            st.markdown("---")
            if st.button("🔄 Reiniciar todos los IDs", key="reset_ids"):
                st.session_state.vehicle_ids = {}
                st.session_state.id_counter = 1
                st.rerun()
