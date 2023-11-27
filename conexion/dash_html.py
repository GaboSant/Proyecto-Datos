from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import psycopg2 as pg



conexion = pg.connect(
    host = "localhost",         # Nombre del host (normalmente es localhost)
    database = "datos",      # nombre de la base donde se guardan los datos
    user = "postgres",          # Nombre del usuario que maneja el servidor (normalmente es postgres)
    password = "123456789",     # Contraseña del servidor
    port = "5432")
cur = conexion.cursor()

# figutra escenario 1
cur.execute('''select nombre, total 
               from Recurso,(select codigo_recurso, sum(cantidad_producida)as total
                             from explota group by codigo_recurso) as datos 
               where codigo = codigo_recurso order by total desc''')
rows = cur.fetchall()
g1_recurso, g1_valor = zip(*rows[:10])
suma = sum(i[1] for i in rows[10:])
g1_recurso += ('OTROS',)
g1_valor += (suma,)
fig1 = figure=px.pie(names=g1_recurso, values=g1_valor, title='Producción por recursos', width=500, height=500)    

# figura escenario 2
cur.execute("select r.nombre, avg(e.valor_contraprestacion) as promedio, \
            sum(e.cantidad_producida) as total_prod from recurso as r, \
            explota as e where r.codigo = e.codigo_recurso and e.tipo_contraprestacion\
            = 'REGALIAS' group by r.nombre")
rows = cur.fetchall()
fig2 = px.bar(rows, x=0, y=1, color_discrete_sequence=["#00FFFF"],
              labels={"0": "Recursos", "1": "Valor promedio regalias (en pesos)"},
              text_auto = ".2s",
              title="Valores promedios de las regalias por recurso",
              height=500)

# figura escenario 3
cur.execute("select r.nombre, avg(e.valor_contraprestacion) as promedio, \
            sum(e.cantidad_producida) as total_prod from recurso as r, \
            explota as e where r.codigo = e.codigo_recurso and e.tipo_contraprestacion\
            = 'COMPENSACIÓN' group by r.nombre")
rows = cur.fetchall()
fig3 = px.bar(rows, x=0, y=1, color_discrete_sequence=["#00FFFF"],
              labels={"0": "Recursos", "1": "Valor promedio compensación (en pesos)"},
              text_auto = ".2s",
              title="Valores promedios de las compensaciones por recurso")

# figuta escenario 4
cur.execute('''select municipio, datos.cantidad_recursos
from ciudad, (select codigo_municipio, count(codigo_recurso) as cantidad_recursos
					from ciudad_recurso
					group by codigo_municipio)as datos
where codigo_dane = datos.codigo_municipio					
order by datos.cantidad_recursos desc''')
g3_data = cur.fetchall()
g3_municipio, g3_cantidad_recursos = zip(*g3_data)
fig4 = figure = px.bar(x = g3_municipio[:30], y = g3_cantidad_recursos[:30],
                       title = 'Municipios con mayor cantidad de recursos explotados',
                       text_auto= True)


# figura escenario 5
cur.execute("select nombre, count(codigo_municipio) from ciudad_recurso as \
            cr, recurso as r where cr.codigo_recurso = r.codigo group by nombre")
rows = cur.fetchall()

fig5 = px.pie(rows, names=0, values=1,
              labels={"0": "Recursos", "1": "número de municipios presentes"},
              title="recursos con mayor presencia en municipios",
              height=500, width=1000)
fig5.update_traces(textposition="inside", textinfo='percent+label')

cur.execute('''select municipio, departamento, codigo_dane
               from Ciudad
               ''')
menu_despegable = cur.fetchall()

app = Dash()
app.layout = html.Div(
    children = [
        html.H1(children="Extracción De Recursos En Colombia", style={"fontSize": 72}),
        html.H2(children=" Escenario 1: Recursos con mayor extracción.", style={"fontSize": 52}),
        dcc.Graph(
            id = "figura 1",
            figure = fig1
            ),
        html.P(style = {"fontSize": 32}, children="Kevin: En la gráfica podemos observar que tomando los 10 minerales más representativos la suma entre el porcentaje de explotación de los 3 mayormente explotados (carbón, plata, gravas) suma más del 50%, esto nos ayudará a concluir los próximos escenarios."),
        html.P(style={"fontSize": 32}, children="Gabriel: Además de que el carbón es el principal recurso explotado en Colombia en este 2023, le siguen la plata, con el 13,5% de la producción total del país; la Grava con el 11%; el zinc con poco más del 8,7% y las piedras calizas, con aproximadamente el 8,5%. Cabe resaltar que, a pesar de que estos son los recursos más extraídos en el proceso de explotación de recursos generan pocos beneficios para los municipios donde se extraen los mismos."),
        html.P(style={"fontSize": 32}, children="Diego: En este gráfico notamos la fuerte explotación de carbón, tan así que representa el 30% de todo el registro de explotaciones de recursos naturales de los 3 trimestres del presente año. Es importante notar que, al analizar la segunda gráfica, el carbón pese a ser el recurso más explotado, no es el recurso del que se tenga más explotaciones en los municipios del país. Los inconvenientes que presenta un gráfico de torta para los datos es la limitación en la visualización de los datos más pequeños, sin embargo, para otros da una idea muy cercana de su proporción."),
        
        
        html.H2(style={"fontSize": 52}, children="Escenario 2: Estimar el recurso natural por el que en promedio el estado recibe mayor contraprestación económica"),
        dcc.Graph(
            id = "figura 2",
            figure = fig2
            ),
        html.P(style = {"fontSize": 32},
               children='''Gabriel: De lo que se puede ver en el gráfico, era de esperar que el carbón generará grandes
                            beneficios a los municipios que explotan este recurso. Sin embargo, sorprende que el níquel
                            generará tantos beneficios sin siquiera estar entre los 10 recursos más explotados, lo que podría
                            indicar un caso de corrupción por el pago elevadísimo en la producción de este metal. También se
                            puede decir lo mismo de la sal, aunque, en este caso, no parece ser un caso tan grave como el del
                            níquel.'''),
        html.P(style = {"fontSize": 32},
               children='''Diego: La información de este gráfico es coherente con las observaciones iniciales. Al observar el
                            recurso más explotado se espere que sea uno de los que mayores ingresos generan. Sorprende que la
                            diferencia con el resto de los recursos sea tan enorme y que por lo mismo se note la desventaja de
                            este gráfico, lo poco ilustrativo que resulta con datos con tanta diferencia.'''),
        html.P(style = {"fontSize": 32},
               children='''Kevin: En base a la gráfica podemos ver que los recursos naturales que más contraprestación le
                            producen al estado son el Níquel, el Carbón y la Sal, estos resultados se pueden contrastar con los
                            resultados del primer escenario, a juzgar por el primer escenario podemos ver que el único recurso
                            que aparece representativo tanto en este escenario como en el primero es el carbón, por tanto
                            podríamos decir que la contraprestación está ligada tanto al precio como a la explotación del
                            recurso.'''),
        
        
        html.H2(style={"fontSize": 52}, children="Escenario 3: auspiciar el recurso por el que se genera una mayor contaminación ambiental"),
        dcc.Graph(
            id = "Figura 3",
            figure = fig3
            ),
        html.P(style = {"fontSize": 32},
               children='''Diego: Muy relacionado con las observaciones previas, además de ser el recurso más explotado y
                            que sin distinciones genera la mayor contraprestación económica, también lo es cuanto a la
                            contraprestación de compensación. Puede reflejar los impactos que tiene en especial la
                            explotación de este recurso para el ambiente y poblaciones. El problema de este gráfico es la
                            escasa representación que tiene los demás valores por la enorme diferencia.'''),
        html.P(style = {"fontSize": 32},
               children='''Kevin: El hecho de que en la grafica de este escenario aparezca mayormente el carbón, y que
                            además este recurso aparezca también representativo en los anteriores escenarios podría decir, que
                            el carbón siendo el recurso más explotado, sea también el recurso que mas daño medioambiental
                            produzca ya que es el recurso que más este ligado a la compensación como tipo de
                            contraprestación.'''),
        html.P(style = {"fontSize": 32},
               children='''Gabriel: De este gráfico podemos observar que la explotación del recurso que podría generar más
                            daño ambiental es el carbón, ya que genera un mayor valor de pago a título de compensación. Por
                            otro lado, el níquel genera también un alto coste en tema de compensación, pero no es de fiar este
                            dato teniendo en cuenta la situación vista en el escenario anterior.'''),
        
        html.H2(style={"fontSize": 52}, children="Escenario 4: determinar cuales son los municipios con más variedad de explotación de recursos"),
        dcc.Graph(
            id = "Figura 4",
            figure = fig4
            ),
        dcc.Dropdown(
            id='dropdown_municipio',
            options=[{'label': (municipio[0]), 'value':(municipio[2])} for municipio in menu_despegable],
            value=menu_despegable[0][2],  # Valor predeterminado
            multi=False,
            style={'width': '50%'}
        ),
        dcc.Graph(
            id='grafico_g3'
        ),
        html.P(style = {"fontSize": 32},
               children='''Kevin: En base a esta tabla, sabiendo que los municipios con la mayor cantidad de recursos
                            explotados son Manizales, Palermo, Dabeiba y Medellín, podríamos decir que estos municipios
                            reciben gran cantidad de contraprestación, pero esto seria verdadero si extraen en su mayoría
                            carbón ya que este recurso es el que más contraprestación produce.'''),
        html.P(style = {"fontSize": 32},
               children='''Gabriel: Del diagrama de barras, concluimos que las ciudades de Manizales y Palermo tienen una
                            mayor variedad en la explotación de recursos, con un total de 7 recursos diferentes explotados
                            durante el transcurso del año. Seguidos por los municipios de Dabeiba y Medellín, donde se han
                            explotado 6 recursos diferentes.'''),
        html.P(style = {"fontSize": 32},
               children='''Diego: De estas tablas observamos la correspondencia debía entre los municipios con mayor
                            explotación y sus respectivos departamentos. Revisando los municipios y los departamentos en su
                            ubicación, es distinguible una franja de explotación concentrada que divide al país diagonalmente
                            y se encuentra en la parte superior. Con respecto a estas gráficas de barras es muy intuitiva y logra
                            reflejar bien los datos siempre y cuando tenga proporcionalidad en sus valores. Una desventaja de
                            estos gráficos son sus limitaciones al momento de tener muchos datos con los que graficar.'''),
        
        
        html.H2(style={"fontSize": 52}, children="Escenario 5: ver el recurso con mayor presencia en el país"),
        dcc.Graph(
            id = "figura 5",
            figure = fig5),
        html.P(style = {"fontSize": 32},
               children='''Diego: Con las gráficas del primer escenario y las de este coinciden en su lectura, comprueben
                            que tantos municipios lo explotan porque justamente es el más presente en el territorio nacional.
                            La desventaja continua es la dificultad de notar los porcentajes más mínimos.
                            '''),
        html.P(style = {"fontSize": 32},
               children='''Gabriel: a pesar de que el carbón es el recurso más explotado en el país, no es el que tiene más
                            presencia. De hecho, el recurso con más presencia es la grava, encontrándose en el 19,3% del total
                            de municipios que explotan al menos un recurso. A su vez, le sigue la arena con una presencia del
                            17,5%, el oro con casi 14%, la plata con casi 13% y el carbón, que, a pesar de ser el recurso más
                            explotado, tiene una presencia de poco más del 9%.'''),
        html.P(style = {"fontSize": 32},
               children='''Kevin: Según la gráfica podemos ver que los recursos con mayor presencia en los territorios son
                            las gravas, las arenas, la plata, el oro y el carbón, con lo cual podríamos suponer que son los
                            recursos mayormente explotados, de los cuales según el escenario 1 todos estos recursos, a
                            excepción del oro están entre los 10 recursos con mayor explotación, lo que podría mostrar una
                            correlación entre la presencia en territorio con la cantidad de explotación.'''),
        ]
    )

@app.callback(
    Output('grafico_g3', 'figure'),
    [Input('dropdown_municipio', 'value')]
)
def actualizar_graficas(codigo_dane):
    # Consulta para obtener los 10 minerales más explotados en el municipio seleccionado
    cur.execute('''SELECT recurso.nombre, sum(explota.cantidad_producida) as cantidad
                    FROM recurso
                    JOIN explota ON recurso.codigo = explota.codigo_recurso
                    WHERE explota.codigo_municipio = %s
                    GROUP BY recurso.nombre
                    ORDER BY cantidad DESC
                    LIMIT 10''', (codigo_dane,))

    g3_data = cur.fetchall()
    g3_recurso, g3_cantidad = zip(*g3_data)

    # Gráfico para los 10 minerales más explotados
    fig_g3 = px.bar(x=g3_recurso, y=g3_cantidad, title=f'Minerales más explotados en {codigo_dane}', text_auto=True)

    return fig_g3

if __name__ == "__main__":
    app.run_server(debug=True)