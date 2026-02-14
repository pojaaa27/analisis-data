```python
import streamlit as st

st.title("Demo")

angka = st.slider("Pilih angka", 0, 100)
st.write("Angka yang dipilih:", angka)

```