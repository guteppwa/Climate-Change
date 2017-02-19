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
path_img1 = '/Users/Toon/Desktop/Building/test.png'
path_img2 = '/Users/Toon/Desktop/Building/test1.png'

def enter_input():
    #window frame
    RTitle=Root.title("Netcdf File")
    RWidth=Root.winfo_screenwidth()
    RHeight=Root.winfo_screenheight()
    Root.geometry(("%dx%d")%(RWidth,RHeight))
    

    #file path selection
    def callback():
        path = var_path.set(tkFileDialog.askopenfilename())
        print(var_path.get()) 
    var_path = StringVar()
    w = Label(Root, text="File Path:")
    e = Entry(Root,textvariable=var_path)
    b = Button(Root,text="Browse", command = callback)
    w.pack()
    w.place(relx=0.78, rely=0.1, anchor="c")
    e.pack()
    e.place(relx=0.85, rely=0.1, anchor="c")
    b.pack()
    b.place(relx=0.92, rely=0.1, anchor="c")
    
    #latitude,longitude Selection
    var_lat = DoubleVar(Root)
    w1 = Scale(Root,label ="Latitude", from_=90, to=-90,variable = var_lat)
    w1.pack()
    w1.place(relx=0.83, rely=0.2, anchor="c")
    var_lon = DoubleVar(Root)
    w2 = Scale(Root,label ="Longtitude", from_=-180, to=180 , orient=HORIZONTAL,variable = var_lon)
    w2.pack()
    w2.place(relx=0.9, rely=0.2, anchor="c")
    
    #year selection
    w = Label(Root, text="Select Year")
    w.pack()
    w.place(relx=0.82, rely=0.3, anchor="c")
    var_year = StringVar(Root)
    var_year.set("<Select Year>")
    choices = ["2041", "2042", "2043", "2044","2045"]
    option = OptionMenu(Root, var_year, *choices)
    option.pack(side='left', padx=10, pady=10)
    option.pack()
    option.place(relx=0.9, rely=0.3, anchor="c")
    
    #month selection
    w = Label(Root, text="Select Month")
    w.pack()
    w.place(relx=0.82, rely=0.4, anchor="c")
    var_mon = StringVar(Root)
    var_mon.set("<Select Month>")
    choices = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    option = OptionMenu(Root, var_mon, *choices)
    option.pack(side='left', padx=10, pady=10)
    option.pack()
    option.place(relx=0.9, rely=0.4, anchor="c")

    #day selection
    w = Label(Root, text="Select Day")
    w.pack()
    w.place(relx=0.82, rely=0.5, anchor="c")
    var_day = StringVar(Root)
    var_day.set("<Select Day>")
    choices = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    option = OptionMenu(Root, var_day, *choices)
    option.pack(side='left', padx=10, pady=10)
    option.pack()
    option.place(relx=0.9, rely=0.5, anchor="c")
    #send data
    button1 = Button(Root, text="Send Data for Pic1", command=lambda: plot_file(var_year.get(),var_mon.get(),var_day.get(),var_path.get(),var_lat.get(),var_lon.get(),path_img1))
    button1.pack()
    button1.place(relx=0.85, rely=0.6, anchor="c")
    button2 = Button(Root, text="Send Data for Pic2", command=lambda: plot_file(var_year.get(),var_mon.get(),var_day.get(),var_path.get(),var_lat.get(),var_lon.get(),path_img2))
    button2.pack()
    button2.place(relx=0.85, rely=0.65, anchor="c")
 
    
enter_input()

def plot_file(year,month,day,path,lats,lons,path_img):
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
    first_year = int(re.search(('([12][90][0-9]{2})[01][0-9][0-3][0-9]\-[12][90][0-9]{2}[01][0-9][0-3][0-9]\.nc'), my_filename).group(1))
    print("first year in .nc file = {}".format(first_year))

    #calculate how many day that past after the day that start
    month_lengths = (0,31,28,31,30,31,30,31,31,30,31,30)
    month_cumulative = []
    counter = 0
    for length in month_lengths:
        counter += length
        month_cumulative.append(counter)      
    days_elapsed = (365 * (my_year - first_year) + month_cumulative[my_month - 1] + my_day)
    print(("{} days elapsed between Jan. 1, {} and specified date of {}-{}-{}").format(days_elapsed, first_year,my_year, my_month, my_day))
    print("(leap days are not counted)")

    #lat and lon from file
    nc_lons = np.array(ncfile.variables['lon'])
    nc_lats = np.array(ncfile.variables['lat'])
    nc_vars = np.array(ncfile.variables['snc'])
    nc_vars = nc_vars[days_elapsed]

    #base map plot
    fig = plt.figure(figsize=(5,5)) #weight and height position of pic in inchs
    ax = fig.add_axes([0.1,0.1,0.8,0.8]) # add axes for pic
    #resolution = low , lon for center = -91 , lat for center = 40 , stereographic type ,smaller area for 1000 km^2 won't be plotted
    m = Basemap(width=6000000,height=4000000,resolution='l',projection='stere',lon_0=lons,lat_0=lats, area_thresh=1000)
    m.drawlsmask(land_color='#00441b',ocean_color='#8be5e5',lakes=True) #draw land and sea with lakes
    m.drawcoastlines() # draw coastlines
    #m.drawstates() #draw state boundaries
    #m.drawrivers() #draw river
    m.drawcountries() #draw country boundaries
    #m.bluemarble()
    parallels = np.arange(-90, 90, 20)#set label from 0 to 90 with increase by 10
    m.drawparallels(parallels,labels=[1,1,0,0],fontsize=10) #draw label [left,right,top,bottom] 
    meridians = np.arange(-180,180,20)#set label from 180 to 360 with increase by 10
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
    x, y = m(nc_lons, nc_lats) #set lat to lon to mapped
    clevs = range(1,110) #set range of level
    cs = m.contourf(x,y,nc_vars,clevs,cmap=plt.cm.Greens_r) #set parameter for measurement
    cbar = m.colorbar(cs,location='bottom',pad="5%") #set position of measurement
    cbar.set_label('% snow cover')
    plt.title('Snow cover projected on "'+ str(my_day) + ' / ' + str(my_month) + ' / '  +str(my_year)+'"')
    #plt.show()
    plt.savefig(path_img)

def open_img():
    def Click1():
        image = Image.open(path_img1)
        photo = ImageTk.PhotoImage(image)
        label = Label(Root,image=photo)
        label.image = photo # keep a reference!
        label.pack()
        label.place(relx=0.18, rely=0.5, anchor="c")
        def Close():
            label.destroy()
        c_image1 = Button(Root, text="Close Pic1", command = Close)
        c_image1.pack()
        c_image1.place(relx=0.87, rely=0.7, anchor="c")
    def Click2():
        image = Image.open(path_img2)
        photo = ImageTk.PhotoImage(image)
        label = Label(Root,image=photo)
        label.image = photo # keep a reference!
        label.pack()
        label.place(relx=0.55, rely=0.5, anchor="c")
        def Close():
            label.destroy()
        c_image2 = Button(Root, text="Close Pic2", command = Close)
        c_image2.pack()
        c_image2.place(relx=0.87, rely=0.75, anchor="c")
    buttonImg1 = Button(Root, text="Open Pic1", command = Click1)
    buttonImg1.pack()
    buttonImg1.place(relx=0.82, rely=0.7, anchor="c")
    buttonImg2 = Button(Root, text="Open Pic2", command = Click2)
    buttonImg2.pack()
    buttonImg2.place(relx=0.82, rely=0.75, anchor="c")

open_img()    
mainloop()
