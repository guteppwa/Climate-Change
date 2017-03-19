from __future__ import print_function
import re
import netCDF4
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from Tkinter import *
import sys
import tkFileDialog
from PIL import Image, ImageTk
import os

Root=Tk()
year = ''
month = ''
day = ''
image = '/Users/Napat/Desktop/Work/Building/test.png'

class Building2:

    def enter_input(self):
        #window frame
        RTitle=Root.title("Netcdf File")
        RWidth=Root.winfo_screenwidth()
        RHeight=Root.winfo_screenheight()
        Root.geometry(("%dx%d")%(RWidth,RHeight))
        
        #Dataset Selection
        w = Label(Root, text="Select Dataset")
        w.pack()
        w.place(relx=0.83, rely=0.16, anchor="c")
        var_data = StringVar(Root)
        var_data.set("<Select Dataset>")
        choices = ["World","USA","Australia","Thailand"]
        option = OptionMenu(Root, var_data, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.92, rely=0.16, anchor="c")
        def open_default():
            image = Image.open('/Users/Napat/Desktop/Work/Building/'+str(var_data.get())+'.png')
            photo = ImageTk.PhotoImage(image)
            label = Label(Root,image=photo)
            label.image = photo # keep a reference!
            label.pack()
            label.place(relx=0.36, rely=0.5, anchor="c")
        button = Button(Root, text="Open Default Image",command = open_default)
        button.pack(side='left', padx=10, pady=10)
        button.place(relx=0.88, rely=0.23, anchor="c")
    
        #file path selection
        def callback():
            path = var_path.set(tkFileDialog.askopenfilename())
            print(var_path.get()) 
        var_path = StringVar()
        w = Label(Root, text="File Path:")
        e = Entry(Root,textvariable=var_path)
        b = Button(Root,text="Browse", command = callback)
        w.pack()
        w.place(relx=0.83, rely=0.1, anchor="c")
        e.pack()
        e.place(relx=0.9, rely=0.1, anchor="c")
        b.pack()
        b.place(relx=0.97, rely=0.1, anchor="c")
        
        #latitude,longitude Selection
        var_lat1 = DoubleVar(Root)
        w1 = Scale(Root,label ="Latitude-Begin", from_=90, to=-90,variable = var_lat1)
        w1.pack()
        w1.place(relx=0.83, rely=0.45, anchor="c")
        var_lat2 = DoubleVar(Root)
        w1 = Scale(Root,label ="Latitude-End", from_=90, to=-90,variable = var_lat2)
        w1.pack()
        w1.place(relx=0.93, rely=0.45, anchor="c")
        var_lon1 = DoubleVar(Root)
        w3 = Scale(Root,label ="Longtitude-Begin", from_=-180, to=180 , orient=HORIZONTAL,variable = var_lon1)
        w3.pack()
        w3.place(relx=0.83, rely=0.3, anchor="c")
        var_lon2 = DoubleVar(Root)
        w3 = Scale(Root,label ="Longtitude-End", from_=-180, to=180 , orient=HORIZONTAL,variable = var_lon2)
        w3.pack()
        w3.place(relx=0.93, rely=0.3, anchor="c")
        
        #year selection
        w = Label(Root, text="Select Year")
        w.pack()
        w.place(relx=0.82, rely=0.55, anchor="c")
        var_year = StringVar(Root)
        var_year.set("<Select Year>")
        choices = ["1900", "1901"]
        option = OptionMenu(Root, var_year, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.9, rely=0.55, anchor="c")
        
        #month selection
        w = Label(Root, text="Select Month")
        w.pack()
        w.place(relx=0.82, rely=0.6, anchor="c")
        var_mon = StringVar(Root)
        var_mon.set("<Select Month>")
        choices = ["1","2","3","4","5","6","7","8","9","10","11","12"]
        option = OptionMenu(Root, var_mon, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.9, rely=0.6, anchor="c")
    
        #day selection
        w = Label(Root, text="Select Day")
        w.pack()
        w.place(relx=0.82, rely=0.65, anchor="c")
        var_day = StringVar(Root)
        var_day.set("<Select Day>")
        choices = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        option = OptionMenu(Root, var_day, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.9, rely=0.65, anchor="c")
        
        #measurement selection
        w = Label(Root, text="Measurement")
        w.pack()
        w.place(relx=0.82, rely=0.7, anchor="c")
        var_mea = StringVar(Root)
        var_mea.set("<Measuerment>")
        choices = ["msl","t2m","skt"]
        option = OptionMenu(Root,var_mea, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.9, rely=0.7, anchor="c")

        #indices selection
        w = Label(Root, text="Indices")
        w.pack()
        w.place(relx=0.82, rely=0.75, anchor="c")
        var_ind = StringVar(Root)
        var_ind.set("<Indices>")
        choices = ["None"]
        option = OptionMenu(Root,var_ind, *choices)
        option.pack(side='left', padx=10, pady=10)
        option.pack()
        option.place(relx=0.9, rely=0.75, anchor="c")
        
        
        #send data
        button1 = Button(Root, text="Send Data for Pic", command=lambda: obj.plot_file(var_year.get(),var_mon.get(),var_day.get(),var_path.get(),var_lat1.get(),var_lat2.get(),var_lon1.get(),var_lon2.get(),var_mea.get(),image,var_data.get()))
        button1.pack()
        button1.place(relx=0.87, rely=0.8, anchor="c")
    
        
    
    
    def plot_file(self,year,month,day,path,lats_s,lats_e,lons_s,lons_e,var,path_img,dataset):
        #nc file name 
        my_filename = (path)
    
        #year, month, day 
        #my_year, my_month, my_day = (2041, 12, 25)
        my_year, my_month, my_day = (int(year), int(month), int(day))
    
        # extracts variable name from beginning of filename:
        #my_variable = my_filename[:my_filename.find('_')]
    
        #Open nc file and read
        ncfile = netCDF4.Dataset(path, 'r')
    
        #Search for first year that in nc file
        first_year = 1900
    
        #calculate how many day that past after the day that start
        month_lengths = (0,31,28,31,30,31,30,31,31,30,31,30)
        month_cumulative = []
        counter = 0
        for length in month_lengths:
            counter += length
            month_cumulative.append(counter)      
        days_elapsed = (365 * (my_year - first_year) + month_cumulative[my_month - 1] + my_day)
    
        #lat and lon from file
        nc_lons = np.array(ncfile.variables['longitude'])
        nc_lats = np.array(ncfile.variables['latitude'])
        nc_vars = np.array(ncfile.variables[var])
        nc_vars = nc_vars[days_elapsed]
    
        #base map plot
        fig = plt.figure(figsize=(11,7)) #weight and height position of pic in inchs
        ax = fig.add_axes([0.1,0.1,0.8,0.8]) # add axes for pic
        #resolution = low , lon for center = -91 , lat for center = 40 , stereographic type ,smaller area for 1000 km^2 won't be plotted
        m = Basemap(projection='cyl', llcrnrlat=lats_s, urcrnrlat=lats_e,llcrnrlon=lons_s, urcrnrlon=lons_e, resolution='i', lon_0=0,lat_0=0,area_thresh=10000)        
        m.drawcoastlines() # draw coastlines
        m.drawstates() #draw state boundaries
        m.drawcountries() #draw country boundaries
        
        #Dataset Range Latitude and Longitude
        if(dataset == 'World'):
            parallels = np.arange(-90, 91, 30)#set label from 0 to 90 with increase by 10
            m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
            meridians = np.arange(-180,180,60)#set label from 180 to 360 with increase by 10
            m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
        elif(dataset == 'Thailand'):
            parallels = np.arange(-90, 91, 5)#set label from 0 to 90 with increase by 10
            m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
            meridians = np.arange(-180,180,5)#set label from 180 to 360 with increase by 10
            m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom]
        else:
            parallels = np.arange(-90, 91, 10)#set label from 0 to 90 with increase by 10
            m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #draw label [left,right,top,bottom] 
            meridians = np.arange(-180,180,10)#set label from 180 to 360 with increase by 10
            m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
        
        #Get Latitude and Longitude to plot
        lons,lats= np.meshgrid(nc_lons-180,nc_lats) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
        x,y = m(lons,lats)
        
        #check for Measurement value
        if(var == 't2m'):
            clevs = range(221,315) #set range of level
            cs = m.contourf(x,y,nc_vars,clevs,cmap=plt.cm.jet) #set parameter for measurement
            cbar = m.colorbar(cs,location='right',pad="5%") #set position of measurement
            cbar.set_label('2 Metre Tempeature(K)')
            plt.title('2 Metre Tempeature projected on '+ str(my_day) + ' / ' + str(my_month) + ' / '  +str(my_year))
        elif(var == 'msl'):
            cs = m.contourf(x,y,nc_vars,cmap=plt.cm.jet) #set parameter for measurement
            cbar = m.colorbar(cs,location='right',pad="5%") #set position of measurement
            cbar.set_label('Mean Sea Level Pressure(Pa)')
            plt.title('Mean Sea Level Pressure projected on '+ str(my_day) + ' / ' + str(my_month) + ' / '  +str(my_year))
        elif(var == 'skt'):
            cs = m.contourf(x,y,nc_vars,cmap=plt.cm.jet) #set parameter for measurement
            cbar = m.colorbar(cs,location='right',pad="5%") #set position of measurement
            cbar.set_label('Skin Temperature(K)')
            plt.title('Skin Temperature projected on '+ str(my_day) + ' / ' + str(my_month) + ' / '  +str(my_year))
        plt.savefig(path_img)
    
    #open image function
    def open_img(self,path_image):
        def Click1():
            image = Image.open(path_image)
            photo = ImageTk.PhotoImage(image)
            label = Label(Root,image=photo)
            label.image = photo # keep a reference!
            label.pack()
            label.place(relx=0.36, rely=0.5, anchor="c")
            def Close():
                label.destroy()
            c_image1 = Button(Root, text="Close Pic", command = Close)
            c_image1.pack()
            c_image1.place(relx=0.91, rely=0.85, anchor="c")
        buttonImg1 = Button(Root, text="Open Pic", command = Click1)
        buttonImg1.pack()
        buttonImg1.place(relx=0.85, rely=0.85, anchor="c")


    
    
obj = Building2()
obj.enter_input()
obj.open_img(image)  
mainloop()
