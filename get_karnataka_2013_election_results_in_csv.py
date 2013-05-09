#!/usr/bin/python
import os,sys

# --------------------------------------------------------------------------------------------------
# Script to fetch results of Karnataka State election 2013 results from eciresults.ap.nic.in portal, and consolidate to a csv file.
# Author: raghavan.vinay
# Date  : May 9, 2013
# License: free to use, modify for any purpose. Just expect to attribute the credits.
# 
# Tested on a linux box. 
# Tools needed on the system for this to work: grep, sed, awk, tail, curl, python
# How to run: ./get_karnataka_2013_election_results_in_csv.py > Karnataka_2013_election_results.csv
# --------------------------------------------------------------------------------------------------

# Below line is taken from the source of http://eciresults.ap.nic.in/ConstituencywiseS1034.html. Data is unstructured, so this is a silly hack.
basestr="34,Afzalpur;46,Aland;177,Anekal;8,Arabhavi;198,Arkalgud;194,Arsikere;3,Athani;52,Aurad;172,B.t.m layout;29,Babaleshwar;23,Badami;24,Bagalkot;140,Bagepalli;16,Bailhongal;176,Bangalore South;147,Bangarapet;205,Bantval;47,Basavakalyan;28,Basavana Bagevadi;170,Basavanagudi;12,Belgaum Dakshin;13,Belgaum Rural;11,Belgaum Uttar;93,Bellary;94,Bellary City;200,Belthangady;195,Belur;112,Bhadravati;51,Bhalki;79,Bhatkal;50,Bidar;49,Bidar South;30,Bijapur City;22,Bilgi;175,Bommanahalli;85,Byadgi;152,Byatarayanapura;118,Byndoor;161,C.V. Raman Nagar;98,Challakere;217,Chamaraja;223,Chamarajanagar;168,Chamrajpet;215,Chamundeshwari;109,Channagiri;185,Channapatna;169,Chickpet;141,Chikkaballapur;2,Chikkodi-Sadalga;125,Chikmagalur;128,Chiknayakanhalli;42,Chincholi;143,Chintamani;99,Chitradurga;40,Chittapur;155,Dasarahalli;106,Davanagere North;107,Davanagere South;56,Devadurga;179,Devanahalli;27,Devar Hippargi;71,Dharwad;180,Doddaballapur;66,Gadag;164,Gandhi Nagar;62,Gangawati;139,Gauribidanur;9,Gokak;166,Govindraj Nagar;135,Gubbi;44,Gulbarga Dakshin;43,Gulbarga Rural;45,Gulbarga Uttar;224,Gundlupet;39,Gurmitkal;88,Hadagalli;89,Hagaribommanahalli;76,Haliyal;82,Hangal;221,Hanur;104,Harapanahalli;105,Harihar;196,Hassan;84,Haveri;158,Hebbal;213,Heggadadevankote;86,Hirekerur;100,Hiriyur;102,Holalkere;197,Holenarasipur;48,Homnabad;110,Honnali;101,Hosadurga;178,Hosakote;74,Hubli-dharwad- West;73,Hubli-dharwad-Central;72,Hubli-dharwad-East;7,Hukkeri;25,Hungund;212,Hunsur;32,Indi;103,Jagalur;21,Jamkhandi;173,Jayanagar;35,Jevargi;151,K.r.pura;127,Kadur;4,Kagwad;75,Kalghatgi;91,Kampli;61,Kanakagiri;184,Kanakapura;121,Kapu;122,Karkal;77,Karwar;14,Khanapur;15,Kittur;148,Kolar;146,Kolar gold field;222,Kollegal;64,Koppal;134,Koratagere;216,Krishnaraja;211,Krishnarajanagara;192,Krishnarajpet;5,Kudachi;96,Kudligi;78,Kumta;119,Kundapura;70,Kundgol;131,Kunigal;60,Kushtagi;57,Lingsugur;187,Maddur;138,Madhugiri;208,Madikeri;182,Magadi;174,Mahadevapura;156,Mahalakshmi Layout;186,Malavalli;157,Malleshwaram;149,Malur;189,Mandya;204,Mangalore;202,Mangalore City North;203,Mangalore City South;55,Manvi;59,Maski;108,Mayakonda;188,Melukote;97,Molakalmuru;201,Moodabidri;26,Muddebihal;19,Mudhol;124,Mudigere;145,Mulbagal;191,Nagamangala;31,Nagthan;214,Nanjangud;218,Narasimharaja;68,Nargund;69,Navalgund;181,Nelamangala;1,Nippani;171,Padmanaba Nagar;137,Pavagada;210,Piriyapatna;159,Pulakeshinagar;206,Puttur;54,Raichur;53,Raichur Rural;165,Rajaji Nagar;154,Rajarajeshwarinagar;183,Ramanagaram;18,Ramdurg;87,Ranibennur;6,Raybag;67,Ron;117,Sagar;199,Sakleshpur;95,Sandur;160,Sarvagnanagar;17,Saundatti yellamma;41,Sedam;37,Shahapur;163,Shanti Nagar;83,Shiggaon;115,Shikaripura;113,Shimoga;111,Shimoga Rural;65,Shirahatti;162,Shivajinagar;36,Shorapur;193,Shravanabelagola;190,Shrirangapattana;142,Sidlaghatta;33,Sindgi;58,Sindhanur;136,Sira;80,Sirsi;92,Siruguppa;116,Sorab;123,Sringeri;144,Srinivaspur;207,Sullia;220,T.narasipur;126,Tarikere;20,Terdal;129,Tiptur;114,Tirthahalli;132,Tumkur City;133,Tumkur Rural;130,Turuvekere;120,Udupi;219,Varuna;167,Vijay Nagar;90,Vijayanagara;209,Virajpet;38,Yadgir;150,Yelahanka;63,Yelburga;81,Yellapur;10,Yemkanmardi;153,Yeshvanthapura"

baseurl="http://eciresults.ap.nic.in/ConstituencywiseS10"

def runcmd(file):
	cmd="  grep \"Karnataka -\" '"+file+"' | "\
		+" sed 's/<\/td>/\\n/g'  | "\
		+" awk -F\"align=\" '{print $(NF)}' | "\
		+" grep -v javascript | "\
		+" cut -d\> -f2  | "\
		+" tail -n +3 > '"+file+".hlst'"
	#print >> sys.stderr, cmd
	os.system(cmd)

for ele in basestr.split(';'):
		conscode,constname=ele.split(',')
		#print conscode,constname
		htmlflname=conscode+"-"+constname.strip()+".html"
		cmd = "curl '" + baseurl+conscode + ".htm' -o '" + htmlflname + "' 2>/dev/null"
		#print >> sys.stderr, cmd
		print >> sys.stderr, "Getting page for %s constituency" % constname.strip() 
		os.system(cmd)
		if os.path.isfile(htmlflname):
				runcmd(htmlflname)

		hlstname=htmlflname+".hlst"
		if os.path.isfile(hlstname):
				print "################################################################################################################################"
				print "Constituency code, \t\t" + conscode
				print "Constituency, \t\t\t" + constname
				print "----------------------------------------------------"
				sys.stdout.write("{0:<48}{1:<56}{2:<10}\n".format('Candiate','Party','Votes'))
				f = open(hlstname,'r')
				origlist=f.read().split('\n')
				f.close()
				lists = [origlist[i:i+3] for i in xrange(0, len(origlist), 3)]
				try:
						for sublist in lists:
								sys.stdout.write("{0:<48}{1:<56}{2:<10}\n".format(sublist[0],sublist[1],sublist[2]))
				#This is for the last elem in the origlist; it is just a '\n'
				except IndexError:
						pass


