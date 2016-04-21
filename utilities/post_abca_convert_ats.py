import urllib, urllib2, csv, string


URL = "http://www.ags.gov.ab.ca/gis/map_converters/Convert_ATS_CGI.exe"
CSVFILE = "bin/dominion_coords.csv"
OUTFILE = "bin/coords_out.csv"
def main():
    
    postvars = ["SPS","ILN","ISN","ITN","IRN","IMN","FTW","FTN"]
    cf = open(CSVFILE,'rb')
    rows = csv.reader(cf,dialect='excel')
    out = []
    for row in rows:
        values = dict(zip(postvars,row))
        data = urllib.urlencode(values)
        req = urllib2.Request(URL,data)
        response = urllib2.urlopen(req)
        page = response.read()
        i = string.find(page,"Decimal Degrees")
        if i>0:
            j = string.find(page,'<td colspan="3" style="text-align:center">',i)
            if j>0:
                print [data,page[j+42:j+135]]
                out.append([data,page[j+42:j+135]])
            else:
                print "ERR2"
                out.append([data])
        else:
            print "ERR"
            out.append([data])
    of = open(OUTFILE,'wb')
    w = csv.writer(of,dialect='excel')
    for row in out:
        w.writerow(row)
        
if __name__ == '__main__':
    main()
    
    