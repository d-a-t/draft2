import streamlit as st

st.set_page_config(page_title="lmc 3403 draft 2", layout="wide")

# ---------------------------------------------------------------- data
# titles, bodies, scores and comment counts are all generated below (lorem ipsum + random numbers).
import random

POSTS = [
    {"id": 1, "sub": "r/todayilearned", "author": "u/tentacle_fan", "age": "3h", "flair": "Science", "kind": "image", "thumb": "🐙", "color": "#6a5acd"},
    {"id": 2, "sub": "r/modhelp", "author": "u/queue_zero", "age": "5h", "flair": "Discussion", "kind": "text", "thumb": "💬", "color": "#2e8b57"},
    {"id": 3, "sub": "r/battlestations", "author": "u/deskgoblin", "age": "7h", "flair": "Setup", "kind": "image", "thumb": "🖥️", "color": "#d2691e"},
    {"id": 4, "sub": "r/science", "author": "u/peer_reviewed", "age": "9h", "flair": "Health", "kind": "link", "thumb": "🔗", "color": "#4682b4"},
    {"id": 5, "sub": "r/help", "author": "u/scroll_weary", "age": "11h", "flair": "Feedback", "kind": "text", "thumb": "💬", "color": "#b22222"},
    {"id": 6, "sub": "r/Breadit", "author": "u/crumbshot", "age": "13h", "flair": "Progress", "kind": "image", "thumb": "🍞", "color": "#c68e17"},
    {"id": 7, "sub": "r/web_design", "author": "u/AutoModerator", "age": "1d", "flair": "Megathread", "kind": "text", "thumb": "📌", "color": "#708090"},
]
AD = {"id": 99, "sub": "Promoted", "author": "u/examplehost", "age": "ad", "flair": "Ad", "kind": "ad", "thumb": "📣", "color": "#444"}

# ---------------------------------------------------------------- lorem ipsum generator
LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et "
    "dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea "
    "commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur "
    "excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum"
).split()


def lorem_sentence(rng, lo=6, hi=14):
    words = [rng.choice(LOREM_WORDS) for _ in range(rng.randint(lo, hi))]
    return " ".join(words).capitalize() + "."


def lorem_title(rng):
    return lorem_sentence(rng, 5, 11).rstrip(".")


def lorem_paragraph(rng, sentences=3):
    return " ".join(lorem_sentence(rng) for _ in range(sentences))


# random content is generated once per browser session (so it stays stable while you click around),
# and a new random set appears each time the app is opened fresh.
if "seed" not in st.session_state:
    st.session_state.seed = random.randrange(1_000_000)

for _p in POSTS + [AD]:
    _rng = random.Random(st.session_state.seed + _p["id"])
    _p["title"] = ("Sponsored: " if _p["kind"] == "ad" else "") + lorem_title(_rng)
    _p["body"] = lorem_paragraph(_rng, 2 if _p["kind"] == "ad" else 3)
    if _p["kind"] == "ad":
        _p["score"], _p["comments"] = 0, 0
    else:
        _p["score"] = _rng.randint(50, 25000)
        _p["comments"] = _rng.randint(5, 1500)


RULES = ["1. Be civil and constructive", "2. No spam or self-promotion", "3. do you actually read this?", "4. deadlock is actually a p good game", "5. i saw a duck yesterday and it was very cute", "6. hello dr kim"]
FLAIRS = ["All", "Science", "Discussion", "Setup", "Health", "Feedback", "Progress", "Megathread"]

# ---------------------------------------------------------------- state
if "votes" not in st.session_state:
    st.session_state.votes = {}  # post id -> 1 / -1 / 0

# ---------------------------------------------------------------- sidebar controls
with st.sidebar:
    st.header("View settings")
    mode = st.radio("Layout", ["Old Reddit", "New Reddit (Cards)", "Hybrid (Compact Card)"], index=2)
    dark = st.toggle("Dark mode", value=True)
    show_thumbs = st.toggle("Show thumbnails", value=True)
    show_ads = st.toggle("Show sponsored posts", value=True)
    st.divider()
    sort = st.selectbox("Sort", ["Hot", "Top", "New", "Most comments"])
    flair_filter = st.selectbox("Filter by flair", FLAIRS)
    st.caption("Tip: switch layouts and compare how many posts fit on one screen.")

# ---------------------------------------------------------------- theme + css
if dark:
    bg, panel, text, muted, border, link, accent = "#0e1113", "#1a1d1f", "#e6e8ea", "#8b9299", "#2c3236", "#6cb2ff", "#ff5a1f"
else:
    bg, panel, text, muted, border, link, accent = "#f4f5f6", "#ffffff", "#1a1a1b", "#6b7177", "#d9dcde", "#0b5cc7", "#ff4500"
if mode == "Old Reddit":
    bg, panel, text, muted, border, link = "#ffffff", "#f6f9fc", "#222222", "#888888", "#e1e8ef", "#0000cc"
    if dark:
        bg, panel, text, muted, border, link = "#1b1b1b", "#222222", "#dddddd", "#888888", "#333333", "#7aa7ff"

pad = 4          # fixed compact density for the hybrid view
thumb_px = 34

# did you know how much i hate doing this? markdown SUCKS, maybe one good thing ai is used for is this css and html bullshit
st.markdown(f"""
<style>
.stApp {{ background:{bg}; color:{text}; }}
.stApp, .stApp p, .stApp span, .stApp label, .stApp li {{ color:{text}; }}
[data-testid="stSidebar"] {{ background:{panel}; }}
.block-container {{ padding-top:1.5rem; max-width:1250px; }}
.topbar {{ display:flex; align-items:center; gap:14px; padding:10px 16px; background:{panel};
  border:1px solid {border}; border-radius:{'0' if mode=='Old Reddit' else '12px'}; margin-bottom:12px; }}
.logo {{ color:{accent}; font-weight:800; font-size:1.2rem; }}
.pill {{ background:{accent}; color:#fff !important; border-radius:999px; padding:2px 10px; font-size:.75rem; }}
.meta {{ color:{muted}; font-size:.78rem; }}
.title {{ color:{text}; font-weight:600; line-height:1.25; }}
.flair {{ background:{border}; color:{text}; border-radius:999px; padding:1px 8px; font-size:.7rem; margin-left:6px; }}
.card {{ background:{panel}; border:1px solid {border}; border-radius:14px; padding:14px 16px; }}
.hybrid {{ background:{panel}; border:1px solid {border}; border-radius:10px; padding:{pad}px 10px; }}
.old {{ background:{bg}; border-bottom:1px solid {border}; padding:3px 4px; }}
.old .title {{ color:{link}; font-weight:400; font-size:.95rem; }}
.thumb {{ display:flex; align-items:center; justify-content:center; border-radius:8px; }}
.media {{ height:210px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  font-size:4rem; margin-top:10px; }}
.ad {{ border:1px dashed {accent}; }}
.side {{ background:{panel}; border:1px solid {border}; border-radius:{'0' if mode=='Old Reddit' else '12px'}; padding:12px 14px; margin-bottom:12px; }}
.side h4 {{ margin:0 0 6px 0; font-size:.9rem; }}
.stButton>button {{ border:none; background:transparent; color:{muted}; padding:0 4px; min-height:0; font-size:.8rem; }}
.stButton>button:hover {{ color:{accent}; background:transparent; }}
div[data-testid="stExpander"] {{ border:none; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- helpers
def fmt(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

def vote_button(post, key_suffix):
    v = st.session_state.votes.get(post["id"], 0)
    label = f"{'▲' if v >= 0 else '▼'} {fmt(post['score'] + v)}"
    if st.button(label, key=f"v_{post['id']}_{key_suffix}", help="Upvote? HA this is a draft for a LMC Class buckaroo"):
        st.session_state.votes[post["id"]] = 0 if v == 1 else 1
        st.rerun()

def meta_line(p):
    return f"{p['sub']} · {p['author']} · {p['age']} · 💬 {fmt(p['comments'])}"

def thumb_html(p, size):
    return (f"<div class='thumb' style='width:{size}px;height:{size}px;background:{p['color']}33;"
            f"font-size:{int(size*0.55)}px'>{p['thumb']}</div>")

def mini_preview(p, max_chars=55):
    """One-line teaser shown next to the 'Quick preview' toggle: post type + a short snippet."""
    type_label = {"image": "🖼️ Image", "text": "📝 Text", "link": "🔗 Link"}.get(p["kind"], "")
    snippet = p["body"][:max_chars].rstrip(" ,.;") + "…"
    return f"Quick preview  ·  {type_label}  ·  {snippet}"

# ---------------------------------------------------------------- renderers
def render_old(p):
    c1, c2, c3 = st.columns([1.1, 0.5, 9])
    with c1:
        vote_button(p, "old")
    with c2:
        if show_thumbs:
            st.markdown(thumb_html(p, 28), unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='old'><span class='title'>{p['title']}</span>"
                    f"<span class='flair'>{p['flair']}</span><br><span class='meta'>{meta_line(p)}</span></div>",
                    unsafe_allow_html=True)

def render_card(p):
    ad_cls = " ad" if p["kind"] == "ad" else ""
    media = ""
    if p["kind"] in ("image", "ad"):
        media = f"<div class='media' style='background:{p['color']}33'>{p['thumb']}</div>"
    st.markdown(f"""<div class='card{ad_cls}'>
        <div class='meta'>{meta_line(p)}</div>
        <div class='title' style='font-size:1.25rem;margin-top:4px'>{p['title']}<span class='flair'>{p['flair']}</span></div>
        <div style='margin-top:6px'>{p['body'] if p['kind'] != 'image' else ''}</div>{media}</div>""",
        unsafe_allow_html=True)
    vote_button(p, "card")

def render_hybrid(p):
    ad_cls = " ad" if p["kind"] == "ad" else ""
    c1, c2, c3 = st.columns([1.1, 0.6 if show_thumbs else 0.01, 9])
    with c1:
        vote_button(p, "hyb")
    with c2:
        if show_thumbs:
            st.markdown(thumb_html(p, thumb_px), unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='hybrid{ad_cls}'><span class='title'>{p['title']}</span>"
                    f"<span class='flair'>{p['flair']}</span><br><span class='meta'>{meta_line(p)}</span></div>",
                    unsafe_allow_html=True)
        if p["kind"] != "ad":
            with st.expander(mini_preview(p)):
                if p["kind"] == "image":
                    st.markdown(f"<div class='media' style='background:{p['color']}33;height:160px'>{p['thumb']}</div>",
                                unsafe_allow_html=True)
                st.write(p["body"])
        else:
            # ads have no preview drawer, so add spacing to match the other rows
            st.markdown("<div style='height:21px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------- page
st.markdown(f"""
<div style="height: 20px;"></div>
<div class='topbar'><span class='logo'>Reddit</span>
<span class='meta'>r/whatever</span><span style='flex:1'></span>
<span class='pill'>{mode}</span></div>""", unsafe_allow_html=True)

feed = [p for p in POSTS if flair_filter == "All" or p["flair"] == flair_filter]
if sort == "Top":
    feed.sort(key=lambda p: -p["score"])
elif sort == "Most comments":
    feed.sort(key=lambda p: -p["comments"])
elif sort == "New":
    feed = sorted(feed, key=lambda p: p["id"])
if show_ads and feed:
    feed = feed[:2] + [AD] + feed[2:]

main, side = st.columns([3.2, 1])

with main:
    st.caption(f"{len(feed)} posts in this view")
    renderer = {"Old Reddit": render_old, "New Reddit (Cards)": render_card, "Hybrid (Compact Card)": render_hybrid}[mode]
    for p in feed:
        renderer(p)
        if mode == "New Reddit (Cards)":
            st.write("")
    if not feed:
        st.info("No posts match this flair.")

with side:
    st.markdown(f"""<div class='side'><h4>About r/whatever</h4>
    <div class='meta'>1 member · 1 online</div>
    <div style='margin-top:6px;font-size:.85rem'>it's lmc 3403, what did you expect?</div></div>""",
    unsafe_allow_html=True)
    rules = "".join(f"<div style='font-size:.82rem;margin:3px 0'>{r}</div>" for r in RULES)
    st.markdown(f"<div class='side'><h4>Rules</h4>{rules}</div>", unsafe_allow_html=True)
    st.markdown(
        """<div class='side'>
            <h4>Mod tools</h4>
            <div style='font-size:.82rem'>
                Queue (<b>...</b>), Reports (<b>...</b>), Modmail (<b>...</b>)
            </div>
            <div style='font-size:.5rem; margin-top: .5rem;'>
                im not a mod because i shower this is what i think it looks like
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='side'><h4>Posts visible</h4>"
                f"<div style='font-size:1.6rem;font-weight:700'>{len(feed)}</div>", unsafe_allow_html=True)