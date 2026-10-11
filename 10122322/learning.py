import streamlit as st
from streamlit_option_menu import option_menu

# SIDEBAR MENU
with st.sidebar:
    selected = option_menu(
         "Hitung Luas", ["Persegi Panjang", 
                        "Lingkaran"
        ], 
        icons = ['gear', 'gear'], 
        menu_icon = "house", 
        default_index = 0
        )
    
# MENU PERSEGI PANJANG
if(selected == "Persegi Panjang"):
    st.title("Hitung Luas Persegi Panjang")

    P = st.number_input("nilai panjang | CM", 0)
    L = st.number_input("nilai lebar | CM", 0)
    hitung = st.button("Hitung Luas")

    if hitung:
        luas = P * L
        st.write("Luas Persegi Panjang adalah ", luas)
        st.success(f"Jadi Hasil Luas Persegi Panjang {luas} CM")

# MENU LINGKARAN
elif(selected == "Lingkaran"):
    st.title("Hitung Luas Lingkaran")

    r = st.slider("Jari-jari Lingkaran", 0, 100)
    phi = st.text_input(
        "Phi",
        placeholder="3.14",
        disabled=True)
    hitung = st.button("Hitung Luas")

    if(hitung):
        luas = 3.14 * r * r
        st.write("Luas Lingkaran adalah ", luas)
        st.success(f"Jadi Hasil Luas Lingkaran adalah {luas}")
