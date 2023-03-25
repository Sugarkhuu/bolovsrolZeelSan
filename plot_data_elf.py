import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('data/processed_data.csv')

# Sometimes there are double country names such as "ОХУ / АНУ", take the first one - not use it is harmless 
df.country_all = df.country 
df.country = df.country.str.split('[/,]').str.get(0).str.strip().str.upper()

# For plotting, set country "Бусад" if number of borrowers less than or equal to 10
df.country_plot = df.country
below10 = df.groupby('country')['amount'].transform('count')<=10 
df.loc[below10,'country_plot'] = "Бусад"
df.loc[~below10,'country_plot'] = df.loc[~below10,'country'] 

# calculate the descriptive statistics
df = df.groupby('country_plot').agg({'amount': ["mean","max","min","count"]})
df.reset_index(inplace=True)
df.columns = ["country","mean","max","min","count"]
df = df.sort_values(by='count')

df.to_csv('data/plot_data.csv', index=False, encoding='utf-8-sig')

# PLOT
fig = make_subplots(specs=[[{"secondary_y": True}]])

# bar
fig.add_trace(
    go.Bar(x=df['country'], y=df['count'], name="Нийт зээлдэгчдийн тоо",marker_color='gray'),
    secondary_y=False
)

# scatter
fig.add_trace(
    go.Scatter(x=df['country'], y=df['mean'], name="Зээлийн дундаж хэмжээ (ам.д, баруун тэнхлэг)", mode='markers',
               marker_color='rgba(45, 41, 59, 1)', marker_size = 12),
    secondary_y=True
)

# general configs
fig.update_layout(title={'text':"Боловсролын зээлийн сангийн олголт, улсаар (1997-2023, нийт 55 сая ам.д, 1946 хүн)",
                         'x': 0.5},
                    legend=dict(yanchor="top", y=0.2, xanchor="left", x=0.05), 
                    font=dict(size=18))

# Set y-axes titles
fig.update_yaxes(title_text="хүний тоо", secondary_y=False)
fig.update_yaxes(title_text="ам.доллар", secondary_y=True)

fig.show()


