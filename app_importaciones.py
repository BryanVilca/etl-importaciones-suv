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
    df_raw = df_raw.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
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
        <img src="data:image/png;base64,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" style="height:32px; display:block; margin-bottom:6px;" />
        <div style="font-size:0.65rem;color:#9B8FBB;text-transform:uppercase;
                    letter-spacing:0.12em;">Market View · Perú</div>
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
        <p class="astara-title">Astara <span>Market View</span></p>
        <p class="astara-subtitle">Inteligencia Competitiva &nbsp;·&nbsp; Mercado Peruano</p>
    </div>
    <div>
        <img src="data:image/png;base64,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" style="height:48px; display:block;" />
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
tab1, tab2 = st.tabs(["📦  Importaciones SUV", "💲  Precios Nyvus"])

with tab1:


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

with tab2:
    # ══════════════════════════════════════════════
    # TAB 2 — PRECIOS NYVUS
    # ══════════════════════════════════════════════
    import numpy as np

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
            <strong>👈 Subí el reporte Nyvus (.xlsx)</strong> para transformar y limpiar el dataset de precios.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="section-title">Cómo funciona</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">01</div>
                <div class="step-text"><strong>Cargá el reporte</strong>Exportá desde Nyvus el reporte de precios en .xlsx</div>
            </div>
            <div class="step-card">
                <div class="step-number">02</div>
                <div class="step-text"><strong>Detección automática</strong>La app detecta las columnas de precios lista y bonificado sin importar cuántos meses tiene el reporte</div>
            </div>
            <div class="step-card">
                <div class="step-number">03</div>
                <div class="step-text"><strong>Transformación</strong>Pivota el dataset a formato largo con métricas de variación mensual y descuento lista vs bonificado</div>
            </div>
            <div class="step-card">
                <div class="step-number">04</div>
                <div class="step-text"><strong>Descargá el resultado</strong>CSV limpio listo para análisis, con precio lista, bonificado, variaciones y % descuento</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        @st.cache_data(show_spinner="Leyendo reporte Nyvus...")
        def leer_nyvus(file_bytes: bytes, file_name: str) -> pd.DataFrame:
            import io
            return pd.read_excel(io.BytesIO(file_bytes), sheet_name=0)

        @st.cache_data(show_spinner="Transformando dataset de precios...")
        def etl_precios(file_bytes: bytes) -> tuple:
            import io, numpy as np
            df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0)

            # ── Detectar columnas fijas (no son fechas ni Unnamed)
            columnas_fijas_candidatas = [
                'ID', 'Código', 'MARCA', 'Modelo', 'Versión',
                'Categoría', 'Segmento', 'Tracción',
                'Tipo De Motor - Combustible Principal',
                'Tipo De Motor - Combustible Alternativo',
                'Transmisión'
            ]
            columnas_fijas = [c for c in columnas_fijas_candidatas if c in df.columns]

            # ── Detectar bloques de precios automáticamente
            # Bloque 1: columnas con nombre de mes/año sin sufijo .1
            mes_pattern = r'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+\d{4}$'
            fechas_lista = [
                col for col in df.columns
                if pd.Series(col).str.match(mes_pattern).any()
                and not str(col).endswith('.1')
                and not str(col).startswith('Unnamed')
            ]

            # Bloque 2: mismas columnas pero con sufijo .1 (bonificado)
            fechas_bonificado = [col for col in df.columns if str(col).endswith('.1')]

            if not fechas_lista or not fechas_bonificado:
                return pd.DataFrame(), [], "No se detectaron columnas de precios. Verificá que el archivo sea un reporte Nyvus válido."

            # ── Separar bloques
            df_lista = df[columnas_fijas + fechas_lista].copy()
            df_bonif = df[columnas_fijas + fechas_bonificado].copy()

            # ── Normalizar nombres del bloque bonificado (quitar .1)
            df_bonif = df_bonif.rename(columns=lambda x: x.replace('.1', '') if x.endswith('.1') else x)

            # ── Pivotar a formato largo
            df_lista_long = pd.melt(
                df_lista, id_vars=columnas_fijas,
                var_name='MES', value_name='PRECIO_LISTA'
            )
            df_bonif_long = pd.melt(
                df_bonif, id_vars=columnas_fijas,
                var_name='MES', value_name='PRECIO_BONIFICADO'
            )

            # ── Merge por ID + MES
            merge_keys = ['MES'] + ([c for c in ['ID'] if c in columnas_fijas])
            df_final = df_lista_long.merge(
                df_bonif_long[merge_keys + ['PRECIO_BONIFICADO']],
                on=merge_keys, how='left'
            )

            # ── Limpiar precios
            for col in ['PRECIO_LISTA', 'PRECIO_BONIFICADO']:
                df_final[col] = pd.to_numeric(
                    df_final[col].replace('-', np.nan), errors='coerce'
                )

            # ── Parsear fecha
            mes_map = {
                'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
                'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
                'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
            }
            df_final['MES_NUM'] = df_final['MES'].str.split(' ').str[0].map(mes_map)
            df_final['ANIO'] = df_final['MES'].str.split(' ').str[1].astype(int, errors='ignore')
            df_final['FECHA'] = pd.to_datetime(
                df_final['ANIO'].astype(str) + '-' + df_final['MES_NUM'].astype(str) + '-01',
                errors='coerce'
            )

            # ── Ordenar
            sort_cols = (['ID'] if 'ID' in df_final.columns else ['MARCA', 'Modelo']) + ['ANIO', 'MES_NUM']
            df_final = df_final.sort_values(sort_cols).reset_index(drop=True)

            # ── Métricas derivadas
            group_id = 'ID' if 'ID' in df_final.columns else ['MARCA', 'Modelo', 'Versión']

            df_final['DIF_LB_NOM'] = df_final['PRECIO_LISTA'] - df_final['PRECIO_BONIFICADO']
            df_final['DIF_LB_PCT'] = df_final['DIF_LB_NOM'] / df_final['PRECIO_LISTA']

            df_final['VAR_LISTA_NOM'] = df_final.groupby(group_id)['PRECIO_LISTA'].diff()
            df_final['VAR_LISTA_PCT'] = df_final.groupby(group_id)['PRECIO_LISTA'].pct_change()
            df_final['VAR_BONIF_NOM'] = df_final.groupby(group_id)['PRECIO_BONIFICADO'].diff()
            df_final['VAR_BONIF_PCT'] = df_final.groupby(group_id)['PRECIO_BONIFICADO'].pct_change()

            # ── Agregación por MARCA + Modelo + MES
            agg_cols = ['PRECIO_LISTA', 'PRECIO_BONIFICADO', 'DIF_LB_NOM', 'DIF_LB_PCT',
                        'VAR_LISTA_NOM', 'VAR_LISTA_PCT', 'VAR_BONIF_NOM', 'VAR_BONIF_PCT']
            group_agg = [c for c in ['MARCA', 'Modelo', 'MES', 'MES_NUM', 'ANIO', 'FECHA'] if c in df_final.columns]

            df_agg = (
                df_final.groupby(group_agg, as_index=False)
                .agg({c: ['mean', 'min', 'max'] for c in agg_cols if c in df_final.columns})
            )
            df_agg.columns = [
                '_'.join(col).upper().strip('_') if col[1] else col[0]
                for col in df_agg.columns
            ]

            meses_detectados = sorted(fechas_lista)
            return df_final, df_agg, meses_detectados, None

        # Cargar y procesar
        precios_bytes = uploaded_precios.getvalue()
        result = etl_precios(precios_bytes)

        if len(result) == 2:
            df_p, error_msg = result
            st.markdown(f'<div class="astara-warning">❌ {error_msg}</div>', unsafe_allow_html=True)
        else:
            df_precios_final, df_precios_agg, meses_detectados, error_msg = result

            if error_msg:
                st.markdown(f'<div class="astara-warning">❌ {error_msg}</div>', unsafe_allow_html=True)
            else:
                # ── Métricas
                n_versiones = df_precios_final['ID'].nunique() if 'ID' in df_precios_final.columns else len(df_precios_final)
                n_marcas = df_precios_final['MARCA'].nunique() if 'MARCA' in df_precios_final.columns else '—'
                n_modelos = df_precios_final['Modelo'].nunique() if 'Modelo' in df_precios_final.columns else '—'
                n_meses = len(meses_detectados)

                st.markdown(f"""
                <div class="astara-success">
                    ✅&nbsp;&nbsp;<strong>Dataset transformado</strong> —
                    {len(df_precios_final):,} registros · {n_meses} meses detectados automáticamente
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card">
                        <div class="metric-label">Registros</div>
                        <div class="metric-value">{len(df_precios_final):,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Marcas</div>
                        <div class="metric-value"><span>{n_marcas}</span></div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Modelos</div>
                        <div class="metric-value"><span>{n_modelos}</span></div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Meses</div>
                        <div class="metric-value"><span>{n_meses}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Meses detectados
                st.markdown('<p class="section-title">Meses detectados automáticamente</p>', unsafe_allow_html=True)
                meses_html = "".join([
                    f'<span style="background:#261D3E;border:1px solid #3A2F5A;border-radius:6px;'
                    f'padding:3px 10px;font-size:0.75rem;color:#F0B74D;margin:2px;display:inline-block;">{m}</span>'
                    for m in meses_detectados
                ])
                st.markdown(f'<div style="line-height:2.2;margin-bottom:1rem">{meses_html}</div>', unsafe_allow_html=True)

                # ── Explorar
                st.markdown('<p class="section-title">Explorar resultado — detalle por versión</p>', unsafe_allow_html=True)
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    marcas_p = sorted(df_precios_final['MARCA'].dropna().unique()) if 'MARCA' in df_precios_final.columns else []
                    marca_p_filtro = st.multiselect("Marca", marcas_p, default=marcas_p, key="pf_marca")
                with col_p2:
                    df_tmp = df_precios_final[df_precios_final['MARCA'].isin(marca_p_filtro)] if marca_p_filtro else df_precios_final
                    modelos_p = sorted(df_tmp['Modelo'].dropna().unique()) if 'Modelo' in df_tmp.columns else []
                    modelo_p_filtro = st.multiselect("Modelo", modelos_p, key="pf_modelo")
                with col_p3:
                    periodos_p = sorted(df_precios_final['MES'].dropna().unique()) if 'MES' in df_precios_final.columns else []
                    periodo_p_filtro = st.multiselect("Mes", periodos_p, key="pf_mes")

                df_p_vista = df_precios_final.copy()
                if marca_p_filtro:   df_p_vista = df_p_vista[df_p_vista['MARCA'].isin(marca_p_filtro)]
                if modelo_p_filtro:  df_p_vista = df_p_vista[df_p_vista['Modelo'].isin(modelo_p_filtro)]
                if periodo_p_filtro: df_p_vista = df_p_vista[df_p_vista['MES'].isin(periodo_p_filtro)]

                # Format pct columns
                pct_cols = [c for c in df_p_vista.columns if 'PCT' in c]
                df_display = df_p_vista.copy()
                for c in pct_cols:
                    df_display[c] = df_display[c].map(lambda x: f"{x:.1%}" if pd.notna(x) else "")

                st.markdown(f'<div style="font-size:0.75rem;color:#444;margin-bottom:0.4rem;">{len(df_p_vista):,} registros visibles</div>', unsafe_allow_html=True)
                st.dataframe(df_display, use_container_width=True, height=380)

                # ── Descarga — dos opciones
                st.markdown('<p class="section-title">Exportar</p>', unsafe_allow_html=True)
                col_d1, col_d2 = st.columns(2)

                with col_d1:
                    st.markdown('<div style="font-size:0.8rem;color:#9B8FBB;margin-bottom:0.4rem;">📄 Detalle por versión (formato largo)</div>', unsafe_allow_html=True)
                    buf1 = io.BytesIO()
                    df_precios_final.to_csv(buf1, index=False, encoding='utf-8-sig')
                    buf1.seek(0)
                    st.download_button(
                        label="⬇️  Descargar detalle (.csv)",
                        data=buf1,
                        file_name="precios_detalle_largo.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="dl_precios_detalle"
                    )

                with col_d2:
                    st.markdown('<div style="font-size:0.8rem;color:#9B8FBB;margin-bottom:0.4rem;">📊 Agregado por marca + modelo + mes</div>', unsafe_allow_html=True)
                    buf2 = io.BytesIO()
                    df_precios_agg.to_csv(buf2, index=False, encoding='utf-8-sig')
                    buf2.seek(0)
                    st.download_button(
                        label="⬇️  Descargar agregado (.csv)",
                        data=buf2,
                        file_name="precios_agregado_modelo_mes.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="dl_precios_agg"
                    )
