import os
import json
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image, ImageTk
ctk.set_appearance_mode("dark")

class wht :
    def __init__(self,root):
        self.root = root
        self.root.title("Météo")
        self.root.geometry("800x600")
        
        self.search_button = ctk.CTkButton(root, text="Rechercher",bg_color="transparent", corner_radius=30,command=self.get_city)
        self.search_button.place(x=1220,y=5)
        self.city_entry = ctk.CTkEntry(root,width=200,placeholder_text="Entrer le nom de la ville",corner_radius=30,bg_color="transparent")
        self.city_entry.place(x=1010,y=5)

        self.Sframe = ctk.CTkFrame(root,height=5,width=500,corner_radius=30)
        self.Sframe.place(x=910,y=54)
        
        
        self.visualiser_tm = ctk.CTkButton(self.Sframe, text="Temp", command=self.visualiser_t, corner_radius=30)
        self.visualiser_tm.pack(side='left', expand=True,padx=5,pady=10)
        self.visualiser_hu = ctk.CTkButton(self.Sframe, text="Humid", command=self.visualiser_h, corner_radius=30)
        self.visualiser_hu.pack(side='left', expand=True,padx=5,pady=10)
        self.visualiser_ve = ctk.CTkButton(self.Sframe, text="vent", command=self.visualiser_v, corner_radius=30)
        self.visualiser_ve.pack(side='left', expand=True,padx=5,pady=10)
        
        self.save_button = ctk.CTkButton(root, text="Sauvegarder JSON",corner_radius=30 , command=self.save_json)
        self.save_button.place(x=1223,y=124)

        self.load_button = ctk.CTkButton(root, text="Charger JSON", corner_radius=30,command=self.load_json )
        self.load_button.place(x=1223,y=184)
        
       
        self.main_frame = ctk.CTkFrame(root,fg_color="transparent")
        self.main_frame.place(x=16, y=16 )
        self.plot_frame = ctk.CTkFrame(root,fg_color="transparent",width=1050,height=400)
        self.plot_frame.place(x=120, y=124 )
        
        fig = plt.figure(figsize=(11, 5))
        fig.patch.set_facecolor('#242424')  
        ax = fig.add_subplot(111)  
        ax.set_facecolor('#242424')  
        plt.plot( label='Température', color='red')  
        plt.title(f"Température à ", color='white')  
        plt.ylabel('Température (°C)', color='white')  
        plt.grid(True, color='#444444')  
        plt.legend(facecolor='#242424', edgecolor='white', labelcolor='white') 
        plt.tick_params(axis='x', colors='white')  
        plt.tick_params(axis='y', colors='white') 
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()
        
        self.temp_label = ctk.CTkLabel(self.main_frame, text="--  --",font=("Arial", 18, "bold"))
        self.temp_label.pack(side='top', expand=True)
        self.humidity_label = ctk.CTkLabel(self.main_frame, text="-- --%",font=("Arial", 16,"bold"))
        self.humidity_label.pack(side='bottom', expand=True)
        self.wind_speed_label = ctk.CTkLabel(self.main_frame, text="-- -- km/h",font=("Arial", 16,"bold"))
        self.wind_speed_label.pack(side='bottom', expand=True)
        self.icon_label = ctk.CTkLabel(self.main_frame, text="--  --",font=("Arial", 16, "bold"))
        self.icon_label.pack(side='top', expand=True)

        self.forecast_labels_data = []
        self.forecast_labels_icon = []
        self.forecast_frame = ctk.CTkFrame(root,height=100,fg_color="transparent")
        self.forecast_frame.place(x=0, y=600, relwidth=1)
        self.forecast_frame.grid_columnconfigure(tuple(range(7)), weight=3) 
        self.forecast_frame.grid_rowconfigure((0, 1), weight=3)
        

        for col in range(7):
            icon_label = ctk.CTkLabel(self.forecast_frame, text="--  --",font=("Arial", 16, "bold")) 
            icon_label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            self.forecast_labels_icon.append(icon_label)

            text_label = ctk.CTkLabel(self.forecast_frame, text="\n-- --\n", font=("Arial", 16, "bold"))
            text_label.grid(row=1, column=col, padx=10, pady=5, sticky="nsew")
            self.forecast_labels_data.append(text_label) 

    def get_city(self):
        self.city = self.city_entry.get()
        if self.city:
            self.get_weather(self.city)
            self.visualiser_t()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un nom de ville.")
        
    def get_weather(self, city_name):
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=fr"
        try:
            geocoding_response = requests.get(geocoding_url)
            geocoding_data = geocoding_response.json()
            if not geocoding_data['results']:
                messagebox.showerror("Erreur", "Ville non trouvée.")
                return
            latitude = geocoding_data['results'][0]['latitude']
            longitude = geocoding_data['results'][0]['longitude']
            
            weather_url = "https://api.open-meteo.com/v1/forecast"
            params = {
            "latitude": latitude,
            "longitude": longitude,
            "past_days": 10,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "Africa/Casablanca"
            }
            weather_url2 = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,windspeed_10m_max&timezone=auto"
            weather_responsep = requests.get(weather_url,params=params)
            weather_responsed = requests.get(weather_url2)
            self.weather_datap = weather_responsep.json()
            self.weather_datad = weather_responsed.json()
            daily_data = self.weather_datad["daily"]
            self.update_current_weather(daily_data)
            self.update_weekly_forecast(daily_data)
            self.create_dataframe(self.weather_datap)

        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

    def create_dataframe(self, data):
   
        df = pd.DataFrame(data['hourly']['time'], columns=['time'])
        df['temperature'] = data['hourly']['temperature_2m']
        df['humidity'] = data['hourly']['relative_humidity_2m']
        df['wind_speed'] = data['hourly']['wind_speed_10m']
        df['time'] = pd.to_datetime(df['time'])
    
        today = pd.Timestamp(datetime.now().date()) 
        start_date = today - timedelta(days=10)      
        df_filtered = df[(df['time'] >= start_date) & (df['time'] < today + timedelta(days=1))]
        self.df = df_filtered  

    def update_weekly_forecast(self, daily_data):
        for i in range(7):
            max_temp = daily_data['temperature_2m_max'][i]
            min_temp = daily_data['temperature_2m_min'][i]
            date = datetime.strptime(daily_data['time'][i], "%Y-%m-%d").strftime("%A")
            label_text = (f"{date}\n"f"🌡️Max:{max_temp}°C\n"f"🌡️Min:{min_temp}°C")
            self.forecast_labels_data[i].configure(text=label_text, font=("Arial", 16, "bold"))

        for z in range(7):
            A = daily_data['weather_code'][z]
            try :
                self.icon = Image.open(rf"icon\{A}.png")
            except FileNotFoundError :
                self.icon = Image.open(r"icon\not.png")
            self.icon = self.icon.resize((60,60))  
            self.iconr = ImageTk.PhotoImage(self.icon)
            self.forecast_labels_icon[z].configure(image=self.iconr,text="")

    def update_current_weather(self, daily_data):
        B = daily_data['weather_code'][0]
        try :
            self.icon = Image.open(rf"icon\{B}.png")
        except FileNotFoundError :
                self.icon = Image.open(r"icon\not.png")
        self.icon = self.icon.resize((60,60))  
        self.iconr = ImageTk.PhotoImage(self.icon)
        self.temp_label.configure(text=f"🌡️{daily_data['temperature_2m_max'][0]}°C/{daily_data['temperature_2m_min'][0]}°C",font=("Arial", 18, "bold"))
        self.humidity_label.configure(text=f"💧  {daily_data['relative_humidity_2m_max'][0]}%",font=("Arial", 16,"bold"))
        self.wind_speed_label.configure(text=f"💨  {daily_data['windspeed_10m_max'][0]} km/h", font=("Arial", 16,"bold"))
        self.icon_label.configure(image=self.iconr,text="")

    def visualiser_t(self):
        if self.df is None:
            messagebox.showerror("Erreur", "Aucune donnée à visualiser.")
            return
        
        df = self.df
        ville = self.city
    
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(11, 5))
        fig.patch.set_facecolor('#242424')  
        ax = fig.add_subplot(111)  
        ax.set_facecolor('#242424') 
        plt.plot(df['time'], df['temperature'], label='Température', color='red')
        plt.title(f"Température à {ville} ", color='white')
        plt.ylabel('Température (°C)',color='white')
        plt.grid(True, color='#444444')  
        plt.legend(facecolor='#242424', edgecolor='white', labelcolor='white') 
        plt.tick_params(axis='x', colors='white')  
        plt.tick_params(axis='y', colors='white') 
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    def visualiser_h(self):
        if self.df is None:
            messagebox.showerror("Erreur", "Aucune donnée à visualiser.")
            return
        
        df = self.df
        ville = self.city
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
    
        fig = plt.figure(figsize=(11, 5))
        fig.patch.set_facecolor('#242424')  
        ax = fig.add_subplot(111)  
        ax.set_facecolor('#242424') 
        plt.plot(df['time'], df['humidity'], label='Humidité', color='blue')
        plt.title(f"Humidité à {ville}", color='white')
        plt.ylabel('Humidité (%)', color='white')
        plt.grid(True, color='#444444')  
        plt.legend(facecolor='#242424', edgecolor='white', labelcolor='white') 
        plt.tick_params(axis='x', colors='white')  
        plt.tick_params(axis='y', colors='white')
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    def visualiser_v(self):
        if self.df is None:
            messagebox.showerror("Erreur", "Aucune donnée à visualiser.")
            return

        df = self.df
        ville = self.city
    
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
    
        fig = plt.figure(figsize=(11, 5))
        fig.patch.set_facecolor('#242424')  
        ax = fig.add_subplot(111)  
        ax.set_facecolor('#242424') 
        plt.plot(df['time'], df['wind_speed'], label='Vitesse du vent', color='green')
        plt.title(f"Vitesse du vent à {ville}", color='white')
        plt.ylabel('Vitesse (m/s)', color='white')
        plt.grid(True, color='#444444')  
        plt.legend(facecolor='#242424', edgecolor='white', labelcolor='white') 
        plt.tick_params(axis='x', colors='white')  
        plt.tick_params(axis='y', colors='white')
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    def save_json(self):
    
        if hasattr (self, 'city') and hasattr (self, 'weather_datap') and hasattr(self, 'weather_datad'):
            df = self.df
            ville = self.city_entry.get()
            data_to_save = {
                'city' : ville,
                'weather_datap': self.weather_datap,  # Hourly data
                'weather_datad': self.weather_datad   # Daily forecast data
        }
                
            folder_path = os.path.join(os.getcwd(), 'data')
            os.makedirs(folder_path, exist_ok=True)

            filename = os.path.join(folder_path, f"{ville}_data.json")
        
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data_to_save, json_file, indent=4)
            messagebox.showinfo("Sauvegarde", "Toutes les données ont été sauvegardées.")
        else:
            messagebox.showerror("Erreur", "Aucune donnée à sauvegarder.")

    def load_json(self):
    
        file_path = filedialog.askopenfilename(title="Charger JSON", filetypes=[("JSON Files", "*.json")])
    
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        
            weather_datap = data.get('weather_datap', None)
            weather_datad = data.get('weather_datad', None)
            ville = data.get('city',None)

            if ville: 
                self.city = ville
            if weather_datap and weather_datad:
                daily_data = weather_datad.get('daily', {})
                if daily_data:
                    self.update_current_weather(daily_data)
                    self.update_weekly_forecast(daily_data)
                self.create_dataframe(weather_datap)
                self.visualiser_t()
                messagebox.showinfo("Chargement", "Toutes les données ont été chargées avec succès.")
            else:
                messagebox.showerror("Erreur", "Données invalides dans le fichier JSON.")
if __name__ == "__main__":
    root = ctk.CTk()
    app = wht(root)
    root.mainloop()