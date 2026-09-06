import subprocess,sys,time,os,json
JOBS=[
('uf_gal_spiral','File:Messier 74 by HST.jpg'),
('uf_gal_barred','File:Hubble2005-01-barred-spiral-galaxy-NGC1300.jpg'),
('uf_gal_elliptical','File:Messier 87 Hubble WikiSky.jpg'),
('uf_gal_lenticular','File:Ngc5866 hst big.jpg'),
('uf_gal_irregular','File:Large Magellanic Cloud (eso1914c).jpg'),
('uf_gal_ring',"File:Hoag's object.jpg"),
('uf_gal_peculiar','File:HLA data - The Antennae Galaxies - NGC4038 4039 (Arp 244) in Corvus (39931666833).jpg'),
('uf_gal_polarring','File:NGC 4650A I HST2002.jpg'),
('uf_gal_shell','File:NGC 3923 Elliptical Shell Galaxy.jpg'),
('uf_gal_giant','File:IC 1101 in Abell 2029 (hst 06228 03 wfpc2 f702w pc).jpg'),
('uf_gal_dwarf','File:Supernova Bonanza in Nearby Galaxy NGC 1569 (2004-06-1455).jpg'),
('uf_gal_udg','File:New Hubble data explains missing dark matter (50652188762).jpg'),
('uf_gal_ucd','File:M60-UCD1 by HST.jpg'),
('uf_gal_quasar','File:Hubble probes the heart of a nearby quasar (opo0303b).jpg'),
('uf_gal_blazar','File:Blazar - Artist Concept.tif'),
('uf_gal_seyfert','File:Black Hole-Powered Spiral Galaxy NGC 7742 (1998-28-696).jpg'),
('uf_gal_radio','File:ESO Centaurus A LABOCA.jpg'),
('uf_gal_liner','File:Hazy dust in Ursa Major NGC 4036.jpg'),
('uf_gal_starburst','File:M82 HST ACS 2006-14-a-large web.jpg'),
('uf_gal_greenpea','File:Green Pea Galaxy Illustration (29801410088).png'),
('uf_gal_bcd','File:NGC 1705.jpg'),
]
for n,t in JOBS:
    if os.path.exists('temp_mj12/%s.jpg'%n) and n in json.load(open('temp_mj12/info.json')):
        print('skip',n); continue
    r=subprocess.run([sys.executable,'dl4.py',n,t,'900'],capture_output=True,text=True)
    print((r.stdout+r.stderr).strip()[-160:])
    time.sleep(12)
