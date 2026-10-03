from pathlib import Path
import json
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Flower Studio · Demo', page_icon='🌷', layout='wide')
st.markdown('''<style>
.stApp {background:#fcf8f4;color:#382f32;}
h1,h2,h3 {font-family:Georgia,serif;}
[data-testid="stImage"] img {height:300px;object-fit:contain;background:#f3ece8;border-radius:12px;}
.stButton>button {border-radius:20px;}
</style>''', unsafe_allow_html=True)
st.title('VESSELL 🌷')
st.write('ارسال گل و هدیه از خارج به سراسر ایران')
st.info('فعلا به صورت آزمایشی برای مهشید (نشخین) گیان')
products = json.loads((ROOT / 'products.json').read_text(encoding='utf-8'))
lookup = {p['id']:p for p in products}
if 'cart' not in st.session_state:
    st.session_state.cart = {}

def add(pid):
    cart = st.session_state.cart
    cart[pid] = min(cart.get(pid, 0) + 1, 20)
    st.session_state[f'qty_{pid}'] = cart[pid]

with st.sidebar:
    st.header('سبد خرید')
    for pid in list(st.session_state.cart):
        p = lookup[pid]
        qty = st.number_input(p['name'], min_value=0, max_value=20,
                              value=st.session_state.cart[pid], key=f'qty_{pid}')
        st.session_state.cart[pid] = qty
    total = sum(lookup[pid]['price']*q for pid,q in st.session_state.cart.items())
    st.metric('جمع (USD)', f'${total:.2f}')
    if st.button('خالی کردن سبد'):
        st.session_state.cart = {}
        for key in list(st.session_state):
            if key.startswith('qty_'):
                del st.session_state[key]
        st.rerun()
    st.caption('سبد موقتی که بعدا به درگاه پرداخت وصل کنیم')

query = st.text_input('جست‌وجوی گل', placeholder='مثلاً صورتی یا بنفش')
items = [p for p in products if query.strip().casefold() in (p['name']+' '+p['description']).casefold()]
for start in range(0,len(items),3):
    cols = st.columns(3)
    for col,p in zip(cols,items[start:start+3]):
        with col:
            with st.container(border=True):
                st.image(str(ROOT/'images'/p['image']))
                st.subheader(p['name'])
                st.write(p['description'])
                st.caption(f"قیمت نمونه: ${p['price']:.2f}")
                st.button('افزودن به سبد', key=f"add_{p['id']}", on_click=add, args=(p['id'],), use_container_width=True)
if not items:
    st.write('محصولی با این نام پیدا نشد.')
st.divider()
if st.button('مشاهده خلاصه سبد آزمایشی'):
    rows = [{'product':lookup[pid]['name'],'quantity':q,'subtotal_usd':lookup[pid]['price']*q}
            for pid,q in st.session_state.cart.items() if q]
    if rows:
        st.dataframe(rows, use_container_width=True)
        st.success('این فقط پیش‌نمایش سبد است؛ سفارشی ارسال نشده است')
    else:
        st.warning('سبد خالی است')
