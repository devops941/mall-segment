"""Shared visual layer for the multi-tenant pages.

Provides a clean, modern, high-contrast light theme across all screens,
including the authentication gate, sidebar, dashboard, and management rosters.
"""

import html

import streamlit as st

ACCENT = "#4F46E5"
ACCENT_SOFT = "#818CF8"
INK = "#0F172A"
MUTED = "#64748B"

STATUS_STYLES = {
    "pending": ("Pending", "#B45309", "#FEF3C7", "#FDE68A"),
    "approved": ("Approved", "#15803D", "#DCFCE7", "#BBF7D0"),
    "rejected": ("Rejected", "#B91C1C", "#FEE2E2", "#FECACA"),
    "disabled": ("Disabled", "#475569", "#F1F5F9", "#E2E8F0"),
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --mz-accent: #4F46E5;
    --mz-accent-soft: #818CF8;
    --mz-ink: #0F172A;
    --mz-muted: #64748B;
    --mz-line: #E2E8F0;
    --mz-card: #FFFFFF;
}

/* ---- clean light page atmosphere ------------------------------------ */
.stApp {
    background-color: #F8FAFC !important;
    background-image:
        radial-gradient(at 100% 0%, rgba(79, 70, 229, 0.03) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(6, 182, 212, 0.03) 0px, transparent 50%) !important;
}
.block-container {
    position: relative;
    z-index: 1;
}

/* ---- light sidebar styling ------------------------------------------ */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] * {
    color: #0F172A;
}
[data-testid="stSidebar"] .mz-kicker {
    color: #4F46E5 !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .mz-pill {
    background: #EEF2FF !important;
    color: #4338CA !important;
    border: 1px solid #C7D2FE !important;
}
[data-testid="stSidebar"] hr {
    border-color: #E2E8F0 !important;
}

/* ---- typography ----------------------------------------------------- */
h1, h2, h3 {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    letter-spacing: -.02em;
    color: #0F172A !important;
}
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 700 !important; }
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    color: #0F172A !important;
}

/* ---- section rule --------------------------------------------------- */
hr {
    border-color: #E2E8F0 !important;
    opacity: 1;
}

/* ---- forms as clean light cards ------------------------------------- */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px;
    padding: 1.4rem 1.4rem 1.1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
    animation: mz-rise .4s cubic-bezier(.22,.9,.3,1) both;
}

/* ---- buttons -------------------------------------------------------- */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid #CBD5E1;
    background: #FFFFFF;
    color: #0F172A;
    transition: all .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    border-color: #4F46E5;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
}
.stFormSubmitButton > button[kind="primary"],
.stFormSubmitButton > button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}

/* ---- tabs ----------------------------------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    gap: .4rem;
    background: #F1F5F9;
    padding: .3rem;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    padding: .45rem .9rem;
    color: #64748B;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* ---- input fields --------------------------------------------------- */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] {
    border-radius: 10px !important;
}
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"],
[data-testid="stTextAreaRootElement"],
[data-testid="stDateInput"] > div,
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [role="group"],
[data-testid="stMultiSelect"] [role="group"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within,
[data-baseweb="select"] > div:focus-within,
[data-testid="stSelectbox"] [role="group"]:focus-within,
[data-testid="stMultiSelect"] [role="group"]:focus-within {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
}
[data-testid="stTextInputRootElement"] input,
[data-testid="stNumberInputContainer"] input,
[data-testid="stTextAreaRootElement"] textarea {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    font-size: .95rem !important;
}

/* ---- animations ----------------------------------------------------- */
@keyframes mz-rise {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: none; }
}
@keyframes mz-fade {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ---- section heading ------------------------------------------------ */
.mz-sec {
    display: flex; align-items: center; gap: .7rem;
    margin: .3rem 0 .2rem;
}
.mz-sec .mz-sec-icon {
    width: 40px; height: 40px; border-radius: 12px;
    display: grid; place-items: center; font-size: 1.15rem;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
}
.mz-sec h2 {
    font-size: 1.35rem !important; margin: 0 !important; color: #0F172A !important;
}
.mz-sec .mz-sec-sub {
    font-size: .82rem; color: #64748B; margin-top: .1rem;
}

/* ---- stat tiles ----------------------------------------------------- */
.mz-tiles {
    display: grid; gap: .85rem;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    margin: .3rem 0 1rem;
}
.mz-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid var(--mz-accent);
    border-radius: 14px;
    padding: .95rem 1.05rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    animation: mz-rise .4s cubic-bezier(.22,.9,.3,1) both;
}
.mz-tile .mz-tile-label {
    font: 600 .7rem/1 'Inter', sans-serif;
    letter-spacing: .08em; text-transform: uppercase; color: #64748B;
}
.mz-tile .mz-tile-value {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    font-size: 1.8rem; font-weight: 800; color: #0F172A;
    margin-top: .35rem; line-height: 1.1;
}
.mz-tile .mz-tile-hint {
    font-size: .76rem; color: #64748B; margin-top: .35rem;
}

/* ---- status pill ---------------------------------------------------- */
.mz-pill {
    display: inline-flex; align-items: center; gap: .4rem;
    padding: .24rem .68rem; border-radius: 999px;
    font: 600 .73rem/1.5 'Inter', sans-serif;
    border: 1px solid transparent; white-space: nowrap;
}
.mz-pill i { width: 7px; height: 7px; border-radius: 50%; background: currentColor; display: inline-block; }

/* ---- store card ----------------------------------------------------- */
.mz-store {
    display: flex; align-items: center; gap: .85rem;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: .85rem 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    animation: mz-rise .4s cubic-bezier(.22,.9,.3,1) both;
}
.mz-store .mz-avatar {
    flex: 0 0 auto; width: 42px; height: 42px; border-radius: 12px;
    display: grid; place-items: center; font-size: 1.2rem;
    color: #FFFFFF;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.2);
}
.mz-store .mz-store-name { font-weight: 700; color: #0F172A; font-size: .98rem; }
.mz-store .mz-store-meta { font-size: .78rem; color: #64748B; margin-top: .1rem; }
.mz-store .mz-store-right { margin-left: auto; text-align: right; }
.mz-store .mz-store-count {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; font-size: 1.25rem; font-weight: 800;
    color: #0F172A; line-height: 1;
}

/* ---- notice --------------------------------------------------------- */
.mz-note {
    border: 1px dashed #CBD5E1;
    background: #F8FAFC;
    border-radius: 12px;
    padding: .85rem 1rem;
    font-size: .87rem; color: #334155;
    animation: mz-fade .4s ease both;
}
</style>
"""


def inject_css() -> None:
    """Apply the shared stylesheet once per run."""
    st.markdown(_CSS, unsafe_allow_html=True)


def section(title: str, subtitle: str = "", icon: str = "✨") -> None:
    """Heading block with an icon chip, replacing the plain markdown header."""
    sub = f"<div class='mz-sec-sub'>{html.escape(subtitle)}</div>" if subtitle else ""
    st.markdown(
        f'<div class="mz-sec">'
        f'<div class="mz-sec-icon">{icon}</div>'
        f'<div><h2>{html.escape(title)}</h2>{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def tiles(items: list[tuple[str, str, str]], accent: str = ACCENT) -> None:
    """Row of metric tiles: (label, value, hint)."""
    cells = "".join(
        f'<div class="mz-tile" style="border-left-color:{accent};animation-delay:{i * 70}ms">'
        f'<div class="mz-tile-label">{html.escape(label)}</div>'
        f'<div class="mz-tile-value">{html.escape(str(value))}</div>'
        f'<div class="mz-tile-hint">{html.escape(hint)}</div>'
        f'</div>'
        for i, (label, value, hint) in enumerate(items)
    )
    st.markdown(f'<div class="mz-tiles">{cells}</div>', unsafe_allow_html=True)


def status_pill(status: str) -> str:
    """Inline HTML badge for a store lifecycle status."""
    label, fg, bg, border = STATUS_STYLES.get(
        status, (status.title(), MUTED, "#F1F5F9", "#E2E8F0")
    )
    return (
        f"<span class='mz-pill' style='color:{fg};background:{bg};border-color:{border}'>"
        f"<i></i>{label}</span>"
    )


def store_card(
    icon: str,
    name: str,
    meta: str,
    status: str,
    count: int,
    color: str,
    count_label: str = "shoppers",
    delay: int = 0,
) -> None:
    """Compact store summary row used in the management roster."""
    st.markdown(
        f'<div class="mz-store" style="animation-delay:{delay}ms">'
        f'<div class="mz-avatar" style="background:linear-gradient(135deg,{color},{color}dd)">{icon}</div>'
        f'<div><div class="mz-store-name">{html.escape(name)}</div>'
        f'<div class="mz-store-meta">{html.escape(meta)}</div></div>'
        f'<div class="mz-store-right"><div class="mz-store-count">{count}</div>'
        f'<div class="mz-store-meta">{html.escape(count_label)}</div>'
        f'<div style="margin-top:.3rem">{status_pill(status)}</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def note(text: str) -> None:
    """Soft informational band used for hints on the new pages."""
    st.markdown(f"<div class='mz-note'>{text}</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# Clean Modern Light Sign-In Screen
# ═════════════════════════════════════════════════════════════════════════════

_AUTH_CSS = """
<style>
/* Clean light backdrop for the auth screen */
.stApp:has(.mz-auth) {
    background-color: #F8FAFC !important;
    background-image:
        radial-gradient(at 10% 10%, rgba(79, 70, 229, 0.05) 0px, transparent 50%),
        radial-gradient(at 90% 90%, rgba(6, 182, 212, 0.05) 0px, transparent 50%) !important;
}
.stApp:has(.mz-auth) .block-container {
    padding-top: 2.5rem;
}
.stApp:has(.mz-auth) [data-testid="stHeader"] {
    background: transparent;
}

/* ---- left showcase ------------------------------------------------ */
.mz-auth-brand {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    font-size: 1.15rem; font-weight: 800; color: #0F172A;
    display: flex; align-items: center; gap: .6rem; margin-bottom: 2rem;
}
.mz-auth-brand .mz-mark {
    width: 34px; height: 34px; border-radius: 10px;
    display: grid; place-items: center; font-size: 1.05rem;
    background: linear-gradient(135deg, #4F46E5, #6366F1);
    color: #FFFFFF;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
}
.mz-auth-kicker {
    font: 700 .72rem/1 'Inter', sans-serif; letter-spacing: .2em;
    text-transform: uppercase; color: #4F46E5;
}
.mz-auth-title {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    font-size: 2.8rem; line-height: 1.1; font-weight: 800;
    color: #0F172A !important; margin: .8rem 0 .9rem; letter-spacing: -.03em;
}
.mz-auth-title em {
    font-style: normal;
    background: linear-gradient(120deg, #4F46E5, #06B6D4);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.mz-auth-lede {
    color: #475569; font-size: .98rem; line-height: 1.6; max-width: 46ch; margin: 0 0 1.8rem;
}
.mz-auth-list { list-style: none; margin: 0; padding: 0; }
.mz-auth-list li {
    display: flex; align-items: flex-start; gap: .8rem;
    padding: .65rem 0; border-top: 1px solid #E2E8F0;
    color: #334155; font-size: .9rem;
}
.mz-auth-list li:first-child { border-top: none; }
.mz-auth-list .mz-ic {
    flex: 0 0 auto; width: 32px; height: 32px; border-radius: 9px;
    display: grid; place-items: center; font-size: .9rem;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
}
.mz-auth-list b { color: #0F172A; font-weight: 600; }
.mz-auth-list span.mz-sub { display: block; color: #64748B; font-size: .78rem; margin-top: .12rem; }

.mz-auth-stats {
    display: flex; gap: 2.2rem; margin-top: 2rem;
    padding-top: 1.4rem; border-top: 1px solid #E2E8F0;
}
.mz-auth-stats .mz-stat-v {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; font-size: 1.7rem; font-weight: 800; color: #0F172A; line-height: 1;
}
.mz-auth-stats .mz-stat-l {
    font-size: .72rem; color: #64748B; text-transform: uppercase;
    letter-spacing: .1em; margin-top: .35rem; font-weight: 600;
}

/* ---- light card --------------------------------------------------- */
.stApp:has(.mz-auth) [data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06), 0 8px 10px -6px rgba(0, 0, 0, 0.03) !important;
    padding: 1.6rem 1.6rem 1.3rem;
    animation: mz-rise .45s cubic-bezier(.22,.9,.3,1) both;
}
.stApp:has(.mz-auth) [data-testid="stForm"] label p,
.stApp:has(.mz-auth) [data-testid="stForm"] .stMarkdown p {
    color: #334155 !important; font-weight: 500;
}
.stApp:has(.mz-auth) [data-testid="stForm"] h5 {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    color: #0F172A !important; font-size: 1.25rem !important; margin: .1rem 0 .9rem !important;
    font-weight: 700 !important;
}

.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextInputRootElement"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stNumberInputContainer"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextAreaRootElement"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="input"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color .15s ease, box-shadow .15s ease;
}

.stApp:has(.mz-auth) [data-testid="stForm"] input,
.stApp:has(.mz-auth) [data-testid="stForm"] textarea {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    caret-color: #4F46E5 !important;
    background: transparent !important;
    font-size: .95rem !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] input::placeholder,
.stApp:has(.mz-auth) [data-testid="stForm"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextInputRootElement"]:focus-within,
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="input"]:focus-within {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.14) !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    font-size: .83rem !important;
    font-weight: 600 !important;
    color: #334155 !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] .stFormSubmitButton > button {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    border: none !important; color: #FFFFFF !important;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}
.stApp:has(.mz-auth) [data-testid="stForm"] .stFormSubmitButton > button:hover {
    filter: brightness(1.05); transform: translateY(-1px);
}

/* ---- footnotes / alerts ------------------------------------------- */
.mz-auth-foot {
    margin-top: 1rem; font-size: .78rem; color: #64748B; text-align: center;
}
.mz-auth-foot code {
    background: #F1F5F9; color: #4338CA;
    padding: .15rem .4rem; border-radius: 6px; border: 1px solid #E2E8F0;
}
.stApp:has(.mz-auth) [data-testid="stAlert"] {
    background: #FFFFFF; border: 1px solid #E2E8F0;
    color: #0F172A; border-radius: 12px;
}
.stApp:has(.mz-auth) [data-testid="stAlert"] p { color: #0F172A !important; }

@media (max-width: 900px) {
    .mz-auth-title { font-size: 2.1rem; }
    .mz-auth-stats { gap: 1.2rem; }
}
</style>
"""


def auth_css() -> None:
    """Light theme styling, scoped to the sign-in screen."""
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)


def auth_showcase(stats: list[tuple[str, str]] | None = None) -> None:
    """Left-hand brand panel for the sign-in screen."""
    items = [
        ("🛡️", "Self-register, owner approves", "Stores apply; the mall owner clears them"),
        ("✉️", "Owner-created accounts", "Credentials are emailed straight to the store"),
        ("✍️", "Manual data entry", "No spreadsheets — stores type each shopper in"),
        ("🔒", "Tenant isolation", "Each store sees only its own; the owner sees all"),
    ]
    rows = "".join(
        f"<li><span class='mz-ic'>{ic}</span>"
        f"<span><b>{html.escape(t)}</b><span class='mz-sub'>{html.escape(s)}</span></span></li>"
        for ic, t, s in items
    )
    stat_html = ""
    if stats:
        stat_html = "<div class='mz-auth-stats'>" + "".join(
            f"<div><div class='mz-stat-v'>{html.escape(v)}</div>"
            f"<div class='mz-stat-l'>{html.escape(l)}</div></div>"
            for v, l in stats
        ) + "</div>"

    st.markdown(
        f'<div class="mz-auth">'
        f'<div class="mz-auth-brand"><span class="mz-mark">◆</span> Mall Segment</div>'
        f'<div class="mz-auth-kicker">KZ-ML-03 · Multi-tenant retail intelligence</div>'
        f'<h1 class="mz-auth-title">One mall.<br>Every store, <em>its own story</em>.</h1>'
        f'<p class="mz-auth-lede">'
        f'Segment shoppers with K-Means, compare every tenant side by side, '
        f'and let each store run its own analytics — all from one place.'
        f'</p>'
        f'<ul class="mz-auth-list">{rows}</ul>'
        f'{stat_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def auth_card_head(title: str, subtitle: str) -> None:
    """Small heading block placed inside the form card."""
    st.markdown(
        f"<h5>{html.escape(title)}</h5>"
        f"<div style='color:#64748B;font-size:.82rem;margin:-.6rem 0 .8rem'>"
        f"{html.escape(subtitle)}</div>",
        unsafe_allow_html=True,
    )


def auth_foot(html_text: str) -> None:
    """Muted footnote under a form."""
    st.markdown(f"<div class='mz-auth-foot'>{html_text}</div>", unsafe_allow_html=True)


_DEMO_CSS = """
<style>
.mz-demo {
    margin-top: 1.1rem;
    border: 1px dashed #CBD5E1;
    background: #FFFFFF;
    border-radius: 14px;
    padding: .95rem 1.05rem;
    animation: mz-fade .4s ease both;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.mz-demo .mz-demo-tag {
    display: inline-flex; align-items: center; gap: .4rem;
    font: 700 .68rem/1 'Inter', sans-serif; letter-spacing: .15em;
    text-transform: uppercase; color: #4F46E5;
}
.mz-demo .mz-demo-tag i {
    width: 6px; height: 6px; border-radius: 50%; background: #4F46E5;
}
.mz-demo .mz-demo-note { color: #64748B; font-size: .76rem; margin: .35rem 0 .7rem; }
.mz-demo-row {
    display: flex; align-items: center; justify-content: space-between;
    gap: .8rem; padding: .55rem .75rem; border-radius: 9px;
    background: #F8FAFC; border: 1px solid #E2E8F0;
    margin-bottom: .45rem;
}
.mz-demo-row:last-child { margin-bottom: 0; }
.mz-demo-role { color: #0F172A; font-size: .8rem; font-weight: 600; }
.mz-demo-role span { display: block; color: #64748B; font-weight: 400; font-size: .72rem; margin-top: .1rem; }
.mz-demo-creds {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: .76rem; color: #334155; text-align: right; line-height: 1.5;
    white-space: nowrap;
}
.mz-demo-creds b { color: #4F46E5; font-weight: 600; }
</style>
"""


def auth_demo_panel(rows: list[tuple[str, str, str, str]]) -> None:
    """Dev-only panel listing working demo logins: (role, hint, email, password)."""
    st.markdown(_DEMO_CSS, unsafe_allow_html=True)
    items = "".join(
        f'<div class="mz-demo-row">'
        f'<div class="mz-demo-role">{html.escape(role)}<span>{html.escape(hint)}</span></div>'
        f'<div class="mz-demo-creds"><b>{html.escape(email)}</b><br>{html.escape(pw)}</div>'
        f'</div>'
        for role, hint, email, pw in rows
    )
    st.markdown(
        f'<div class="mz-demo">'
        f'<div class="mz-demo-tag"><i></i>Demo credentials</div>'
        f'<div class="mz-demo-note">Use any demo account below to sign in:</div>'
        f'{items}'
        f'</div>',
        unsafe_allow_html=True,
    )
