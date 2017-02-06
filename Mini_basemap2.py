from __future__ import print_function
import re
import netCDF4
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from Tkinter import *
year = ''
month = ''
day = ''
def enter_input():
    master = Tk()
    w1 = Scale(master,label ="Latitude", from_=0, to=130, orient=HORIZONTAL)
    w1.pack()
    w2 = Scale(master,label ="Longtitude", from_=0, to=155)
    w2.pack()
    var1 = StringVar(master)
    var2 = StringVar(master)
    var3 = StringVar(master)
    var1.set("Select Year") # initial value
    option = OptionMenu(master, var1, "2041", "2042", "2043", "2044","2045")
    option.pack()
    var2.set("Select Month") # initial value
    option1 = OptionMenu(master, var2, "1","2","3","4","5","6","7","8","9","10","11","12")
    option1.pack()
    var3.set("Select Day") # initial value
    option2 = OptionMenu(master, var3, "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
    option2.pack()
    button1 = Button(master, text="Send Data", command=lambda: plot_file(var1.get(),var2.get(),var3.get()))
    button1.pack()
    #def show_entry_fields():
     #   year = var1.get()
     #   month = var2.get()
      #  day = var3.get()
      #  button1 = Button(master, text="Send Data", command=lambda: plot_file(year,month,day))
      #  button1.pack()
      # # Button(master, text='Show', command= lambda: plot_file(year)).grid(row=4, column=1, sticky=W, pady=4)
    #button = Button(master, text="Get Data", command=show_entry_fields)
    #button.pack()
    #Button(master, text='Get year', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
    

enter_input()


def plot_file(year,month,day):
    #nc file name 
    my_filename = ('snc_NAM-44_CCCma-CanESM2_rcp85_r1i1p1_CCCma-CanRCM4_r2_day_20410101-20451231.nc')

    #year, month, day 
    #my_year, my_month, my_day = (2041, 12, 25)
    my_year, my_month, my_day = (int(year), int(month), int(day))

    # extracts variable name from beginning of filename:
    #my_variable = my_filename[:my_filename.find('_')]

    #Open nc file and read
    ncfile = netCDF4.Dataset('/Users/Toon/Desktop/Building/'+my_filename, 'r')

    #Search for first year that in nc file
    first_year = int(re.search(('([12][90][0-9]{2})[01][0-9]'
        '[0-3][0-9]\-[12][90][0-9]{2}[01][0-9][0-3][0-9]\.nc'), 
        my_filename).group(1))
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
    fig = plt.figure(figsize=(10,10)) #weight and height position of pic in inchs
    ax = fig.add_axes([0.1,0.1,0.8,0.8]) # add axes for pic
    #resolution = low , lon for center = -91 , lat for center = 40 , stereographic type ,smaller area for 1000 km^2 won't be plotted
    m = Basemap(width=6000000,height=4000000,resolution='l',projection='stere',lon_0=-91,lat_0=40, area_thresh=1000)
    m.drawlsmask(land_color='#00441b',ocean_color='#8be5e5',lakes=True) #draw land and sea with lakes
    m.drawcoastlines() # draw coastlines
    #m.drawstates() #draw state boundaries
    #m.drawrivers() #draw river
    m.drawcountries() #draw country boundaries
    #m.bluemarble()
    parallels = np.arange(0., 90, 10.)#set label from 0 to 90 with increase by 10
    m.drawparallels(parallels,labels=[1,1,0,0],fontsize=10) #draw label [left,right,top,bottom] 
    meridians = np.arange(180.,360.,10.)#set label from 180 to 360 with increase by 10
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #draw label [left,right,top,bottom] 
    x, y = m(nc_lons, nc_lats) #set lat to lon to mapped
    clevs = range(1,110) #set range of level
    cs = m.contourf(x,y,nc_vars,clevs,cmap=plt.cm.Greens_r) #set parameter for measurement
    cbar = m.colorbar(cs,location='bottom',pad="5%") #set position of measurement
    cbar.set_label('% snow cover')
    plt.title('Snow cover projected on "'+ str(my_day) + ' / ' + str(my_month) + ' / '  +str(my_year)+'"')
    plt.show()




mainloop( )

