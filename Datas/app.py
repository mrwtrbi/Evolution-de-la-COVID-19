import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from bokeh.plotting import figure

st.set_page_config(page_icon="🔍", layout="wide", page_title="Evolution de la COVID 19")

PAGE_CONFIG = {"page_title":"Marwa's & Sithursha's Project", "page_icon":"smiley", "layout":"centered" }

DATA_PATH = '/content/drive/MyDrive/STID2022_-_Evolution_de_la_COVID_19/Datas/Database.csv'
DATE_COLUMN ='date'

# Load data
@st.cache
def load_data():
  data = pd.read_csv(DATA_PATH, sep=",", header=0, encoding='utf-8')
  data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
  return data

data = load_data()

# Sep for figures
def thousand_sep(num):
    return ("{:,}".format(num))

# Widgets data
countries = []
for country in data['country']:
  countries.append(country)
countries = list(set(countries))

date_min = min(data['date'])
date_max = max(data['date'])

# Import images
img_Marwa = '/content/drive/MyDrive/STID2022_-_Evolution_de_la_COVID_19/Datas/Marwa.jpg'
img_Sithursha = '/content/drive/MyDrive/STID2022_-_Evolution_de_la_COVID_19/Datas/Sithursha.jpg'
logo =  '/content/drive/MyDrive/STID2022_-_Evolution_de_la_COVID_19/Datas/Logo projet S4.png'

def main():
  
  t1, t2 = st.columns((0.1,1)) 
  t1.image(logo, width = 100)
  t2.title("Bienvenue sur le Tableau de bord COVID 19 :earth_africa:")
  t2.text("Vous vous demandez comment évolue la situation sanitaire dans le Monde ? On vous répond !")

  menu = ["Pourquoi ce tableau de bord ?","La situation sanitaire mondiale", "Classement des pays",
          "Zoomons sur un pays"]

  choice = st.sidebar.radio('Menu', menu)
    
  if choice == 'Pourquoi ce tableau de bord ?':
    st.header("L'histoire du tableau de bord")
    st.text("""
    Avec ce tableau de bord, vous pourrez voir les données de manière simple et ludique. Beaucoup de sites web et applications nous permettent déjà de consulter
    les données de la pandémie, mais les données ne sont pas assez mises en valeur. Notre but est de faire en sorte que l'appréciation des données
    soit agréable et captivante.
    """)

    st.markdown(""" 
    ### Qui sommes-nous ?

    Nous sommes deux étudiantes en deuxième année de DUT STID (Statistiques et Traitement Informatique des Données).
    """)

    intro_marwa = st.write("**Etudiante n°1 :**")
    col1, mid, col2 = st.columns([20,1,50])
    with col1:
      st.image(img_Marwa, width=350)
    with col2:
      st.write("""Je m'appelle Marwa ! Dans ce projet, je me suis occupée de la rédaction du cahier des charges et du 
      développement du site web. Ce qui m'a le plus plu dans ce que j'ai fait, c'est d'observer l'avancement du site web.
      Cela m'a procuré beaucoup de satisfaction et je suis fière du résultat !""")
    
    intro_sithursha = st.write("**Etudiante n°2 :**")
    col1, mid, col2 = st.columns([50,1,20])
    with col1:
      st.write("""Moi c'est Sithursha ! Je me suis occupée de la base de données. J'ai traité les données manquantes,
      ajouter des colonnes pour les données géographiques de chaque pays (continents, latitude et longitude) et fusionner nos différentes
      sources de données.""")
    with col2:
      st.image(img_Sithursha, width=350)

    st.markdown("""
    ### D'où nous est venue l'idée de créer un tableau de bord de la COVID 19 ?

    Au troisième semestre de notre formation, nous avions créer une application Shiny en langage R
    qui permettait de visualiser les données hospitalières françaises.
    Cela nous a énormément plu donc nous nous sommes lancées le défi de créer des visualisations intéractives dans
    un autre langage de programmation :sparkles: Python :sparkles:.

    Sur TousAnti Covid, application de l'Etat, il y a la possibilité de consulter les donneés relatives
    à la pandémie. Nous étions très frustrées de voir que les données n'étaient pas mise en valeur par
    l'application. De plus, ces données sont dans l'ombre de l'option qui permet d'avoir son pass
    sanitaire à tout moment sur soi.

    Notre coeur de métier étant le traitement et la visualisation de données, nous ne nous pouvions pas 
    rester devant cette injustice sans rien faire.

    C'est donc de là qu'est partie notre idée de créer un tableau de bord de la COVID 19 !

    Nous nous sommes dit qu'observer la situation sanitaire française était bien mais observer la
    situation sanitaire mondiale est encore mieux ! 

    Nous avons donc décider de faire un tableau de bord de l'évolution de la situation sanitaire mondiale :sunglasses::earth_africa:.

    ### Quel est l'intérêt de créer un tableau de bord en Python ?

    Il y a tout d'abord l'outil "tableau de bord" en lui-même qui est plaisant, l'interactivité nous permet
    de "voyager" dans les données.

    Ensuite, nous souhaitons à l'issue de ce projet, monter en compétences dans ce vaste langage de programmation qui est Python.
    Le package Streamlit, qui permet de créer un site et faire des visualisations intéractives des données, nous servira dans notre
    vie professionnelle future car nos projets professionnelles tournent autour de la représentation des données autrement appelée la 
    :sparkles:**Data Visualization**:sparkles:.
    
    ### De quoi nous sommes-nous inspirées pour créer ce tableau de bord ?

    Pour réaliser ce tableau de bord, nous nous sommes inspirées de plusieurs sites/applications dont
    voici les liens :
    """)

    st.write("Covid Visualizer : https://www.covidvisualizer.com/")
    st.write("Tous AntiCovid : https://www.gouvernement.fr/info-coronavirus/tousanticovid")
    st.write("Worldometer : https://www.worldometers.info/coronavirus/")
    st.write("WHO (World Health Organization) : https://covid19.who.int/table")

  # Situation sanitaire mondiale

  if choice == 'La situation sanitaire mondiale' :
    st.header('Comment évolue la situation sanitaire dans le monde ?')

    regions = st.multiselect("Je veux voir la situation sanitaire ...", ("dans le monde entier", "en Afrique","en Asie",
                                                                         "en Amérique du Nord", "en Amérique du Sud", "en Europe",
                                                                         "en Océanie"), default='dans le monde entier')

    viz = st.radio("Je souhaite observer...", ('Le nombre de cas positifs à la COVID',
                                               'Le nombre de cas positifs à la COVID (en cas cumulés)',
                                               'Le nombre de morts', 'Le nombre de morts (en morts cumulées)',
                                               'La vaccination'))

    if viz == "Le nombre de cas positifs à la COVID":      
      p = figure(
              title="Nombre de cas positifs à la COVID",
              x_axis_label='Date',
              x_axis_type='datetime',
              y_axis_label='Nombre de cas positifs à la COVID'
          )
      
      for region in regions:
        if region == "dans le monde entier": 
          
          df = data[["date", "New_cases"]].groupby(["date"]).sum().reset_index()
    
          p.line(df["date"], df["New_cases"], legend_label="dans le monde entier", color="black", line_width=2)
    
        elif region == "en Afrique":
          df = data[data["continents"] == "Afrique"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label="en Afrique", color="red", line_width=2)

        elif region == "en Asie":
          df = data[data["continents"] == "Asie"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label='en Asie', line_width=2, color='green')

        elif region == "en Amérique du Nord":
          df = data[data["continents"] == "Amérique du Nord"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label='en Amérique du Nord', line_width=2, color='purple')
        
        elif region == "en Amérique du Sud":
          df = data[data["continents"] == "Amérique du Sud"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label='en Amérique du Sud', line_width=2, color='brown')

        elif region == "en Europe":
          df = data[data["continents"] == "Europe"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label='en Europe', line_width=2, color='blue')

        elif region == "en Océanie":
          df = data[data["continents"] == "Océanie"][["date", "New_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_cases"], legend_label='en Océanie', line_width=2, color='orange')
    
      p.legend.location = "top_left"
      st.bokeh_chart(p, use_container_width=True)
    
    elif viz == "Le nombre de cas positifs à la COVID (en cas cumulés)":      
      p = figure(
              title="Le nombre de cas cumulés positifs à la COVID",
              x_axis_label='Date',
              x_axis_type='datetime',
              y_axis_label='Le nombre de cas cumulés positifs à la COVID'
          )
      
      for region in regions:
        if region == "dans le monde entier": 
          
          df = data[["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
    
          p.line(df["date"], df["Cumulative_cases"], legend_label="dans le monde entier", color="black", line_width=2)
    
        elif region == "en Afrique":
          df = data[data["continents"] == "Afrique"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label="en Afrique", color="red", line_width=2)

        elif region == "en Asie":
          df = data[data["continents"] == "Asie"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label='en Asie', line_width=2, color='green')

        elif region == "en Amérique du Nord":
          df = data[data["continents"] == "Amérique du Nord"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label='en Amérique du Nord', line_width=2, color='purple')
        
        elif region == "en Amérique du Sud":
          df = data[data["continents"] == "Amérique du Sud"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label='en Amérique du Sud', line_width=2, color='brown')

        elif region == "en Europe":
          df = data[data["continents"] == "Europe"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label='en Europe', line_width=2, color='blue')

        elif region == "en Océanie":
          df = data[data["continents"] == "Océanie"][["date", "Cumulative_cases"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_cases"], legend_label='en Océanie', line_width=2, color='orange')
    
      p.legend.location = "top_left"
      st.bokeh_chart(p, use_container_width=True)
    
    elif viz == "Le nombre de morts":      
      p = figure(
              title="Nombre de morts",
              x_axis_label='Date',
              x_axis_type='datetime',
              y_axis_label='Nombre de morts'
          )
      
      for region in regions:
        if region == "dans le monde entier": 
          
          df = data[["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
    
          p.line(df["date"], df["New_deaths"], legend_label="dans le monde entier", color="black", line_width=2)
    
        elif region == "en Afrique":
          df = data[data["continents"] == "Afrique"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label="en Afrique", color="red", line_width=2)

        elif region == "en Asie":
          df = data[data["continents"] == "Asie"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label='en Asie', line_width=2, color='green')

        elif region == "en Amérique du Nord":
          df = data[data["continents"] == "Amérique du Nord"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label='en Amérique du Nord', line_width=2, color='purple')
        
        elif region == "en Amérique du Sud":
          df = data[data["continents"] == "Amérique du Sud"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label='en Amérique du Sud', line_width=2, color='brown')

        elif region == "en Europe":
          df = data[data["continents"] == "Europe"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label='en Europe', line_width=2, color='blue')

        elif region == "en Océanie":
          df = data[data["continents"] == "Océanie"][["date", "New_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["New_deaths"], legend_label='en Océanie', line_width=2, color='orange')
      p.legend.location = "top_left"
      st.bokeh_chart(p, use_container_width=True)

    elif viz == "Le nombre de morts (en morts cumulées)":      
      p = figure(
              title="Nombre de morts cumulés",
              x_axis_label='Date',
              x_axis_type='datetime',
              y_axis_label='Nombre de morts cumulés'
          )
      
      for region in regions:
        if region == "dans le monde entier": 
          
          df = data[["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
    
          p.line(df["date"], df["Cumulative_deaths"], legend_label="dans le monde entier", color="black", line_width=2)
    
        elif region == "en Afrique":
          df = data[data["continents"] == "Afrique"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label="en Afrique", color="red", line_width=2)

        elif region == "en Asie":
          df = data[data["continents"] == "Asie"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label='en Asie', line_width=2, color='green')

        elif region == "en Amérique du Nord":
          df = data[data["continents"] == "Amérique du Nord"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label='en Amérique du Nord', line_width=2, color='purple')
        
        elif region == "en Amérique du Sud":
          df = data[data["continents"] == "Amérique du Sud"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label='en Amérique du Sud', line_width=2, color='brown')

        elif region == "en Europe":
          df = data[data["continents"] == "Europe"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label='en Europe', line_width=2, color='blue')

        elif region == "en Océanie":
          df = data[data["continents"] == "Océanie"][["date", "Cumulative_deaths"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["Cumulative_deaths"], legend_label='en Océanie', line_width=2, color='orange')
      p.legend.location = "top_left"
      st.bokeh_chart(p, use_container_width=True)
    
    elif viz == "La vaccination":      
      p = figure(
              title="Vaccination",
              x_axis_label='Date',
              x_axis_type='datetime',
              y_axis_label='Vaccination'
          )
      
      for region in regions:
        if region == "dans le monde entier": 
          
          df = data[["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
    
          p.line(df["date"], df["daily_vaccinations"], legend_label="dans le monde entier", color="black", line_width=2)
    
        elif region == "en Afrique":
          df = data[data["continents"] == "Afrique"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label="en Afrique", color="red", line_width=2)

        elif region == "en Asie":
          df = data[data["continents"] == "Asie"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label='en Asie', line_width=2, color='green')

        elif region == "en Amérique du Nord":
          df = data[data["continents"] == "Amérique du Nord"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label='en Amérique du Nord', line_width=2, color='purple')
        
        elif region == "en Amérique du Sud":
          df = data[data["continents"] == "Amérique du Sud"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label='en Amérique du Sud', line_width=2, color='brown')

        elif region == "en Europe":
          df = data[data["continents"] == "Europe"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label='en Europe', line_width=2, color='blue')

        elif region == "en Océanie":
          df = data[data["continents"] == "Océanie"][["date", "daily_vaccinations"]].groupby(["date"]).sum().reset_index()
          p.line(df["date"], df["daily_vaccinations"], legend_label='en Océanie', line_width=2, color='orange')
      p.legend.location = "top_left"
      st.bokeh_chart(p, use_container_width=True)

  # Classement des pays

  if choice == 'Classement des pays' :
    selected_date = st.slider("Choisis une date", min_value=date_min, max_value=date_max, value=datetime(2021,4,6))

    n = st.number_input("Choisis le nombre de pays que tu veux voir", min_value=1, max_value=10, value=3)

    top_selected = st.radio(f'Les {n} pays avec le plus...', ('de cas positifs à la COVID','de morts de la COVID',
                                                              'de doses de vaccins injectées contre la COVID'))

    if top_selected == 'de cas positifs à la COVID':
      st.subheader(f'Quels sont les {n} pays avec le plus de cas positifs à la COVID le {selected_date.date()} ?')
      case1 = st.radio('Comment veux-tu voir le classement ?', ('en cas par jour', 'en cas cummulés'))

      if case1 == 'en cas par jour':
        variable = data[data["date"] == selected_date.date().strftime('%Y-%m-%d')].nlargest(n, columns="New_cases")[["country", "New_cases"]].reset_index()
        s = "## **Résultats :**\n"
        for index, row in variable.iterrows():
            s += f'**Position {index + 1} :** {row["country"]} avec {thousand_sep(row["New_cases"])} cas  \n\n'

        st.markdown(s)

      if case1 == 'en cas cummulés':
        variable = data[data["date"] == selected_date.date().strftime('%Y-%m-%d')].nlargest(n, columns="Cumulative_cases")[["country", "Cumulative_cases"]].reset_index()
        s = "## **Résultats :**\n"
        for index, row in variable.iterrows():
            s += f'**Position {index + 1} :** {row["country"]} avec {thousand_sep(row["Cumulative_cases"])} cas  \n\n'

        st.markdown(s)

    if top_selected == 'de morts de la COVID':
      st.subheader(f'Quels sont les pays avec le plus de cas positifs à la COVID le {selected_date.date()} ?')
      case2 = st.radio('Comment veux-tu voir le classement ?', ('en cas par jour', 'en cas cummulés'))

      if case2 == 'en cas par jour':
        variable = data[data["date"] == selected_date.date().strftime('%Y-%m-%d')].nlargest(n, columns="New_deaths")[["country", "New_deaths"]].reset_index()
        s = "## **Résultats :**\n"
        for index, row in variable.iterrows():
            s += f'**Position {index + 1} :** {row["country"]} avec {thousand_sep(row["New_deaths"])} morts  \n\n'

        st.markdown(s)

      if case2 == 'en cas cummulés':
        variable = data[data["date"] == selected_date.date().strftime('%Y-%m-%d')].nlargest(n, columns="Cumulative_deaths")[["country", "Cumulative_deaths"]].reset_index()
        s = "## **Résultats :**\n"
        for index, row in variable.iterrows():
            s += f'**Position {index + 1} :** {row["country"]} avec {thousand_sep(row["Cumulative_deaths"])} morts  \n\n'

        st.markdown(s)

    if top_selected == 'de doses de vaccins injectées contre la COVID':
      st.subheader(f'Quels sont les pays avec le plus de doses de vaccins injectées contre la COVID le {selected_date.date()} ?')
      variable = data[data["date"] == selected_date.date().strftime('%Y-%m-%d')].nlargest(n, columns="daily_vaccinations")[["country", "daily_vaccinations"]].reset_index()
      s = "## **Résultats :**\n"
      for index, row in variable.iterrows():
          s += f'**Position {index + 1} :** {row["country"]} avec {thousand_sep(row["daily_vaccinations"])} doses de vaccin injectées  \n\n'

      st.markdown(s)

  # Zoom sur un pays

  if choice == 'Zoomons sur un pays' :
    st.header("Sélectionnez le pays de votre choix")

    selected_country = st.selectbox("Choisis un pays", sorted(countries))

    selected_data = st.radio("Je souhaite voir...", ('Les cas positifs', 'Les décès', 'La vaccination'))

    # Functions for 'Zoom sur un pays'
    def select_population(selected_country):
      pop = data[data.country == selected_country].Population.unique()
      return pop.astype(int)

    def sum_cases(selected_country):
      sum_cases = data[data.country == selected_country].New_cases.sum()
      return thousand_sep(sum_cases)

    def sum_deaths(selected_country):
      sum_deaths = data[data.country == selected_country].New_deaths.sum()
      return thousand_sep(sum_deaths)

    def sum_vaccinations(selected_country):
      sum_vaccinations = max(data[data.country == selected_country].daily_vaccinations)
      return thousand_sep(sum_vaccinations)

    # End functions for 'Zoom sur un pays'

    pop = select_population(selected_country)
    sum_cases = sum_cases(selected_country)
    sum_deaths = sum_deaths(selected_country)
    sum_vaccinations = sum_vaccinations(selected_country)

    c1, c2, c3, c4 = st.columns((0.8,0.9,0.8,1.5)) 
    c1.subheader("**Nombre d'habitants**\n\n")
    c1.markdown(f"### **{thousand_sep(pop[0])} habitants**")
    c2.subheader("**Nombre total de cas**\n\n")
    c2.markdown(f"### **{sum_cases} cas**")
    c3.subheader("**Nombre total de morts**\n\n")
    c3.markdown(f"### **{sum_deaths} morts**")
    c4.subheader("**Nombre total de doses de vaccins injectées**\n\n")
    c4.markdown(f"### **{sum_vaccinations} doses**")

    x = data[data.country == selected_country].date

    if selected_data == 'Les cas positifs':
      y = data[data.country == selected_country].New_cases
      title = 'cas atteints par la COVID 19'
      y_label = 'de cas'

    if selected_data == 'Les décès':
      y = data[data.country == selected_country].New_deaths
      title = 'décès causés par la COVID 19'
      y_label = 'de morts'

    if selected_data == 'La vaccination':
      y = data[data.country == selected_country].daily_vaccinations
      title = 'doses de vaccins injectées'
      y_label = 'de doses de vaccins injectées'
   
    p = figure(
        title= f'Evolution du nombre de {title}',
        x_axis_label='Date',
        x_axis_type='datetime',
        y_axis_label=f'Nombre {y_label}')
    
    p.line(x, y, legend_label=f'Tendance du pays {selected_country}', line_width=2)
    st.bokeh_chart(p, use_container_width=True)

if __name__ =='__main__':
  main()
