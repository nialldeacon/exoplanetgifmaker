# exoplanetgifmaker
Makes a gif video of the number of exoplanets discovered over time by different methods
Example of the output here https://twitter.com/nialldeacon/status/1207270762945667072

This code requires PIL, astropy and numpy.

You can generate an input file from https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets note you need to add the pl_publ_date attribute and downloads as a VOTable

The cutout images for the planets are in the image subfolder of this repository, please add the following credits to any mention of them on social media etc.
earth NASA EPIC/DISCOVR
super earth artist's impression of Kepler 62e NASA Ames/JPL-Caltech/T. Pyle
neptune voyager 2 NASA/JPL
jupiter NASA, ESA, A. Simon (Goddard Space Flight Center) and M.H. Wong (University of California, Berkeley)

I used the HindVadodara-Bold font, you can download this font or change it to something you prefer by editing the font_loc string 

I converted from the animated GIF to MPEG using
ffmpeg -i test.gif -r 20 -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
