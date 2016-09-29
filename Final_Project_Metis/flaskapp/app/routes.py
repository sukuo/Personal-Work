import pandas as pd
from flask import Flask, render_template, request, jsonify

production_df = pd.read_csv('prod_df_v5.csv')

production_df['Average Delay (min)']  = production_df.ix[:,'Average Delay (min)'].apply(lambda x: round(x,1))
production_df['Variance of Delays (min)'] = production_df.ix[:, 'Variance of Delays (min)'].apply(lambda x:round(x,1))
 
app = Flask(__name__)      
 
@app.route('/', methods=['GET', 'POST'])


def home():
  results = []
  logos = []
  if request.method == 'POST':
    org = request.form['Orig']
    dest = request.form['Dest']
    sortby = request.form['sortby']
    results.append(display_dist(org, dest))
    results.append(get_airlines(org, dest, sortby).to_html(index=False))
#    results.append(display_topics(org, dest, sortby))
#    extracts.append(for_extract(org, dest, sortby))
    logos.append(html_dict(for_extract_img(org, dest, sortby), for_extract_text(org, dest, sortby)))
  return render_template('home.html', results=results, logos=logos)

def get_airlines(org, dest, sortby):  
    assert len(org), len(dest) == 3
    org, dest = org.upper(), dest.upper()
    if sortby == 'Average Delay (min)' or sortby == 'Variance of Delays (min)':
        return production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].ix[:, (1,5,6,7,8,9,10,11,12)].sort_values(str(sortby), ascending=True).reset_index().drop('index', axis=1)
    else:
        return production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].ix[:, (1,5,6,7,8,9,10,11,12)].sort_values(str(sortby), ascending=False).reset_index().drop('index', axis=1)

def origin_city(org, dest):
    org, dest = org.upper(), dest.upper()
    return eval(production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].iloc[0,2])[0]

def destination_city(org, dest):
    org, dest = org.upper(), dest.upper()
    return eval(production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].iloc[0,2])[1]

def distance_btw_cities(org, dest):
    org, dest = org.upper(), dest.upper()
    return production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].iloc[0,4]

def display_dist(org, dest):
    return 'Distance from ' + str(origin_city(org, dest)) + ' to ' + str(destination_city(org, dest)) + ' is ' + str(distance_btw_cities(org, dest)) + ' miles.' 

def display_topics(org, dest, sortby):
    org, dest = org.upper(), dest.upper()
    df = production_df.loc[production_df['Airports'] == str((str(org),str(dest)))].ix[:, (1,5,6,7,8,9,10,11,12,13)].sort_values(str(sortby), ascending=False).reset_index().drop('index', axis=1)
    airlines = df['Airline Name'].tolist()
    topics = df['Topics Extract'].tolist()
    return dict(list(zip(airlines, topics)))

#def for_extract(org, dest, sortby):
#    org, dest = org.upper(), dest.upper()
#    return production_df.ix[production_df['Airports'] == str((str(org), str(dest)))].ix[:,15].tolist()

def for_extract(org, dest, sortby):
    org, dest = org.upper(), dest.upper()
    if sortby == 'Average Delay (min)' or sortby == 'Variance of Delays (min)':
        return production_df.ix[production_df['Airports'] == str((str(org),str(dest)))].sort_values(str(sortby), ascending=True).ix[:,14].tolist()
    else:
      return production_df.ix[production_df['Airports'] == str((str(org),str(dest)))].sort_values(str(sortby), ascending=False).ix[:,14].tolist()


def for_extract_img(org, dest, sortby):
    org, dest = org.upper(), dest.upper()
    if sortby == 'Average Delay (min)' or sortby == 'Variance of Delays (min)':
        return production_df.ix[production_df['Airports'] == str((str(org), str(dest)))].sort_values(str(sortby), ascending=True).ix[:,14].tolist()
    else:
      return production_df.ix[production_df['Airports'] == str((str(org), str(dest)))].sort_values(str(sortby), ascending=False).ix[:,14].tolist()

def for_extract_text(org, dest, sortby):
    org, dest = org.upper(), dest.upper()
    if sortby == 'Average Delay (min)' or sortby == 'Variance of Delays (min)':
        return production_df.ix[production_df['Airports'] == str((str(org), str(dest)))].sort_values(str(sortby), ascending=True).ix[:,13].tolist()
    else:
      return production_df.ix[production_df['Airports'] == str((str(org), str(dest)))].sort_values(str(sortby), ascending=False).ix[:,13].tolist()


def html_dict(imgList, extractsList):
    dictList = []
    for i, img in enumerate(imgList):
        tempDict = { 'img': img, 'text':extractsList[i] }
        dictList.append(tempDict)
    return dictList



 
if __name__ == '__main__':
  app.run(debug=True)
