import streamlit as st
from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict

st.set_page_config(page_title="Form Kritik dan Saran Kelurahan Kalitirto")
markdown = utils.set_markdown()

st.title("Form Kritik dan Saran")
with st.container(border=False):
    st.write("Silakan isi form di bawah ini untuk memberikan kritik dan saran Anda. " \
    "Kami sangat menghargai masukan Anda untuk meningkatkan pelayanan kami. Terima kasih atas partisipasi Anda!")
    st.container(height=5, border=False)
    user_input = st.chat_input("Say something")
    if user_input:
        st.toast("Terima kasih atas kritik dan saran Anda!")
        prediction = predict.predict(user_input).lower()
        data = {
            "feedback": user_input,
            "prediction": prediction,
        }
        repo.insert_data(data)

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Statistik Sentimen")
with col2:
    filter_date = st.date_input("Pilih tanggal", value=date.today(), format="DD-MM-YYYY", label_visibility="collapsed")
    start_date = datetime.combine(filter_date, time.min).isoformat()
    end_date = datetime.combine(filter_date, time.max).isoformat()

positive = repo.get_count_by_prediction("positif", start_date, end_date)
neutral = repo.get_count_by_prediction("netral", start_date, end_date)
negative = repo.get_count_by_prediction("negatif", start_date, end_date)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Positif", value=positive, delta=None, help="Positive feedback")
    st.markdown('<div class="stMetricValue-positif"></div>', unsafe_allow_html=True)
with col2:  
    st.metric(label="Netral", value=neutral, delta=None, help="Netral feedback")
    st.markdown('<div class="stMetricValue-netral"></div>', unsafe_allow_html=True)
with col3:
    st.metric(label="Negatif", value=negative, delta=None, help="Negative feedback")
    st.markdown('<div class="stMetricValue-negatif"></div>', unsafe_allow_html=True)

st.container(height=30, border=False)

feedback_history = repo.get_feedback_history(start_date, end_date)
if feedback_history:
    data = utils.process_feedback_history(feedback_history)
    st.dataframe(data, use_container_width=True, hide_index=True, height=400)
else:
    st.warning("Tidak ada data untuk tanggal ini.")