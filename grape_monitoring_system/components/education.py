import streamlit as st
import os


@st.cache_data(ttl=3600)
def load_fungicide_data(force_refresh=False):
    try:
        if force_refresh:
            st.cache_data.clear()

        from scrape_data import get_grape_data_smart

        with st.spinner("📊 Fungisit verileri yükleniyor..."):
            df = get_grape_data_smart(force_refresh=force_refresh)
            if df is not None and not df.empty:
                df = df.dropna(how='all').reset_index(drop=True)
                st.success(f"✅ {len(df)} kayıt başarıyla yüklendi!")
                return df
            return None
    except ImportError:
        st.error("❌ scrape_data.py dosyası bulunamadı!")
        return None
    except Exception as e:
        st.error(f"❌ Veri yükleme hatası: {e}")
        return None


def education_component(perform_web_search_func):
    st.header("📚 Bilgi Bankası / Eğitim Modülü")
    st.markdown("Bağcılık, hastalıklar ve ilaçlar hakkında eğitim içerikleri.")

    tab2, tab3 = st.tabs(["🌐 Web Araması", "🧪 Fungisit Veritabanı"])

    with tab2:
        st.subheader("🔍 Online Makale Araması")
        search_query = st.text_input("Aramak istediğiniz konu girin (örn: üzüm mildiyö tedavisi):", placeholder="Mildiyö")
        if st.button("🌐 Web'de Ara"):
            if search_query:
                with st.spinner(f"'{search_query}' konusu için web araması yapılıyor..."):
                    try:
                        results = perform_web_search_func(search_query)
                        if results:
                            st.subheader("🔍 Arama Sonuçları:")
                            for res in results:
                                st.markdown(f"- [{res['title']}]({res['url']})")
                        else:
                            st.info("Arama sonuç bulunamadı.")
                    except Exception as e:
                        st.error(f"Web araması sırasında bir hata oluştu: {e}")
            else:
                st.warning("Lütfen bir arama konusu girin.")

    with tab3:
        st.subheader("🧪 Fungisit Etkinlik Veritabanı")
        st.markdown("**UMass Üniversitesi'nden çekilen güncel fungisit verileri**")
        df = load_fungicide_data()
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=400, hide_index=True)
        else:
            st.warning("Veri yüklenemedi veya boş.")

 