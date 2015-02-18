
import pandas as pd
import os
import dissolve_shp
import makemap
import subprocess
import json
import mapnik_render

INSHP = "shps/out.shp"
TMPSHP = "tmp.shp"
LABELS = "csvs/labels_20140416.csv"
PROJECT = 'tilemill_project'

def make_polygon_style(name, field, values, colors):
    s = '''#{} {{
  polygon-opacity:1;
  polygon-gamma:.2;
'''.format(name)
    for i in range(len(values)):
        s += '  [{}="{}"] {{polygon-fill:{}; }}\n'.format(
            field, values[i], colors[i])
    s += '}'
    return s

def main():

    fields = ['ws4028cl',
              'ut4028cl',
              'bt4028cl',
              'sv4028cl',
              'ut4028ul',
              'sv4028ul']
    label_headers = ['wsc',
                     'utc',
                     'btc',
                     'svc',
                     'utu',
                     'svu']
    colors = [
        ['#0099CC', '#73AFD1', '#F8C7D9', '#DDDDDD', '#F8AB95', '#FF7351', '#FF1900', '#4e4e4e'],
        ['#0099CC', '#73AFD1', '#F8C7D9', '#DDDDDD', '#F8AB95', '#FF7351', '#FF1900', '#4e4e4e'],
        ['#FF1900', '#FF7351', '#F8AB95', '#DDDDDD', '#F8C7D9', '#73AFD1', '#0099CC' , '#4e4e4e'],
        ['#0099CC', '#73AFD1', '#F8C7D9', '#DDDDDD', '#F8AB95', '#FF7351', '#FF1900', '#4e4e4e'],
        ['#dddddd', '808080', '#4e4e4e'],
        ['#dddddd', '808080', '#4e4e4e']
    ]
    labels = pd.read_csv(LABELS)

    for i in range(len(fields)):
        if not os.path.isdir(PROJECT):
            os.makedirs(PROJECT)

        l = labels[label_headers[i]].dropna()
        outshp = os.path.join(PROJECT, TMPSHP)
        dissolve_shp.dissolve_shp(INSHP, outshp, fields[i])
        s = make_polygon_style('lyr',fields[i],l,colors[i])


        with open(os.path.join(PROJECT, 'style.mss'),'w') as f:
            f.write(s)
        p = makemap.Project(PROJECT)

        p['Stylesheet'].append('style.mss')
        p['Layer'].append(makemap.Layer('lyr', TMPSHP))
        p['srs'] = '+proj=wintri'
        mml = os.path.join(PROJECT,'project.mml')
        xml = os.path.join(PROJECT,'mapnik.xml')
        with open(mml, 'w') as f:
            json.dump(p, f)

        x = subprocess.Popen(['carto', mml, '-l'], stdout=subprocess.PIPE)
        with open(xml, 'w') as f:
            f.write(x.stdout.read())
        
        mapnik_render.render(xml, fields[i]+'.pdf')

if __name__ == "__main__":
    main()
