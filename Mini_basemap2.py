##############################################################
"""

Climate Change Program

Create By Napat Rodtang     5501012620049
          Tanapoom Wongpai  5601012630108
          
Use Enthought Canoply as Editor(Python3)

---Instruction---

    Change Path of NC and JSON(line 499 - line 510) file before run program 

---Library Download Link---

1. Netcdf 
(https://pypi.python.org/packages/d8/22/8c3a488af29aa387e5fde0d677a8c3808cad46d3cd59b8160bdab6249edd/netCDF4-1.2.7.tar.gz#md5=77b357d78f9658dd973dee901f6d86f8)

2.Numpy
(https://pypi.python.org/packages/a5/16/8a678404411842fe02d780b5f0a676ff4d79cd58f0f22acddab1b392e230/numpy-1.12.1.zip#md5=c75b072a984028ac746a6a332c209a91)

3.Matplotlib
(https://pypi.python.org/packages/8f/d5/1488c5d7690fd95f91934cdce74292473e760a8dd0d8bf263fd9305728f1/matplotlib-2.0.1.tar.gz#md5=055407dc168a12c736bb65943c0d0368)

4.Json
(Come with Python from installation)

5.Tkinter
(Come with Python from installation)

6.Basemap
(https://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz/download)
"""


##############################################################
import netCDF4
import numpy as np
import matplotlib
matplotlib.use('TkAgg') 

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import json
from Tkinter import *
import matplotlib.pyplot as plt

class Plot_data(): 

    #get average data from json
    def get_data(self,json_path):
            with open(json_path) as json_data:
                d = json.load(json_data)
            data = d['mean_avg']
            return data[0] 
    
    #get max or min data from json
    def get_data1(self,json_path):
            with open(json_path) as json_data:
                d = json.load(json_data)
            data = d['data']
            return data  
            
    #plot default map
    def plot_default(self,json,var_mea,var_reso):

        #get data from json
        if(json == json_file or json == json_file1):
            data = obj.get_data(json)
        else:
            data = obj.get_data1(json)

        #get data from nc file
        ncfile = netCDF4.Dataset(nc_path)   
        nc_lons = np.array(ncfile.variables['longitude'])
        nc_lats = np.array(ncfile.variables['latitude']) 
        
        #plot screen from Frame
        f2 = Frame(root,width=500, height=100, background="blue")
        f2.pack()
        f, ax = plt.subplots(figsize=(9,6))

        #resolution condition
        if(var_reso == 'crude'):
            map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='c', lon_0=0,lat_0=0,  ax = ax) 
        if(var_reso == 'low'):
            map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l', lon_0=0,lat_0=0,  ax = ax)
        if(var_reso == 'intermediate'):
            map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='i', lon_0=0,lat_0=0,  ax = ax)       
        map.drawcoastlines() # draw coastlines
        map.drawcountries() #draw country boundaries
        parallels = np.arange(-90, 91, 30)#set label from 0 to 90 with increase by 10
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
        meridians = np.arange(-180,180,60)#set label from 180 to 360 with increase by 10
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
        lons,lats= np.meshgrid(nc_lons-180,nc_lats) #latitude and longitude from plot
        x,y = map(lons,lats)
        #cs = map.contourf(x,y,data,clevs,cmap=plt.cm.jet) #set parameter for measurement
        cs = plt.pcolormesh(x,y,data,cmap=plt.cm.jet)
        cbar = map.colorbar(cs,location='right',pad="5%") #set position of measurement
        
        #Condition for Measurement
        if(var_mea == 't2m'):
            cbar.set_label('2 Metre Tempeature(K)')
            plt.title('Mean 2 Metre Tempeature projected')
        elif(var_mea == 'tcwv'): 
            cbar.set_label('Total Column Water Vapour(kg m**-2)')
            plt.title('Total Column Water Vapour')
            
        #plot canvas
        canvas = FigureCanvasTkAgg(f, master=f2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #plot toolbar
        toolbar = NavigationToolbar2TkAgg( canvas, f2 )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        f2.place(anchor="c", relx=0.34, rely=0.5)
     
    #plot customize map   
    def plot_Customize(self,year_s,year_e,month_s,month_e,day_s,day_e,lats_s,lats_e,lons_s,lons_e,var,var_reso,var_m):
        
        #year, month, day 
        start_year, start_month, start_day = (int(year_s), int(month_s), int(day_s))
        end_year, end_month, end_day = (int(year_e), int(month_e), int(day_e))
            
        #Search for first year 
        first_year = start_year
            
        #calculate how many day that past after the day that start
        month_lengths = (0,31,28,31,30,31,30,31,31,30,31,30)
        month_cumulative = []
        counter = 0
        for length in month_lengths:
            counter += length
            month_cumulative.append(counter)      
        days_start = (365 * (start_year - first_year) + month_cumulative[start_month - 1] + start_day)
        days_end = (365 * (end_year - first_year) + month_cumulative[end_month - 1] + end_day)
            
        #get data from nc file
        ncfile = netCDF4.Dataset(nc_path)   
        nc_lons = np.array(ncfile.variables['longitude'])
        nc_lats = np.array(ncfile.variables['latitude']) 
        nc_vars = np.array(ncfile.variables[var])
        nc_vars1 = nc_vars[days_end-1]
        nc_vars2 = np.array(ncfile.variables[var]).tolist()
        nc_vars3 = np.array(ncfile.variables[var]).tolist()
        
        #find average
        if(var_m == "AVG"):
            for i in range(days_start-1,days_end-1):
                nc_vars1 = nc_vars1 + nc_vars[i]
            days_count = (days_end - days_start)+1
            avg_var = nc_vars1/days_count
            
        #find max
        elif(var_m == "Max"):
            for i in range(days_start-1,days_end-1):
                for j in range(0,len(nc_vars2[i])):
                    for k in range(0,len(nc_vars2[i][j])):
                        if(nc_vars2[0][j][k] < nc_vars2[i][j][k]):
                            nc_vars2[0][j][k] = nc_vars2[i][j][k]
                            
        #find min 
        elif(var_m == "Min"):           
            for i in range(days_start-1,days_end-1):
                for j in range(0,len(nc_vars3[i])):
                    for k in range(0,len(nc_vars3[i][j])):
                        if(nc_vars3[0][j][k] > nc_vars3[i][j][k]):
                            nc_vars3[0][j][k] = nc_vars3[i][j][k]
        
        #plot screen from Frame
        f2 = Frame(root,width=500, height=100, background="blue")
        f2.pack()
        f, ax = plt.subplots(figsize=(9,6))
        
        #resolution condtion 
        if(var_reso == 'crude'):
            map = Basemap(projection='cyl', llcrnrlat=lats_s, urcrnrlat=lats_e,llcrnrlon=lons_s, urcrnrlon=lons_e, resolution='c', lon_0=0,lat_0=0,  ax = ax) 
        if(var_reso == 'low'):
            map = Basemap(projection='cyl', llcrnrlat=lats_s, urcrnrlat=lats_e,llcrnrlon=lons_s, urcrnrlon=lons_e, resolution='l', lon_0=0,lat_0=0,  ax = ax)
        if(var_reso == 'intermediate'):
            map = Basemap(projection='cyl', llcrnrlat=lats_s, urcrnrlat=lats_e,llcrnrlon=lons_s, urcrnrlon=lons_e, resolution='i', lon_0=0,lat_0=0,  ax = ax)       
        map.drawcoastlines() # draw coastlines
        map.drawcountries() #draw country boundaries
        parallels = np.arange(-90, 91, 30)#set label from 0 to 90 with increase by 10
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
        meridians = np.arange(-180,180,60)#set label from 180 to 360 with increase by 10
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
        lons,lats= np.meshgrid(nc_lons-180,nc_lats) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
        x,y = map(lons,lats)
        #cs = map.contourf(x,y,data,clevs,cmap=plt.cm.jet) #set parameter for measurement
        
        #condition for AVG/Max/Min
        if(var_m == "AVG"):
            cs = plt.pcolormesh(x,y,avg_var,cmap=plt.cm.jet)
        elif(var_m == "Max"):
            cs = plt.pcolormesh(x,y,nc_vars2[0],cmap=plt.cm.jet)
        elif(var_m == "Min"):
            cs = plt.pcolormesh(x,y,nc_vars3[0],cmap=plt.cm.jet)
        cbar = map.colorbar(cs,location='right',pad="5%") #set position of measurement
        
        #condition for Measurement
        if(var == 't2m'):
            cbar.set_label('2 Metre Tempeature(K)')
            plt.title('Mean 2 Metre Tempeature projected')
        elif(var == 'tcwv'): 
            cbar.set_label('Total Column Water Vapour(kg m**-2)')
            plt.title('Total Column Water Vapour')
            
        #plot canvas
        canvas = FigureCanvasTkAgg(f, master=f2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #plot toolbar
        toolbar = NavigationToolbar2TkAgg( canvas, f2 )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        f2.place(anchor="c", relx=0.34, rely=0.5)
    
    #plot indices graph
    def plot__graph_indices(self,var_in):
        
        #get data from json file
        with open(json_graph) as json_data:
            d = json.load(json_data)
        data = d[var_in]
        
        #plot screen from Frame
        f2 = Frame(root,width=500, height=100, background="blue")
        f2.pack()
        f, ax = plt.subplots(figsize=(9,6))
        
        #plot data to graph
        plt.plot([0,1,2,3,4,5,6,7,8,9,10],[0,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]])
        plt.xlabel('Years')
        
        #condition for indices
        if(var_in == "FD"):
            plt.ylabel('number of frost days')
        elif(var_in == "ID"):
            plt.ylabel('number of icing days')
        elif(var_in == "SU"):
            plt.ylabel('number of summer days')
        elif(var_in == "TR"):
            plt.ylabel('number of tropical nights')
        elif(var_in == "R10mm"):
            plt.ylabel('number of day that precipitation more than 10mm')
        elif(var_in == "R20mm"):
            plt.ylabel('number of day that precipitation more than 20mm')
        
        #plot canvas
        canvas = FigureCanvasTkAgg(f, master=f2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #plot toolbar
        toolbar = NavigationToolbar2TkAgg( canvas, f2 )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        f2.place(anchor="c", relx=0.34, rely=0.5)
     
    #plot indices map   
    def plot__map_indices(self,var_in):
        
        #get data from json
        with open(json_map) as json_data:
            d = json.load(json_data)
        data = d[var_in]
        
        #get data from nc
        ncfile = netCDF4.Dataset(nc_path)   
        nc_lons = np.array(ncfile.variables['longitude'])
        nc_lats = np.array(ncfile.variables['latitude']) 
        
        #plot screen from Frame
        f2 = Frame(root,width=500, height=100, background="blue")
        f2.pack()
        f, ax = plt.subplots(figsize=(9,6))
        
        #plot Basemap
        map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='c', lon_0=0,lat_0=0,  ax = ax)       
        map.drawcoastlines() # draw coastlines
        map.drawcountries() #draw country boundaries
        parallels = np.arange(-90, 91, 30)#set label from 0 to 90 with increase by 10
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
        meridians = np.arange(-180,180,60)#set label from 180 to 360 with increase by 10
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
        lons,lats= np.meshgrid(nc_lons-180,nc_lats) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
        x,y = map(lons,lats)
        #cs = map.contourf(x,y,data,clevs,cmap=plt.cm.jet) #set parameter for measurement
        cs = plt.pcolormesh(x,y,data,cmap=plt.cm.Purples)
        cbar = map.colorbar(cs,location='right',pad="5%") #set position of measurement
        
        #condition for Indices
        if(var_in == 'FD'):
            cbar.set_label('Frost day(days)')
            plt.title('Frost Day')
        elif(var_in == 'ID'): 
            cbar.set_label('Icing day(days)')
            plt.title('Icing day')
        elif(var_in == 'SU'): 
            cbar.set_label('Summer day(days)')
            plt.title('Summer day')
        elif(var_in == 'TR'): 
            cbar.set_label('Tropical night(days)')
            plt.title('Tropical night')
        elif(var_in == 'R10mm'): 
            cbar.set_label('Precipitation more than 10mm(days)')
            plt.title('Precipitation more than 10mm') 
        elif(var_in == 'R20mm'): 
            cbar.set_label('Precipitation more than 20mm(days)')
            plt.title('Precipitation more than 20mm') 
            
        #plot canvas    
        canvas = FigureCanvasTkAgg(f, master=f2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #plot toolbar
        toolbar = NavigationToolbar2TkAgg( canvas, f2 )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        #f1.pack(fill="both", expand=False, padx=10, pady=20)
        f2.place(anchor="c", relx=0.34, rely=0.5)
    
    
class Get_input():
    
    #plot input screen
    def plot_screen(self):
        #plot window screen
        RWidth=root.winfo_screenwidth()
        RHeight=root.winfo_screenheight()
        root.geometry(("%dx%d")%(RWidth,RHeight))
        
        #latitude for plot
        var_lat1 = DoubleVar(root)
        w1 = Scale(root,label ="Latitude-Begin", from_=90, to=-90,variable = var_lat1)
        w1.pack()
        w1.place(relx=0.83, rely=0.45, anchor="c")
        var_lat2 = DoubleVar(root)
        w1 = Scale(root,label ="Latitude-End", from_=90, to=-90,variable = var_lat2)
        w1.pack()
        w1.place(relx=0.93, rely=0.45, anchor="c")
        
        #longitude for plot
        var_lon1 = DoubleVar(root)
        w3 = Scale(root,label ="Longtitude-Begin", from_=-180, to=180 , orient=HORIZONTAL,variable = var_lon1)
        w3.pack()
        w3.place(relx=0.83, rely=0.32, anchor="c")
        var_lon2 = DoubleVar(root)
        w3 = Scale(root,label ="Longtitude-End", from_=-180, to=180 , orient=HORIZONTAL,variable = var_lon2)
        w3.pack()
        w3.place(relx=0.93, rely=0.32, anchor="c")
        
        #resolution selection
        def func4(value):
            obj.plot_default(json_file,var_mea.get(),var_reso.get())
        w = Label(root, text="Resolution")
        w.pack()
        w.place(relx=0.82, rely=0.2, anchor="c")
        var_reso = StringVar(root)
        var_reso.set("crude")
        choices = ["crude","low","intermediate"]
        option = OptionMenu(root,var_reso, *choices,command=func4)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.2, anchor="c")
        
        #day selection
        w = Label(root, text="Start Date")
        w.pack()
        w.place(relx=0.8, rely=0.57, anchor="c")
        w1 = Label(root, text="End Date")
        w1.pack()
        w1.place(relx=0.8, rely=0.62, anchor="c")
        var_day1 = StringVar(root)
        var_day1.set("Day")
        var_day2 = StringVar(root)
        var_day2.set("Day")
        choices = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        option = OptionMenu(root,var_day1, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.85, rely=0.57, anchor="c")
        option = OptionMenu(root,var_day2, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.85, rely=0.62, anchor="c")
        
        #month selection
        var_month1 = StringVar(root)
        var_month1.set("Month")
        var_month2 = StringVar(root)
        var_month2.set("Month")
        choices = ["1","2","3","4","5","6","7","8","9","10","11","12"]
        option = OptionMenu(root,var_month1, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.57, anchor="c")
        option = OptionMenu(root,var_month2, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.62, anchor="c")
        
        #year selection
        var_year1 = StringVar(root)
        var_year1.set("Year")
        var_year2 = StringVar(root)
        var_year2.set("Year")
        choices = ["1958","1959","1960","1961","1962","1963","1964","1965","1966","1967"]
        option = OptionMenu(root,var_year1, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.97, rely=0.57, anchor="c")
        option = OptionMenu(root,var_year2, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.97, rely=0.62, anchor="c")
        
        
        #Label for Default Image
        w = Label(root, text="Default Image")
        w.pack()
        w.place(relx=0.87, rely=0.05, anchor="c")
        
        #Label for Customize Image
        w = Label(root, text="Customize Image")
        w.pack()
        w.place(relx=0.87, rely=0.25, anchor="c")
        
        #Measuremtn selection
        def func(value):
            if(value == "t2m"):
                obj.plot_default(json_file,var_mea.get(),'crude')
                var_m.set("AVG")
                var_lat1.set(0)
                var_lat2.set(0)
                var_lon1.set(0)
                var_lon2.set(0)
            if(value == "tcwv"):
                obj.plot_default(json_file1,var_mea.get(),'crude')  
                var_m.set("AVG")  
                var_lat1.set(0)
                var_lat2.set(0)
                var_lon1.set(0)
                var_lon2.set(0)
        w = Label(root, text="Measurement")
        w.pack()
        w.place(relx=0.82, rely=0.1, anchor="c")
        var_mea = StringVar(root)
        var_mea.set("<t2m>")
        choices = ["t2m","tcwv"]
        option = OptionMenu(root,var_mea, *choices,command= func)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.1, anchor="c")
        
        #Open Custimize Image Button
        def func2():
                obj.plot_Customize(var_year1.get(),var_year2.get(),var_month1.get(),var_month2.get(),var_day1.get(),var_day2.get(),
                var_lat1.get(),var_lat2.get(),var_lon1.get(),var_lon2.get(),var_mea.get(),var_reso.get(),var_m.get())
        w = Label(root, text="Measurement")
        #send data
        button1 = Button(root, text="Open Customize Image", command=func2)
        button1.pack()
        button1.place(relx=0.87, rely=0.7, anchor="c")
        
        #Max Min selection
        def func3(value):
            if(value == "AVG" and var_mea.get() == "t2m"):
                obj.plot_default(json_file,var_mea.get(),'crude')  
            if(value == "AVG" and var_mea.get() == "tcwv"):
                obj.plot_default(json_file1,var_mea.get(),'crude')  
            if(value == "Min" and var_mea.get() == "t2m"):
                obj.plot_default(json_min_t,var_mea.get(),'crude')
            if(value == "Min" and var_mea.get() == "tcwv"):
                obj.plot_default(json_min_p,var_mea.get(),'crude')
            if(value == "Max" and var_mea.get() == "t2m"):
                obj.plot_default(json_max_t,var_mea.get(),'crude') 
            if(value == "Max" and var_mea.get() == "tcwv"):
                obj.plot_default(json_max_p,var_mea.get(),'crude') 
        w = Label(root, text="Max/Min/AVG")
        w.pack()
        w.place(relx=0.82, rely=0.15, anchor="c")
        var_m = StringVar(root)
        var_m.set("AVG")
        choices = ["AVG","Min","Max"]
        option = OptionMenu(root,var_m, *choices,command=func3)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.15, anchor="c")
        
        """#Daily/Monthly selection
        w = Label(root, text="Daily/Monthly")
        w.pack()
        w.place(relx=0.82, rely=0.2, anchor="c")
        var_dm = StringVar(root)
        var_dm.set("Daily")
        choices = ["Daily","Monthly","Annual_Year"]
        option = OptionMenu(root,var_dm, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.2, anchor="c")"""
        
        #Indices selection
        def func5():
            obj.plot__graph_indices(var_in.get())
                
        def func6():
            obj.plot__map_indices(var_in.get())
        w = Label(root, text="Indices")        
        w.pack()
        w.place(relx=0.82, rely=0.8, anchor="c")
        var_in = StringVar(root)
        var_in.set("<Indices>")
        choices = ["FD","ID","SU","TR","R10mm","R20mm"]
        option = OptionMenu(root,var_in, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.place(relx=0.91, rely=0.8, anchor="c")
        button1 = Button(root, text="Plot Graph", command=func5)
        button1.pack()
        button1.place(relx=0.85, rely=0.87, anchor="c")
        button1 = Button(root, text="Plot Map", command=func6)
        button1.pack()
        button1.place(relx=0.91, rely=0.87, anchor="c")

#nc file path
nc_path = "/NC/_grib2netcdf-Lh8Vbr.nc"

#json file path
json_file = '/JSON/mean_temp1.json'
json_file1 = '/JSON/mean_precip1.json'
json_max_t = '/JSON/max_temp.json'
json_min_t = '/JSON/min_temp.json'
json_max_p = '/JSON/max_precip.json'
json_min_p = '/JSON/min_precip.json'
json_map = "/JSON/indice_map.json"
json_graph = '/JSON/indice_value10years.json'

obj = Plot_data() #Plot data class
obj1 = Get_input() #Get Input class

root=Tk() #Enable TKinter GUI

obj1.plot_screen()  #Call for plot input screen 
obj.plot_default(json_file,"t2m",'crude') # call for plot default

root.mainloop() # Run as loop
