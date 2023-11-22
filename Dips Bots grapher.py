#!/usr/bin/env python
# coding: utf-8

# In[41]:


import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import Slider

def cargar_datos():
    global file_path
    file_path = filedialog.askopenfilename(title="Selecciona un archivo CSV", filetypes=[("CSV files", "*.csv")])

    try:
        global df, name_crypto
        df = pd.read_csv(file_path, sep='\t')
        df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: int(x.timestamp()))
        name_crypto = df['Crypto'].iloc[0]

        # Resto del código...
    except Exception as e:
        print(f"Error al cargar los datos: {e}")

def generar_grafico():
    global df, buy_points, sell_points, file_path, name_crypto
    try:
        df['Date'] = pd.to_datetime(df['Date'], unit='s')
        df = df.sort_values(by='Date')  # Ordenar por fecha

        # Puedes usar el índice numérico para el eje x
        buy_points = df[df['Side'] == 'Buy']
        sell_points = df[df['Side'] == 'Sell']

        if not df.empty:
            # Crear una nueva ventana para el gráfico
            graph_window = tk.Toplevel(root)
            graph_window.title(str(name_crypto))
            # Ajustar el tamaño de la ventana
            graph_window.geometry("1200x900")
            #ubicacion
            graph_window.geometry("+0+0")
            #topmost
            graph_window.attributes('-topmost',True)
            
            # Crear el gráfico en la nueva ventana
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_buy = ax.scatter(buy_points['Date'], buy_points['Price'], color='blue', label='Buy', marker='^')
            plot_sell = ax.scatter(sell_points['Date'], sell_points['Price'], color='red', label='Sell', marker='v')
            ax.set_title(str(name_crypto)+' TRADE BOT TIMELINE')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()
            ax.yaxis.set_major_formatter('${:.2f}'.format)
            # Ajustar el número de ticks principales en el eje y
            ax.yaxis.set_major_locator(plt.MaxNLocator(15))  # Ajusta el número según tus necesidades
            ax.xaxis.set_major_locator(plt.MaxNLocator(25))

            # Contamos el número de datos del eje X
            max_val_x = len(df['Date'].unique())

            initial_num_points_y = 10
            min_price = df['Price'].min()
            max_price = df['Price'].max()
            initial_ylim = (max_price - max_price / initial_num_points_y, max_price)

            plt.xticks(rotation=45, ha='right')
            plt.grid(True)

            # Configuración de la ventana de gráfico
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Crear la toolbar
            toolbar = NavigationToolbar2Tk(canvas, graph_window)
            toolbar.update()

            # Agregar la toolbar a la ventana
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)

            # Función para actualizar el gráfico al mover los sliders
            def update(val):
                x_scale = slider_xscale.val
                y_scale = slider_yscale.val
                max_date = df['Date'].max()
                ax.set_xlim([max_date - pd.DateOffset(days=x_scale), max_date])
                ax.set_ylim([max_price - y_scale, max_price])
                fig.canvas.draw_idle()

            # Sliders para el zoom
            ax_xscale = plt.axes([0.2, 0.1, 0.55, 0.03], facecolor='lightgoldenrodyellow')
            slider_xscale = Slider(ax_xscale, 'X Scale', 10, max_val_x, valinit=max_val_x)

            ax_yscale = plt.axes([0.2, 0.02, 0.55, 0.03], facecolor='lightgoldenrodyellow')
            slider_yscale = Slider(ax_yscale, 'Y Scale', (max_price - max_price * 0.9), max_price, valinit=max_price)

            # Asociar sliders a la función de actualización
            slider_xscale.on_changed(update)
            slider_yscale.on_changed(update)

            # Función para mostrar el precio al pasar el mouse sobre un punto
            # Función para mostrar el precio al pasar el mouse sobre un punto
# Función para mostrar el precio al pasar el mouse sobre un punto
            def hover(event):
                if event.inaxes == ax:
                    x, y = event.xdata, event.ydata
                    formatted_date = pd.to_datetime(x, unit='D', origin='unix').strftime("%d-%b")
                    text.set_text(f' Date: {formatted_date}\n Price: ${y:.2f}')
                    text.set_position((x, y))
                    fig.canvas.draw_idle()

            # Conectar evento de hover
            fig.canvas.mpl_connect('motion_notify_event', hover)

            # Texto para mostrar el precio
            text = ax.text(0, 0, '', transform=ax.transData)

            plt.subplots_adjust(bottom=0.3)

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Generar Gráfico")
root.geometry("200x180")
root.geometry("+0+0")

# Título sobre el botón
titulo_label = tk.Label(root, text="Graficador Dip", fg="Black", font=("Helvetica", 14))
titulo_label.pack(pady=10)

# Botón para cargar datos y generar el gráfico
btn_cargar_datos = tk.Button(root, text="File", bg="white", fg="black", font=("Helvetica", 14), command=cargar_datos)
btn_cargar_datos.pack(pady=10)
graficar_datos = tk.Button(root, text="Graph", bg="black", fg="white", font=("Helvetica", 14), command=generar_grafico)
graficar_datos.pack(pady=10)

# Ejecutar el bucle principal de Tkinter
root.attributes('-topmost',True)
root.mainloop()


# In[ ]:




