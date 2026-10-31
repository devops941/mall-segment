"""Shared visual layer for the multi-tenant pages.

Keeps the login, manual data-entry and store-management screens consistent with
the violet brand used by the analytics pages, without touching their markup.
"""

import html

import streamlit as st

ACCENT = "#7C3AED"
ACCENT_SOFT = "#A78BFA"
INK = "#1A1033"
MUTED = "#6B7280"

STATUS_STYLES = {
    "pending": ("Pending", "#B45309", "#FEF3C7", "#FDE68A"),
    "approved": ("Approved", "#15803D", "#DCFCE7", "#BBF7D0"),
    "rejected": ("Rejected", "#B91C1C", "#FEE2E2", "#FECACA"),
    "disabled": ("Disabled", "#475569", "#F1F5F9", "#E2E8F0"),
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --mz-accent: #7C3AED;
    --mz-accent-soft: #A78BFA;
    --mz-ink: #1A1033;
    --mz-muted: #6B7280;
    --mz-line: #E4DAFB;
    --mz-card: #FFFFFF;
}

/* ---- page atmosphere ------------------------------------------------ */
.stApp {
    background:
        radial-gradient(1100px 520px at 8% -8%, rgba(124,58,237,.13), transparent 60%),
        radial-gradient(900px 480px at 96% 4%, rgba(236,72,153,.10), transparent 58%),
        radial-gradient(700px 420px at 50% 108%, rgba(59,130,246,.08), transparent 62%),
        #FAF9FE;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: .035;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");
}
.block-container { position: relative; z-index: 1; }

/* ---- typography ----------------------------------------------------- */
h1, h2, h3 {
    font-family: 'Fraunces', Georgia, serif !important;
    letter-spacing: -.015em;
    color: var(--mz-ink);
}
h1 { font-weight: 700 !important; }
h2, h3 { font-weight: 600 !important; }
[data-testid="stMetricValue"] { font-family: 'Fraunces', Georgia, serif; }

/* ---- section rule --------------------------------------------------- */
hr { border-color: var(--mz-line) !important; opacity: .9; }

/* ---- forms as cards ------------------------------------------------- */
[data-testid="stForm"] {
    background: var(--mz-card);
    border: 1px solid var(--mz-line);
    border-radius: 18px;
    padding: 1.35rem 1.35rem 1.1rem;
    box-shadow: 0 18px 40px -28px rgba(26,16,51,.45);
    animation: mz-rise .45s cubic-bezier(.22,.9,.3,1) both;
}

/* ---- buttons -------------------------------------------------------- */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 11px;
    font-weight: 600;
    border: 1px solid var(--mz-line);
    transition: transform .14s ease, box-shadow .14s ease, background .14s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px -16px rgba(124,58,237,.75);
}
.stFormSubmitButton > button[kind="primary"],
.stFormSubmitButton > button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    border: none;
    color: #fff;
}

/* ---- tabs ----------------------------------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    gap: .4rem;
    background: rgba(124,58,237,.06);
    padding: .35rem;
    border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    padding: .5rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: #fff !important;
    box-shadow: 0 8px 18px -14px rgba(26,16,51,.6);
}

/* ---- inputs --------------------------------------------------------- */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] {
    border-radius: 11px !important;
}
/* Neutral white fields instead of the theme's lavender tint. Scoped away from
   the sign-in screen, which paints its own dark glass fields. */
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"],
[data-testid="stTextAreaRootElement"],
[data-testid="stDateInput"] > div,
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [role="group"],
[data-testid="stMultiSelect"] [role="group"] {
    background: #FFFFFF !important;
    border: 1px solid var(--mz-line) !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within,
[data-baseweb="select"] > div:focus-within,
[data-testid="stSelectbox"] [role="group"]:focus-within,
[data-testid="stMultiSelect"] [role="group"]:focus-within {
    border-color: var(--mz-accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.16) !important;
}

/* ---- animations ----------------------------------------------------- */
@keyframes mz-rise {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: none; }
}
@keyframes mz-fade {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ---- section heading ------------------------------------------------ */
.mz-sec {
    display: flex; align-items: center; gap: .65rem;
    margin: .2rem 0 .1rem;
}
.mz-sec .mz-sec-icon {
    width: 38px; height: 38px; border-radius: 11px;
    display: grid; place-items: center; font-size: 1.1rem;
    background: linear-gradient(135deg, rgba(124,58,237,.16), rgba(236,72,153,.14));
    border: 1px solid var(--mz-line);
}
.mz-sec h2 {
    font-size: 1.42rem !important; margin: 0 !important;
}
.mz-sec .mz-sec-sub {
    font-size: .82rem; color: var(--mz-muted); margin-top: .1rem;
}

/* ---- stat tiles ----------------------------------------------------- */
.mz-tiles { display: grid; gap: .85rem; grid-template-columns: repeat(3, 1fr); margin: .2rem 0 .9rem; }
.mz-tile {
    background: var(--mz-card);
    border: 1px solid var(--mz-line);
    border-left: 4px solid var(--mz-accent);
    border-radius: 15px;
    padding: .95rem 1.05rem;
    box-shadow: 0 16px 34px -30px rgba(26,16,51,.6);
    animation: mz-rise .5s cubic-bezier(.22,.9,.3,1) both;
}
.mz-tile .mz-tile-label {
    font: 600 .7rem/1 'Inter', sans-serif;
    letter-spacing: .1em; text-transform: uppercase; color: var(--mz-muted);
}
.mz-tile .mz-tile-value {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.85rem; font-weight: 700; color: var(--mz-ink);
    margin-top: .4rem; line-height: 1;
}
.mz-tile .mz-tile-hint { font-size: .76rem; color: var(--mz-muted); margin-top: .35rem; }

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
    background: var(--mz-card);
    border: 1px solid var(--mz-line);
    border-radius: 16px;
    padding: .85rem 1rem;
    box-shadow: 0 16px 34px -32px rgba(26,16,51,.6);
    animation: mz-rise .45s cubic-bezier(.22,.9,.3,1) both;
}
.mz-store .mz-avatar {
    flex: 0 0 auto; width: 44px; height: 44px; border-radius: 13px;
    display: grid; place-items: center; font-size: 1.25rem;
    color: #fff;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.28);
}
.mz-store .mz-store-name { font-weight: 700; color: var(--mz-ink); font-size: .98rem; }
.mz-store .mz-store-meta { font-size: .78rem; color: var(--mz-muted); margin-top: .1rem; }
.mz-store .mz-store-right { margin-left: auto; text-align: right; }
.mz-store .mz-store-count {
    font-family: 'Fraunces', Georgia, serif; font-size: 1.25rem; font-weight: 700;
    color: var(--mz-ink); line-height: 1;
}

/* ---- notice --------------------------------------------------------- */
.mz-note {
    border: 1px dashed var(--mz-line);
    background: linear-gradient(135deg, rgba(124,58,237,.05), rgba(236,72,153,.04));
    border-radius: 14px;
    padding: .85rem 1rem;
    font-size: .87rem; color: var(--mz-ink);
    animation: mz-fade .5s ease both;
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
        f"""
        <div class="mz-sec">
            <div class="mz-sec-icon">{icon}</div>
            <div><h2>{html.escape(title)}</h2>{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tiles(items: list[tuple[str, str, str]], accent: str = ACCENT) -> None:
    """Row of metric tiles: (label, value, hint)."""
    cells = "".join(
        f"""
        <div class="mz-tile" style="border-left-color:{accent};animation-delay:{i * 70}ms">
            <div class="mz-tile-label">{html.escape(label)}</div>
            <div class="mz-tile-value">{html.escape(str(value))}</div>
            <div class="mz-tile-hint">{html.escape(hint)}</div>
        </div>
        """
        for i, (label, value, hint) in enumerate(items)
    )
    st.markdown(f"<div class='mz-tiles'>{cells}</div>", unsafe_allow_html=True)


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
        f"""
        <div class="mz-store" style="animation-delay:{delay}ms">
            <div class="mz-avatar" style="background:linear-gradient(135deg,{color},{color}cc)">{icon}</div>
            <div>
                <div class="mz-store-name">{html.escape(name)}</div>
                <div class="mz-store-meta">{html.escape(meta)}</div>
            </div>
            <div class="mz-store-right">
                <div class="mz-store-count">{count}</div>
                <div class="mz-store-meta">{html.escape(count_label)}</div>
                <div style="margin-top:.3rem">{status_pill(status)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def note(text: str) -> None:
    """Soft informational band used for hints on the new pages."""
    st.markdown(f"<div class='mz-note'>{text}</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# Premium sign-in experience
# ═════════════════════════════════════════════════════════════════════════════

_AUTH_CSS = """
<style>
/* dark aurora backdrop for the auth screen only */
.stApp:has(.mz-auth) {
    background:
        radial-gradient(760px 520px at 14% 8%,  rgba(124,58,237,.55), transparent 62%),
        radial-gradient(680px 520px at 88% 12%, rgba(236,72,153,.40), transparent 60%),
        radial-gradient(820px 620px at 72% 96%, rgba(56,189,248,.32), transparent 62%),
        linear-gradient(165deg, #140A2E 0%, #1D0F45 46%, #0C0720 100%);
    background-attachment: fixed;
}
.stApp:has(.mz-auth)::before { opacity: .05; }
.stApp:has(.mz-auth) .block-container { padding-top: 3.2rem; }
.stApp:has(.mz-auth) [data-testid="stHeader"] { background: transparent; }

/* ---- left showcase ------------------------------------------------ */
.mz-auth-brand {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.15rem; font-weight: 700; color: #fff;
    display: flex; align-items: center; gap: .6rem; margin-bottom: 2.4rem;
}
.mz-auth-brand .mz-mark {
    width: 34px; height: 34px; border-radius: 10px;
    display: grid; place-items: center; font-size: 1.05rem;
    background: linear-gradient(135deg, #A855F7, #EC4899);
    box-shadow: 0 10px 24px -12px rgba(236,72,153,.9);
}
.mz-auth-kicker {
    font: 600 .7rem/1 'Inter', sans-serif; letter-spacing: .26em;
    text-transform: uppercase; color: #C4B5FD;
}
.mz-auth-title {
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 3.1rem; line-height: 1.05; font-weight: 600;
    color: #fff; margin: .9rem 0 1rem; letter-spacing: -.02em;
}
.mz-auth-title em {
    font-style: italic;
    background: linear-gradient(100deg, #F0ABFC, #A78BFA 55%, #67E8F9);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.mz-auth-lede {
    color: #CBC3E6; font-size: 1rem; line-height: 1.65; max-width: 46ch; margin: 0 0 2rem;
}
.mz-auth-list { list-style: none; margin: 0; padding: 0; }
.mz-auth-list li {
    display: flex; align-items: flex-start; gap: .8rem;
    padding: .7rem 0; border-top: 1px solid rgba(255,255,255,.08);
    color: #EDE9FE; font-size: .9rem;
}
.mz-auth-list li:first-child { border-top: none; }
.mz-auth-list .mz-ic {
    flex: 0 0 auto; width: 30px; height: 30px; border-radius: 9px;
    display: grid; place-items: center; font-size: .85rem;
    background: rgba(167,139,250,.16);
    border: 1px solid rgba(167,139,250,.32);
}
.mz-auth-list b { color: #fff; font-weight: 600; }
.mz-auth-list span.mz-sub { display: block; color: #A79FC7; font-size: .78rem; margin-top: .12rem; }

.mz-auth-stats {
    display: flex; gap: 2.4rem; margin-top: 2.6rem;
    padding-top: 1.6rem; border-top: 1px solid rgba(255,255,255,.1);
}
.mz-auth-stats .mz-stat-v {
    font-family: 'Fraunces', Georgia, serif; font-size: 1.7rem; font-weight: 700; color: #fff; line-height: 1;
}
.mz-auth-stats .mz-stat-l {
    font-size: .72rem; color: #A79FC7; text-transform: uppercase;
    letter-spacing: .12em; margin-top: .35rem;
}

/* ---- glass card --------------------------------------------------- */
.stApp:has(.mz-auth) [data-testid="stForm"] {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 22px;
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow: 0 40px 80px -40px rgba(0,0,0,.9), inset 0 1px 0 rgba(255,255,255,.14);
    padding: 1.6rem 1.5rem 1.3rem;
    animation: mz-rise .55s cubic-bezier(.22,.9,.3,1) both;
}
.stApp:has(.mz-auth) [data-testid="stForm"] label p,
.stApp:has(.mz-auth) [data-testid="stForm"] .stMarkdown p {
    color: #E7E2F8 !important; font-weight: 500;
}
.stApp:has(.mz-auth) [data-testid="stForm"] h5 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: #fff !important; font-size: 1.25rem !important; margin: .1rem 0 .9rem !important;
}
/* Streamlit 1.66 puts the field background on these testids, not on
   [data-baseweb="input"], so both selector families are covered here. */
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextInputRootElement"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stNumberInputContainer"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextAreaRootElement"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="input"],
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="select"] > div {
    background: rgba(10,5,28,.55) !important;
    border: 1px solid rgba(255,255,255,.16) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 2px rgba(0,0,0,.35);
    transition: border-color .16s ease, box-shadow .16s ease;
}
/* clear any inner wrapper that still carries the theme's light fill */
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextInputRootElement"] div,
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="input"] div,
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="base-input"] {
    background-color: transparent !important;
}
/* Base Web paints input text with -webkit-text-fill-color, which beats `color`.
   Both must be set or the typed characters stay invisible on the dark card. */
.stApp:has(.mz-auth) [data-testid="stForm"] input,
.stApp:has(.mz-auth) [data-testid="stForm"] textarea {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #F0ABFC !important;
    background: transparent !important;
    font-size: .95rem !important;
    padding: .15rem .1rem !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] input::placeholder,
.stApp:has(.mz-auth) [data-testid="stForm"] textarea::placeholder {
    color: #8E86B0 !important;
    -webkit-text-fill-color: #8E86B0 !important;
    opacity: 1 !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] input:-webkit-autofill,
.stApp:has(.mz-auth) [data-testid="stForm"] input:-webkit-autofill:hover,
.stApp:has(.mz-auth) [data-testid="stForm"] input:-webkit-autofill:focus {
    -webkit-text-fill-color: #FFFFFF !important;
    -webkit-box-shadow: 0 0 0 40px #150B33 inset !important;
    caret-color: #F0ABFC !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stTextInputRootElement"]:focus-within,
.stApp:has(.mz-auth) [data-testid="stForm"] [data-baseweb="input"]:focus-within {
    border-color: #A855F7 !important;
    box-shadow: 0 0 0 4px rgba(168,85,247,.22), inset 0 1px 2px rgba(0,0,0,.35) !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    font-size: .8rem !important;
    letter-spacing: .02em;
    color: #CBC3E6 !important;
}
.stApp:has(.mz-auth) [data-testid="stForm"] .stFormSubmitButton > button {
    background: linear-gradient(120deg, #7C3AED, #A855F7 55%, #EC4899) !important;
    border: none !important; color: #fff !important;
    font-weight: 700; letter-spacing: .01em;
    box-shadow: 0 18px 34px -18px rgba(168,85,247,.95);
}
.stApp:has(.mz-auth) [data-testid="stForm"] .stFormSubmitButton > button:hover {
    filter: brightness(1.07); transform: translateY(-1px);
}

/* ---- segmented switch -------------------------------------------- */
.stApp:has(.mz-auth) [data-testid="stSegmentedControl"] button {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.12) !important;
    color: #CBC3E6 !important; font-weight: 600;
}
.stApp:has(.mz-auth) [data-testid="stSegmentedControl"] button[aria-checked="true"],
.stApp:has(.mz-auth) [data-testid="stSegmentedControl"] button[data-selected="true"] {
    background: linear-gradient(120deg, rgba(168,85,247,.9), rgba(236,72,153,.85)) !important;
    color: #fff !important; border-color: transparent !important;
    box-shadow: 0 12px 26px -14px rgba(168,85,247,.95);
}

/* ---- footnotes / alerts ------------------------------------------- */
.mz-auth-foot {
    margin-top: 1rem; font-size: .78rem; color: #A79FC7; text-align: center;
}
.mz-auth-foot code {
    background: rgba(255,255,255,.08); color: #E7E2F8;
    padding: .1rem .38rem; border-radius: 6px;
}
.stApp:has(.mz-auth) [data-testid="stAlert"] {
    background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.16);
    color: #EDE9FE;
}
.stApp:has(.mz-auth) [data-testid="stAlert"] p { color: #EDE9FE !important; }

@media (max-width: 900px) {
    .mz-auth-title { font-size: 2.2rem; }
    .mz-auth-stats { gap: 1.4rem; }
}
</style>
"""


def auth_css() -> None:
    """Dark aurora styling, scoped to the sign-in screen."""
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
        f"""
        <div class="mz-auth">
            <div class="mz-auth-brand"><span class="mz-mark">◆</span> Mall Segment</div>
            <div class="mz-auth-kicker">KZ-ML-03 · Multi-tenant retail intelligence</div>
            <h1 class="mz-auth-title">One mall.<br>Every store, <em>its own story</em>.</h1>
            <p class="mz-auth-lede">
                Segment shoppers with K-Means, compare every tenant side by side,
                and let each store run its own analytics — all from one place.
            </p>
            <ul class="mz-auth-list">{rows}</ul>
            {stat_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def auth_card_head(title: str, subtitle: str) -> None:
    """Small heading block placed inside the glass form card."""
    st.markdown(
        f"<h5>{html.escape(title)}</h5>"
        f"<div style='color:#A79FC7;font-size:.82rem;margin:-.6rem 0 .8rem'>"
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
    border: 1px dashed rgba(240,171,252,.42);
    background: linear-gradient(135deg, rgba(168,85,247,.14), rgba(236,72,153,.10));
    border-radius: 16px;
    padding: .95rem 1.05rem;
    animation: mz-fade .5s ease both;
}
.mz-demo .mz-demo-tag {
    display: inline-flex; align-items: center; gap: .4rem;
    font: 700 .63rem/1 'Inter', sans-serif; letter-spacing: .18em;
    text-transform: uppercase; color: #F0ABFC;
}
.mz-demo .mz-demo-tag i {
    width: 6px; height: 6px; border-radius: 50%; background: #F0ABFC;
    box-shadow: 0 0 0 4px rgba(240,171,252,.2);
}
.mz-demo .mz-demo-note { color: #A79FC7; font-size: .74rem; margin: .35rem 0 .7rem; }
.mz-demo-row {
    display: flex; align-items: center; justify-content: space-between;
    gap: .8rem; padding: .5rem .7rem; border-radius: 10px;
    background: rgba(10,5,28,.5); border: 1px solid rgba(255,255,255,.1);
    margin-bottom: .45rem;
}
.mz-demo-row:last-child { margin-bottom: 0; }
.mz-demo-role { color: #EDE9FE; font-size: .8rem; font-weight: 600; }
.mz-demo-role span { display: block; color: #A79FC7; font-weight: 400; font-size: .72rem; margin-top: .1rem; }
.mz-demo-creds {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: .76rem; color: #F5F3FF; text-align: right; line-height: 1.5;
    white-space: nowrap;
}
.mz-demo-creds b { color: #F0ABFC; font-weight: 600; }
</style>
"""


def auth_demo_panel(rows: list[tuple[str, str, str, str]]) -> None:
    """Dev-only panel listing working demo logins: (role, hint, email, password)."""
    st.markdown(_DEMO_CSS, unsafe_allow_html=True)
    items = "".join(
        f"""
        <div class="mz-demo-row">
            <div class="mz-demo-role">{html.escape(role)}<span>{html.escape(hint)}</span></div>
            <div class="mz-demo-creds"><b>{html.escape(email)}</b><br>{html.escape(pw)}</div>
        </div>
        """
        for role, hint, email, pw in rows
    )
    st.markdown(
        f"""
        <div class="mz-demo">
            <div class="mz-demo-tag"><i></i>Demo credentials</div>
            <div class="mz-demo-note">Shown on this deployment only — never rendered in production.</div>
            {items}
        </div>
        """,
        unsafe_allow_html=True,
    )
