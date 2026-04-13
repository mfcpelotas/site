# Arquivo: builder.py atualizado
import pandas as pd
from datetime import datetime, timedelta
import locale

# URL da sua planilha publicada (Substitua pela sua URL real do Google Sheets)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQe2uTE5GpiMPKIzFzv3kzuLAj-covtjG7bur7XcJ4wWEUStq2qXQvek-lEeDB04FLqbWwzcRGI86Z/pub?gid=0&single=true&output=csv"

# Dicionário para tradução de meses (evita problemas de locale no servidor)
MESES = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

def gerar_agenda():
    try:
        df = pd.read_csv(CSV_URL)
        df['data_obj'] = pd.to_datetime(df['data'], format='%d/%m/%Y', dayfirst=True)
        
        hoje = datetime.now()
        
        # --- NOVIDADE: Definindo o limite de 45 dias ---
        limite_futuro = hoje + timedelta(days=45)
        
        # Filtra eventos entre hoje e o limite de 45 dias
        df_futuro = df[
            (df['data_obj'] >= hoje) & 
            (df['data_obj'] <= limite_futuro)
        ].sort_values('data_obj')
        # -----------------------------------------------

        markdown_output = ""

        if df_futuro.empty:
            markdown_output += "::: {.callout-note}\n## Agenda\nNão há eventos programados para os próximos 45 dias.\n:::\n"
        else:
            # Mantemos a mesma lógica de construção visual dos cards
            for _, row in df_futuro.iterrows():
                dia = row['data_obj'].day
                mes_extenso = MESES[row['data_obj'].month]
                
                markdown_output += f"""
::: {{.card .mb-3}}
::: {{.card-body}}
### 🗓️ {dia} de {mes_extenso}
**{row['evento']}** 📍 *{row['local']}* 👥 Org: {row['equipe']}
:::
:::
"""
        
        with open("agenda_component.md", "w", encoding="utf-8") as f:
            f.write(markdown_output)
            print(f"Agenda filtrada (próximos 45 dias) gerada com sucesso!")

    except Exception as e:
        print(f"Erro ao gerar agenda: {e}")
        with open("agenda_component.md", "w", encoding="utf-8") as f:
            f.write("::: {.callout-warning}\n## Erro na sincronização\nNão foi possível atualizar a agenda.\n:::")

if __name__ == "__main__":
    gerar_agenda()
