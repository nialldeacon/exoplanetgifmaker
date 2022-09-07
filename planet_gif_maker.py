from astropy.io.votable import parse_single_table
import numpy as np
import struct
import datetime
from PIL import Image, ImageDraw, ImageFont

#image credits
# earth NASA EPIC/DISCOVR
# super earth Kepler 62e NASA Ames/JPL-Caltech/T. Pyle
# neptune voyager 2 NASA/JPL
# jupiter NASA, ESA, A. Simon (Goddard Space Flight Center) and M.H. Wong (University of California, Berkeley)

n_slide=5
today=datetime.date.today()
indir='/Users/deacon/temp'
indir1='/Users/deacon/Dropbox/writing/twenty_worlds_promo'
outdir='/Users/deacon/temp'
font_loc='/Library/Fonts/HindVadodara-Bold.ttf'
image_filename=outdir+'/test.gif'
infile=indir+'/planets_2022.09.06_16.08.50.votable'
factor=0.25
width=200
event=['First pulsar planets','First planet orbiting a Sun-like star','First transiting planet','First microlensing planet','CoRoT planet-finding mission launched','First directly-imaged planets orbiting stars','Kepler planet-finding mission launched','First rocky planet around a Sun-like star','Kepler mission finds 715 new exoplanets','Kepler mission finds 1284 new exoplanets','Rocky, temperate TRAPPIST-1 planets','Rocky planet around the nearest star to the Sun','TESS planet-finding mission launched']
event_time=[(1,1992),(10,1995),(9,1999),(5,2004),(12,2006),(11,2008),(3,2009),(1,2011),(2,2014),(5,2016),(5,2016),(8,2016),(4,2018)]
event_pos=[0,0,0,0,0,0,1,0,0,0,1,2,0]
print((event_time[0])[1])
colours=['orange','green','blue','red','teal']
months_str=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
centre_bins=[200,600,1000,1400]

earth=Image.open(indir1+'/earth.png')
earth.thumbnail((20,20), Image.ANTIALIAS)
super_earth=Image.open(indir1+'/super_earth.png')
super_earth.thumbnail((30,30), Image.ANTIALIAS)
neptune=Image.open(indir1+'/neptune.png')
neptune.thumbnail((80,80), Image.ANTIALIAS)
jup=Image.open(indir1+'/jupiter.png')
jup.thumbnail((200,200), Image.ANTIALIAS)

#initialist animated gif frames
frames = []

table = parse_single_table(infile)
data=table.array
date1_bytes=data['disc_pubdate']
date1_strings=date1_bytes.astype('U')
date2_bytes=data['rowupdate']
date2_strings=date2_bytes.astype('U')
disc_year=data['disc_year']
disc_method_bytes=data['discoverymethod']
disc_method_strings=disc_method_bytes.astype('U')
pl_hostname_bytes=data['hostname']
pl_hostname_strings=pl_hostname_bytes.astype('U')
pl_letter_bytes=data['pl_letter']
pl_letter_strings=pl_letter_bytes.astype('U')
pl_rad=11.2*data['pl_radj']
data['pl_bmassj'].fill_value = -99
pl_mass=317.8*data['pl_bmassj']
years1 = [x[0:4] for x in date1_strings]
months1= [x[5:7] for x in date1_strings]
years2 = [x[0:4] for x in date2_strings]
months2= [x[5:7] for x in date2_strings]
years=np.zeros(len(years2))
#print(years2)
months=np.zeros(len(years2))
pl_detect_grid=np.zeros((4,5))
pl_detect_grid_old=np.zeros((4,5))
pl_disc_method=np.full(len(years2),-1,dtype=int)
pl_type=np.full(len(years2),-1,dtype=int)
pl_name=strs = ["" for x in range(len(years2))]
disc_methods=['Astrometry','Disk Kinematics','Eclipse Timing Variations','Imaging','Microlensing','Orbital Brightness Modulation','Pulsar Timing','Pulsation Timing Variations','Radial Velocity','Transit','Transit Timing Variations']
for i in range(0,len(years2)):
    index=[j for j, s in enumerate(disc_methods) if disc_method_strings[i] == s]
    #print(pl_hostname_strings[i],pl_letter_strings[i],index)
    pl_name[i]=pl_hostname_strings[i]+' '+pl_letter_strings[i]
    if(pl_rad[i]>0):
        if(pl_rad[i]<1.25):
           pl_type[i]=0
        if((pl_rad[i]>1.25)&(pl_rad[i]<2.0)):
           pl_type[i]=1
        if((pl_rad[i]>2.0)&(pl_rad[i]<6.0)):
           pl_type[i]=2
        if((pl_rad[i]>6.0)):
           pl_type[i]=3
    else:
        if(pl_mass[i]>0.0):
            if((pl_mass[i]>0.0)&(pl_mass[i]<2.0)):
                pl_type[i]=0
            if((pl_mass[i]>2.0)&(pl_mass[i]<6.0)):
                pl_type[i]=1
            if((pl_mass[i]>6.0)&(pl_mass[i]<10.0)):
                pl_type[i]=2
            if((pl_mass[i]>100.0)):
                pl_type[i]=3
    #print(pl_type[i],pl_rad[i],pl_mass[i])
    if(len(index)==1):
        pl_disc_method[i]=index[0]
    else:
        print('WARNING: discovery method not parsing',disc_method_strings[i])
    if(len(years1[i])>0):
        years[i]=float(years1[i])
        months[i]=float(months1[i])
    else:
        up_year=int(years2[i])
        if(up_year!=disc_year[i]):
            years[i]=float(disc_year[i])
            months[i]=6.0
        else:
            years[i]=float(years2[i])
            months[i]=float(months2[i]) 
      
for i0 in range(1990,2023):
    for i1 in range(1,13):
        if(((i0==today.year)&(i1>today.month))|(i0>today.year)):
            break
        discovered_mask=[((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1))&(pl_mass<13*318)]
        for i1a in range(1,n_slide+1):
            img = Image.new('RGBA', (1920,1080), color = 'white')
            fnt_lab = ImageFont.truetype(font_loc, 50)
            fnt_lab1 = ImageFont.truetype(font_loc, 40)
            fnt_lab1_sub = ImageFont.truetype(font_loc, 30)
            d = ImageDraw.Draw(img)
            tmp_str='@nialldeacon'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab1_sub))[0],1010),tmp_str, font=fnt_lab1_sub,fill='black')
            tmp_str='Data: NASA'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab1_sub))[0],900),tmp_str, font=fnt_lab1_sub,fill='black')
            tmp_str='Exoplanet'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab1_sub))[0],930),tmp_str, font=fnt_lab1_sub,fill='black')
            tmp_str='Archive'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab1_sub))[0],960),tmp_str, font=fnt_lab1_sub,fill='black')
            for i2 in range(0,len(event_time)):
                if(((i0==(event_time[i2])[1])&(i1>=(event_time[i2])[0]))|((i0==(event_time[i2])[1]+1)&((i1<(event_time[i2])[0])))):
                    tmp_str=event[i2]
                    if((12*i0+i1)<(12*(event_time[i2])[1]+(event_time[i2])[0]+11)):
                        d.text((100,100+50*event_pos[i2]),tmp_str, font=fnt_lab,fill='black')
                    else:
                        colour_step=int(255*float(n_slide*((12*i0+i1)-(12*(event_time[i2])[1]+(event_time[i2])[0]+11))+i1a)/float(n_slide))
                        d.text((100,100+50*event_pos[i2]),tmp_str, font=fnt_lab,fill=(colour_step,colour_step,colour_step))
            tmp_str=months_str[i1-1]+' '+str(int(i0))
            #tmp_str=str(int(i0))
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],100),tmp_str, font=fnt_lab,fill='black')
            tmp_str='Imaging'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],180),tmp_str, font=fnt_lab,fill=colours[0])
            tmp_str='Microlensing'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],260),tmp_str, font=fnt_lab,fill=colours[1])
            tmp_str="Radial"
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],340),tmp_str, font=fnt_lab,fill=colours[2])
            tmp_str="velocity"
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],400),tmp_str, font=fnt_lab,fill=colours[2])
            tmp_str='Transit'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],480),tmp_str, font=fnt_lab,fill=colours[3])
            tmp_str='Other'
            d.text((1900-(d.textsize(tmp_str, font=fnt_lab))[0],560),tmp_str, font=fnt_lab,fill=colours[4])
            tmp_str='Earth-sized'
            d.text((centre_bins[0]-0.5*(d.textsize(tmp_str, font=fnt_lab))[0],850), tmp_str, font=fnt_lab,fill='black')
            tmp_str='<1.25R'
            d.text((centre_bins[0]-0.5*(d.textsize(tmp_str, font=fnt_lab1))[0],920),tmp_str , font=fnt_lab1,fill='black')
            d.text((centre_bins[0]+55,950),'E' , font=fnt_lab1_sub,fill='black')
            tmp_str='Super-Earth'
            d.text((centre_bins[1]-0.5*(d.textsize(tmp_str, font=fnt_lab))[0],850), tmp_str, font=fnt_lab,fill='black')
            tmp_str='1.25R - 2R'
            d.text((centre_bins[1]-0.5*(d.textsize(tmp_str, font=fnt_lab1))[0],920),tmp_str , font=fnt_lab1,fill='black')
            d.text((centre_bins[1]+5,950),'E' , font=fnt_lab1_sub,fill='black')
            d.text((centre_bins[1]+85,950),'E' , font=fnt_lab1_sub,fill='black')
            tmp_str='Neptune-sized'
            d.text((centre_bins[2]-0.5*(d.textsize(tmp_str, font=fnt_lab))[0],850), tmp_str, font=fnt_lab,fill='black')
            tmp_str='2R - 6R'
            d.text((centre_bins[2]-0.5*(d.textsize(tmp_str, font=fnt_lab1))[0],920),tmp_str , font=fnt_lab1,fill='black')
            d.text((centre_bins[2]-20,950),'E' , font=fnt_lab1_sub,fill='black')
            d.text((centre_bins[2]+60,950),'E' , font=fnt_lab1_sub,fill='black')
            tmp_str='Jupiter-sized'
            d.text((centre_bins[3]-0.5*(d.textsize(tmp_str, font=fnt_lab))[0],850), tmp_str, font=fnt_lab,fill='black')
            tmp_str='>6R'
            d.text((centre_bins[3]-0.5*(d.textsize(tmp_str, font=fnt_lab1))[0],920),tmp_str , font=fnt_lab1,fill='black')
            d.text((centre_bins[3]+32,950),'E' , font=fnt_lab1_sub,fill='black')
            #print(i0,i1,np.sum(discovered_mask))
            for i2 in range(0,4):
                mask1=[(pl_type==i2)&(pl_disc_method==3)&(((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1)))&(pl_mass<13*318)]
                mask2=[(pl_type==i2)&(pl_disc_method==4)&(((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1)))&(pl_mass<13*318)]
                mask3=[(pl_type==i2)&(pl_disc_method==8)&(((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1)))&(pl_mass<13*318)]
                mask4=[(pl_type==i2)&(pl_disc_method==9)&(((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1)))&(pl_mass<13*318)]
                mask5=[(pl_type==i2)&((pl_disc_method==0)|(pl_disc_method==1)|(pl_disc_method==2)|(pl_disc_method==5)|(pl_disc_method==6)|(pl_disc_method==7)|(pl_disc_method==10))&(((years>1990)&(years<i0))|((years>1990)&(years<=i0)&(months>0)&(months<=i1)))&(pl_mass<13*318)]
                pl_detect_grid[i2,0]=np.sum(mask1)
                pl_detect_grid[i2,1]=np.sum(mask2)
                pl_detect_grid[i2,2]=np.sum(mask3)
                pl_detect_grid[i2,3]=np.sum(mask4)
                pl_detect_grid[i2,4]=np.sum(mask5)
            
            for i2 in range(0,4):
                base=0.0
                slide_factor=float(i1a)/float(n_slide)
                
                for i3 in range(0,5):
                    d.rectangle([(centre_bins[i2]-0.5*width,800-factor*base),(centre_bins[i2]+0.5*width,800-factor*base-factor*pl_detect_grid_old[i2,i3]-factor*slide_factor*(pl_detect_grid[i2,i3]-pl_detect_grid_old[i2,i3]))],fill=colours[i3])
                    base=base+pl_detect_grid_old[i2,i3]+slide_factor*(pl_detect_grid[i2,i3]-pl_detect_grid_old[i2,i3])
                    if(i1a==n_slide):
                         pl_detect_grid_old[i2,i3]=pl_detect_grid[i2,i3]
                    #print(i0,i1,i1a,i2,i3,base)
                tmp_str=str(int(base))
                d.text((centre_bins[i2]-0.5*(d.textsize(tmp_str, font=fnt_lab))[0],990),tmp_str , font=fnt_lab,fill='black')
                if(i2==0):
                    img.paste(earth,(int(centre_bins[i2]-10),int(770-factor*base)))
                if(i2==1):
                    img.paste(super_earth,(int(centre_bins[i2]-15),int(760-factor*base)))
                if(i2==2):
                    img.paste(neptune,(int(centre_bins[i2]-40),int(710-factor*base)))
                if(i2==3):
                    img.paste(jup,(int(centre_bins[i2]-100),int(590-factor*base)))
            #print(i0,i1,i1a)
            frames.append(img)
        #print('overwriting planet_detect_grid_old',i0,i1,i1a,pl_detect_grid_old,pl_detect_grid)
       
            
frames[0].save(image_filename, format='GIF', append_images=frames[1:], save_all=True, duration=50, loop=0)
print(pl_mass)
