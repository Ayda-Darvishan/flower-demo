from pathlib import Path
import base64
import html
import json
import mimetypes
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='VESSELL · Flower Studio', page_icon='🌷', layout='wide')

# All product content is escaped before insertion into HTML.
def esc(value):
    return html.escape(str(value), quote=True)

@st.cache_data(show_spinner=False)
def image_url(path, modified):
    file = Path(path)
    mime = mimetypes.guess_type(file.name)[0] or 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(file.read_bytes()).decode()

def photo(product):
    path = ROOT / 'images' / product['image']
    return image_url(str(path), path.stat().st_mtime_ns) if path.is_file() else ''

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Vazirmatn:wght@400;500;600;700&display=swap');
:root { --ink:#283c34; --muted:#788279; --rose:#b66c7d; --line:#e6e5dd; --paper:#fbfaf6; }
.stApp { background:var(--paper); color:var(--ink); }
html, body, [class*="css"], .stApp, input, button, textarea, select {
    font-family:'DM Sans','Vazirmatn',sans-serif;
}
[data-testid="stMainBlockContainer"] { max-width:1440px; padding-top:4.5rem; padding-bottom:3rem; }
[data-testid="stHeader"] { background:rgba(251,250,246,.92); }
h1,h2,h3,p { color:var(--ink); }
.v-nav { display:flex; align-items:center; justify-content:space-between; gap:20px;
    padding:0 0 25px; border-bottom:1px solid var(--line); margin-bottom:25px; }
.v-logo { font-family:Georgia,serif; font-size:30px; letter-spacing:5px; }
.v-logo small { display:block; font-family:'DM Sans',sans-serif; font-size:9px;
    letter-spacing:3px; color:var(--muted); margin-top:4px; }
.v-nav-note { direction:rtl; font-size:13px; color:var(--muted); }
.v-nav-cart { font-size:11px; letter-spacing:1.5px; border:1px solid var(--line);
    border-radius:30px; padding:10px 16px; white-space:nowrap; }
.v-hero { display:grid; grid-template-columns:1.05fr 1fr; min-height:445px;
    background:#edf0e7; border-radius:24px; overflow:hidden; margin-bottom:16px; }
.v-hero-text { padding:48px 45px; display:flex; flex-direction:column; justify-content:center; }
.v-eyebrow { font-size:10px; font-weight:700; letter-spacing:3px; color:#687864; margin-bottom:18px; }
.v-hero h1 { font-family:Georgia,serif; font-weight:400; font-size:clamp(38px,4.5vw,65px);
    line-height:1.08; margin:0 0 17px; letter-spacing:-2px; }
.v-hero h1 em { font-weight:400; color:var(--rose); }
.v-hero-fa { direction:rtl; text-align:left; font-family:'Vazirmatn',sans-serif;
    font-size:18px; line-height:1.9; margin:0 0 10px; }
.v-hero-sub { font-size:14px; color:#718071; line-height:1.8; max-width:360px; margin-bottom:25px; }
.v-cta { align-self:flex-start; text-decoration:none!important; background:#304d3e;
    color:white!important; border-radius:30px; padding:13px 22px; font-size:13px; }
.v-hero-art { position:relative; min-height:445px; background:#ead9d6; }
.v-hero-art img { width:100%; height:100%; position:absolute; object-fit:cover; object-position:center; }
.v-art-caption { position:absolute; bottom:20px; left:20px; background:rgba(255,255,255,.9);
    padding:12px 17px; border-radius:12px; font-size:12px; direction:rtl; }
.v-demo { direction:rtl; text-align:center; color:#926b73; background:#f6ecec;
    border:1px solid #efdddd; padding:10px 14px; border-radius:12px; font-size:12px; margin-bottom:30px; }
.v-section { display:flex; justify-content:space-between; align-items:end; margin:12px 0 14px; }
.v-section h2 { font-family:Georgia,serif; font-size:34px; font-weight:400; margin:0; }
.v-section p { font-size:12px; direction:rtl; color:var(--muted); margin:0; }
[data-testid="stTextInput"] input { direction:rtl; }
[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stSelectbox"] [data-baseweb="select"]>div { border-radius:12px; background:#fff; border-color:var(--line); }
[data-testid="stVerticalBlockBorderWrapper"]>div { border-radius:18px!important; border-color:var(--line)!important;
    background:#fff; overflow:hidden; box-shadow:0 5px 20px rgba(35,48,39,.035); }
.v-product-photo { position:relative; height:290px; background:#f3eee9; border-radius:12px; overflow:hidden; }
.v-product-photo img { height:100%; width:100%; object-fit:contain; transition:transform .45s ease; }
.v-product-photo:hover img { transform:scale(1.045); }
.v-product-badge { position:absolute; left:12px; top:12px; background:rgba(255,255,255,.92);
    padding:6px 10px; border-radius:20px; color:#6d756d; font-size:9px; letter-spacing:1.5px; }
.v-product-title { direction:rtl; text-align:right; font-weight:600; font-size:19px; margin:17px 0 8px; }
.v-product-desc { direction:rtl; text-align:right; font-size:12px; line-height:1.9;
    color:var(--muted); min-height:46px; margin:0 0 15px; }
.v-product-price { display:flex; justify-content:space-between; align-items:center;
    border-top:1px solid #efeee9; padding-top:13px; margin-bottom:4px; }
.v-price { font-size:22px; font-weight:600; color:#304d3e; }
.v-price-note { direction:rtl; font-size:10px; color:#9a9e94; }
.stButton>button { border-radius:30px!important; border:1px solid #d3ded3;
    background:#eff3ec; color:#304d3e; font-family:'Vazirmatn','DM Sans',sans-serif;
    font-size:13px; min-height:43px; transition:all .2s; }
.stButton>button:hover { background:#304d3e; color:#fff; border-color:#304d3e; }
.stButton>button[kind="primary"] { background:#304d3e; color:white; border-color:#304d3e; }
[data-testid="stSidebar"] { background:#f0f2eb; border-right:1px solid #e2e5db; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top:28px; }
.v-bag-title { font-family:Georgia,serif; font-size:30px; margin:0; }
.v-bag-sub { direction:rtl; color:var(--muted); font-size:12px; margin:9px 0 22px; }
.v-empty { text-align:center; border:1px dashed #cbd4c7; border-radius:18px;
    padding:30px 14px; color:#7d8877; font-size:13px; direction:rtl; }
.v-empty span { display:block; font-size:35px; margin-bottom:12px; }
.v-cart-name { direction:rtl; font-size:14px; text-align:right; margin-bottom:2px; }
.v-cart-price { font-size:11px; color:var(--muted); text-align:right; }
.v-total { border-top:1px solid #d8dfd2; padding-top:18px; margin-top:18px;
    display:flex; align-items:center; justify-content:space-between; }
.v-total strong { font-family:Georgia,serif; font-size:30px; font-weight:400; }
.v-total span { font-size:13px; }
.v-footer { border-top:1px solid var(--line); margin-top:35px; padding-top:25px;
    display:flex; align-items:center; justify-content:space-between; gap:15px; }
.v-footer strong { font-family:Georgia,serif; letter-spacing:3px; }
.v-footer span { color:var(--muted); font-size:11px; }
@media(max-width:800px) {
    [data-testid="stMainBlockContainer"] { padding:4.5rem 1rem 2rem; }
    .v-nav-note { display:none; }
    .v-logo { font-size:24px; }
    .v-hero { grid-template-columns:1fr; }
    .v-hero-text { padding:30px 25px; }
    .v-hero-art { min-height:300px; }
    .v-hero h1 { font-size:45px; }
    .v-section { flex-direction:column; align-items:start; gap:8px; }
    .v-footer { flex-direction:column; align-items:start; }
}

.stButton > button[kind="primary"], .stButton > button[kind="primary"] * {color:white!important;}
.stButton > button:hover * {color:white!important;}
.st-key-navigation_bar {background:#f0f2eb; border:1px solid #d8dfd2; border-radius:14px; padding:12px 16px; margin-bottom:20px;}
.st-key-navigation_bar [role="radiogroup"] {gap:24px; flex-wrap:wrap;}
.st-key-navigation_bar label p {font-weight:600; color:#304d3e;}
.v-cart-photo {height:150px; object-fit:contain; width:100%; background:#f3eee9; border-radius:12px;}
@media(max-width:640px) {
    [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important; flex:1 1 100%!important; min-width:0!important;}
    .v-nav-cart {font-size:10px;padding:9px;}
    .v-product-photo {height:310px;}
}
</style>''', unsafe_allow_html=True)

try:
    products = json.loads((ROOT / 'products.json').read_text(encoding='utf-8'))
except (OSError, json.JSONDecodeError) as error:
    st.error(f'Cannot load products.json: {error}')
    st.stop()
lookup = {str(p['id']):p for p in products}
if 'cart' not in st.session_state:
    st.session_state.cart = {}
# Remove stale IDs if the catalogue has changed.
st.session_state.cart = {str(pid):int(q) for pid,q in st.session_state.cart.items() if str(pid) in lookup}

def add(pid):
    current = int(st.session_state.cart.get(pid, 0))
    st.session_state.cart[pid] = min(current + 1, 20)
    st.session_state[f'qty_{pid}'] = st.session_state.cart[pid]
    st.toast('به سبد اضافه شد؛ برای تغییر یا حذف، «سبد خرید» را انتخاب کنید.', icon='🌷')

def remove_item(pid):
    st.session_state.cart.pop(pid, None)
    st.session_state[f'qty_{pid}'] = 0


def go_cart():
    st.session_state['navigation'] = 'cart'


def go_catalog():
    st.session_state['navigation'] = 'catalog'


def update_quantity(pid):
    st.session_state.cart[pid] = int(st.session_state[f'qty_{pid}'])

def clear_cart():
    st.session_state.cart = {}
    for key in list(st.session_state):
        if key.startswith('qty_'):
            del st.session_state[key]

def render_cart():
    st.markdown('<div class="v-bag-title">Your little garden</div><div class="v-bag-sub">سبد خرید شما · انتخاب‌هایی با عشق</div>', unsafe_allow_html=True)
    active = [pid for pid,q in st.session_state.cart.items() if q>0]
    if not active:
        st.markdown('<div class="v-empty"><span>♡</span>هنوز گلی انتخاب نکرده‌اید.<br>از مجموعه، گل دلخواهتان را اضافه کنید.</div>', unsafe_allow_html=True)
    for pid in active:
        p = lookup[pid]
        a,b = st.columns([1,2.2])
        with a:
            path = ROOT/'images'/p['image']
            if path.is_file():
                st.markdown(f'<img class="v-cart-photo" src="{photo(p)}" alt="{esc(p["name"])}">', unsafe_allow_html=True)
        with b:
            st.markdown(f'<div class="v-cart-name">{esc(p["name"])}</div><div class="v-cart-price">${float(p["price"]):,.2f} / item</div>', unsafe_allow_html=True)
            key = f'qty_{pid}'
            if key not in st.session_state:
                st.session_state[key] = st.session_state.cart[pid]
            st.number_input(f'تعداد {p["name"]}', min_value=0, max_value=20,
                            key=key, on_change=update_quantity, args=(pid,), label_visibility='visible')
            st.button('حذف از سبد ×', key=f'remove_{pid}', on_click=remove_item, args=(pid,), use_container_width=True)
    total = sum(float(lookup[pid]['price'])*q for pid,q in st.session_state.cart.items())
    st.markdown(f'<div class="v-total"><span>جمع سبد · USD</span><strong>${total:,.2f}</strong></div>', unsafe_allow_html=True)
    st.write('')
    show_summary = st.button('مشاهده خلاصه سبد  ↗', type='primary', use_container_width=True)
    st.button('خالی کردن سبد', on_click=clear_cart, use_container_width=True, disabled=not active)
    st.caption('سبد موقتی که بعدا به درگاه پرداخت وصل کنیم')
    st.button('بازگشت به گل‌ها', key='back_to_flowers', on_click=go_catalog, use_container_width=True)
    return show_summary

count = sum(st.session_state.cart.values())
st.markdown(f'''<div class="v-nav"><div class="v-logo">VESSELL<small>SENDING LOVE HOME</small></div>
<div class="v-nav-note">گل‌های کوچک، احساس‌های بزرگ</div><div class="v-nav-cart">YOUR BAG &nbsp; / &nbsp; {count:02d}</div></div>''', unsafe_allow_html=True)
with st.container(key='navigation_bar'):
    page = st.radio('انتخاب صفحه', ['catalog', 'cart'],
                    format_func=lambda value: '🌷 مجموعه گل‌ها' if value == 'catalog' else '🛍️ سبد خرید',
                    key='navigation', horizontal=True, label_visibility='collapsed')
if page == 'cart':
    show_summary = render_cart()
    if show_summary:
        st.subheader('خلاصه سبد آزمایشی')
        rows = [{'محصول':lookup[pid]['name'],'تعداد':q,'جمع (USD)':float(lookup[pid]['price'])*q}
                for pid,q in st.session_state.cart.items() if q]
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
            st.success('این فقط پیش‌نمایش سبد است؛ سفارشی ارسال نشده است')
        else:
            st.warning('سبد خالی است')
    st.stop()

hero = photo(products[2] if len(products)>2 else products[0]) if products else ''
hero_image = f'<img src="{hero}" alt="دسته گل صورتی">' if hero else ''
st.markdown(f'''<section class="v-hero"><div class="v-hero-text"><div class="v-eyebrow">A LITTLE FLOWER. A LOT OF LOVE.</div>
<h1>Beautiful things.<br><em>Closer hearts.</em></h1><p class="v-hero-fa">ارسال گل و هدیه از خارج به سراسر ایران</p>
<div class="v-hero-sub">You’re far away. Your love doesn’t have to be.<br>A thoughtful little gift, chosen with love.</div>
<a class="v-cta" href="#collection">مشاهده مجموعه &nbsp; ↗</a></div><div class="v-hero-art">{hero_image}<div class="v-art-caption">یک دسته گل، هزار حرف نگفته ♡</div></div></section>
<div class="v-demo">فعلا به صورت آزمایشی برای مهشید (نشخین) گیان</div>
<div class="v-section" id="collection"><h2>The flower collection</h2><p>گل دلخواهتان را انتخاب کنید</p></div>''', unsafe_allow_html=True)

search_col, sort_col = st.columns([2,1])
with search_col:
    query = st.text_input('جست‌وجوی گل', placeholder='نام یا رنگ گل را جست‌وجو کنید…')
with sort_col:
    sort = st.selectbox('مرتب‌سازی', ['ترتیب مجموعه','قیمت: کم به زیاد','قیمت: زیاد به کم'])
items = [p for p in products if query.strip().casefold() in (p['name']+' '+p['description']).casefold()]
if sort != 'ترتیب مجموعه':
    items = sorted(items, key=lambda p:float(p['price']), reverse=sort=='قیمت: زیاد به کم')
st.caption(f'{len(items)} گل در مجموعه · قیمت‌ها به دلار آمریکا')
for start in range(0,len(items),3):
    cols = st.columns(3, gap='medium')
    for col,p in zip(cols,items[start:start+3]):
        pid = str(p['id'])
        with col:
            with st.container(border=True):
                src = photo(p)
                picture = f'<img src="{src}" alt="{esc(p["name"])}" loading="lazy">' if src else '<p>تصویر موجود نیست</p>'
                st.markdown(f'''<div class="v-product-photo">{picture}<span class="v-product-badge">FLOWER STUDIO</span></div>
<div class="v-product-title">{esc(p['name'])}</div><div class="v-product-desc">{esc(p['description'])}</div>
<div class="v-product-price"><span class="v-price">${float(p['price']):,.2f}</span><span class="v-price-note">USD · قیمت نمونه</span></div>''', unsafe_allow_html=True)
                amount = st.session_state.cart.get(pid,0)
                label = f'افزودن به سبد  +  ·  {amount} در سبد' if amount else 'افزودن به سبد  +'
                st.button(label, key=f'add_{pid}', on_click=add, args=(pid,), use_container_width=True, disabled=amount>=20)
                if amount:
                    st.button('حذف از سبد ×', key=f'catalog_remove_{pid}', on_click=remove_item, args=(pid,), use_container_width=True)
if not items:
    st.info('محصولی پیدا نشد. نام یا رنگ دیگری را امتحان کنید.')

st.button(f'مشاهده سبد خرید ({count}) 🛍️', key='catalog_cart_link', on_click=go_cart, type='primary', use_container_width=True)
st.markdown('<footer class="v-footer"><strong>VESSELL</strong><span>Sending love home. One little flower at a time.</span><span>گل‌های کوچک، احساس‌های بزرگ ♡</span></footer>', unsafe_allow_html=True)
