import pandas as pd
import streamlit as st
import io

def elabora_multipli_file():
    st.title("Elaboratore Riepilogo Multi-mese")

    # Sostituisce filedialog.askopenfilenames
    uploaded_files = st.file_uploader("Seleziona i file CSV dei mesi", type="csv", accept_multiple_files=True)

    if not uploaded_files:
        st.info("Inizia caricando uno o più file CSV.")
        return

    dati_mesi = {}
    
    try:
        for uploaded_file in uploaded_files:
            # Lettura file caricato
            df = pd.read_csv(uploaded_file, sep=';', decimal=',', index_col=False)
            
            df['Giorno'] = pd.to_datetime(df['Giorno'], format='%d/%m/%Y')
            df['Somma_Giornaliera'] = df.iloc[:, 1:].sum(axis=1) 
            
            periodo = df['Giorno'].dt.to_period('M').iloc[0]
            df['Day'] = df['Giorno'].dt.day
            dati_mesi[periodo] = df.set_index('Day')['Somma_Giornaliera']

        periodi_ordinati = sorted(dati_mesi.keys())
        df_finale = pd.DataFrame(index=range(1, 32))
        df_finale.index.name = 'Giorno'

        for p in periodi_ordinati:
            nome_col = p.strftime('%m/%Y')
            df_finale[nome_col] = dati_mesi[p]

        totali_mensili = df_finale.sum()
        riga_totali = pd.DataFrame([totali_mensili], columns=df_finale.columns, index=['TOTALE MENSILE'])
        df_risultato = pd.concat([df_finale, riga_totali])

        totale_generale = totali_mensili.sum()
        df_risultato['TOTALE GENERALE'] = ""
        df_risultato.at['TOTALE MENSILE', 'TOTALE GENERALE'] = totale_generale

        # Visualizza anteprima
        st.write("Anteprima Risultato:", df_risultato)

        # Sostituisce filedialog.asksaveasfilename (Download via Browser)
        towrite = io.BytesIO()
        df_risultato.to_excel(towrite, index=True)
        towrite.seek(0)
        
        st.download_button(
            label="Scarica File Excel",
            data=towrite,
            file_name="riepilogo_multi_mese.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Errore durante l'elaborazione: {e}")

if __name__ == "__main__":
    elabora_multipli_file()
