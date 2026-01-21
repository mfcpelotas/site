# Arquivo: builder.py
import pandas as pd
from datetime import datetime
import locale

# URL da sua planilha publicada (Substitua pela sua URL real do Google Sheets)
CSV_URL = "SUA_URL_DO_GOOGLE_SHEETS_AQUI"

# Dicionário para tradução de meses (evita problemas de locale no servidor)
MESES = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

def gerar_agenda():
    try:
        # Lê o CSV (espera colunas: data, evento, local, equipe)
        df = pd.read_csv(CSV_URL)
        
        # Converte a coluna data para datetime (esperando formato DD/MM/AAAA)
        df['data_obj'] = pd.to_datetime(df['data'], format='%d/%m/%Y', dayfirst=True)
        
        # Filtra apenas datas futuras ou hoje
        hoje = datetime.now()
        df_futuro = df[df['data_obj'] >= hoje].sort_values('data_obj')

        markdown_output = ""

        if df_futuro.empty:
            markdown_output += "::: {.callout-note}\n## Sem eventos programados\nNo momento não temos eventos futuros na agenda.\n:::\n"
        else:
            # Itera sobre os eventos
            for _, row in df_futuro.iterrows():
                dia = row['data_obj'].day
                mes_extenso = MESES[row['data_obj'].month]
                ano = row['data_obj'].year
                
                # Cria um "Card" visual para cada evento
                markdown_output += f"""
::: {{.card .mb-3}}
::: {{.card-body}}
### 🗓️ {dia} de {mes_extenso}
**{row['evento']}** 📍 *{row['local']}* 👥 Org: {row['equipe']}
:::
:::
"""
        
        # Salva em um arquivo que o Quarto vai incluir
        with open("agenda_component.md", "w", encoding="utf-8") as f:
            f.write(markdown_output)
            print("Agenda atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao gerar agenda: {e}")
        # Cria um arquivo de erro para não quebrar o site
        with open("agenda_component.md", "w", encoding="utf-8") as f:
            f.write(f"::: {{.callout-warning}}\n## Erro na sincronização\nNão foi possível atualizar a agenda.\n:::")

if __name__ == "__main__":
    gerar_agenda()
