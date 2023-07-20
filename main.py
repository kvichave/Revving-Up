import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import json
from flask import Flask,render_template,request









class bugati:
    cars_list = {}
    models = {}
    detailofcar = {}
    domain = "https://www.cartrade.com"
    brands = {}
    names=[]
    df=pd.DataFrame()

    def brand(self):
        # self.brands.clear()
        # import streamlit as st
        # Send a GET request to the URL
        url = "https://www.cartrade.com/new-cars/"
        response = requests.get(url)

        # Create a BeautifulSoup object and specify the parser
        soup = bs(response.content, "html.parser")

        # # Find the car listings on the page Peak Torque (Nm@rpm
        brand_listings = soup.find_all("div", class_="logo_brnds")
        for brand in brand_listings:
            links = brand.find_all('a')[1]
            self.brands[brand.text] = self.domain + links['href']
            # print("https://www.cartrade.com"+links['href'])
        # a = list(self.brands.keys())
        return self.brands

    def cars(self, car):
        # self.cars_list.clear()
        url = self.brands.get(car)
        response = requests.get(url)

        # Create a BeautifulSoup object and specify the parser
        soup = bs(response.content, "html.parser")
        car_list = soup.find_all('a', class_="car-list-title")
        for car in car_list:
            # print(car)
            self.cars_list[car.text] = self.domain + car['href']
        # print (self.cars_list)
        return self.cars_list

    def variant(self, model):
        # self.models.clear()
        url = self.cars_list.get(model)
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        model = soup.find_all("div", class_="car-vrsn")
        for model in model:
            ahref = model.find_all('a')[0]
            self.models[ahref.text] = self.domain + ahref['href']
        # print(self.models)

        return self.models

    # text=[]
    def details(self,var):
        url = self.models.get(var)
        # print(var,"varprinnnnnnnnnnnnnnnnnnnnnnnn")
        print("listtttttttttttt:::::: ",self.detailofcar)
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        spe = soup.find_all("div", class_="spec-details")
        for div in spe:
            text = div.find('div', class_='text').text
            if div.find('div', class_='val') != None:
                val = div.find('div', class_='val').text
            else:
                val = "No information"
            self.detailofcar[text] = val
        # print (self.a)
        self.detailofcar['Name']=var

        return (self.detailofcar)

    def reg(self, det):
        try:
            power = re.findall(r'\d+', det[" Peak Power (bhp@rpm)"])
            det[' Peak Power (bhp@rpm)'] = [int(i) for i in power]
        except:
            msg=('Null')

        try:
            torque = re.findall(r'\d+', det[" Peak Torque (Nm@rpm)"])
            det[' Peak Torque (Nm@rpm)'] = [int(i) for i in torque]
        except:
            msg=('Null')

        try:
            det[' Bootspace / Dicky Capacity (L)'] = int(det[' Bootspace / Dicky Capacity (L)'])
        # print(bootspace)
        except:
            msg=('Null')

        try:
            det[' Fuel Tank Capacity (L)'] = int(det[" Fuel Tank Capacity (L)"])
        # print(fueltank)
        except:
            msg=('Null')

        try:
            det[' Passenger Capacity'] = int(det[' Passenger Capacity'])
        # print(passengercapacity)
        except:
            msg=('Null')

        try:

            det[' Ground Clearance (mm)'] = int(det[' Ground Clearance (mm)'])
        # print(gclearnece)
        except:
            msg=('Null')

        try:
            det[' No of Seating Rows'] = int(det[' No of Seating Rows'])
        except:
            msg=('Null')

        try:
            ncap = re.findall(r'\d+', det[" NCAP Rating (Best - 5 Star)"])
            det[' NCAP Rating (Best - 5 Star)'] = int(ncap[0])
        except:
            msg=('Null')

        try:
            det[' Airbags'] = int(re.findall(r'\d+', det[" Airbags"])[0])
        # print(airbags)
        except:
            msg=('Null')

        try:
            det[' Braking Performance'] = float(det[' Braking Performance'])
        # print(breakingper)
        except:
            msg=('Null')

        try:
            det[' Warranty (Years)'] = int(det[' Warranty (Years)'])
        # print(warranty)
        except:
            msg=('Null')

        try:
            det[' Transmission'] = int(re.findall(r'\d+', det[" Transmission"])[0])
        # print(transmission)
        except:
            msg=('Null')

        try:
            engin = re.findall(r'\d+', det[" Engine"])
            det[' Engine'] = [int(i) for i in engin]
        # print(engin)
        except:
            msg=('Null')

        try:
            milage = re.findall(r"[-+]?(?:\d*\.*\d+)", det[" Mileage - ARAI Reported"])
            det[' Mileage - ARAI Reported'] = [int(i) for i in milage]
        except:
            msg=('Null')

        try:
            det[' Driving Range (km)'] = int(det[' Driving Range (km)'])
        except:
            msg=('Null')
        return det
        # print(milage)










obj=bugati()



app = Flask(__name__)
@app.route('/')
def main():
    

    
    return render_template('index.html',brands=obj.brand())

@app.route('/touch',methods=['POST'])
def gen():
    if request.method == 'POST':
        if request.form.get('brand'):
            obj.cars_list.clear()

            # print(request.form.get('brand'))
        
            carli =(obj.cars(request.form.get('brand')))
            # print(carli)
        else:
            carli=''
        
        if request.form.get('car')!='':
            # print("length : ",len(request.form.get('car')))
            
            obj.models.clear()

            # print((request.form.get('car')))
            model=obj.variant(request.form.get('car'))
            # print("modelsssssss: ",model)
            # print("printed models:::::::::::::::: ",obj.models)
        else:
            # print('inside else notttttt blank')
            model=''
        
        if request.form.get('variant')!='':
            # print("prii:::::::::::::: ",model)
            obj.detailofcar.clear()
            re=request.form.get('variant')
            print("var : :::: ",re)
            det=obj.details(re)
            re=obj.reg(det)
            # fd=df
            # pd1=pd.DataFrame([obj.df])
            pd2=pd.DataFrame([re])
            print(pd2)
            print(obj.df)

            
            if obj.df.empty:
                obj.df=pd.concat([pd2],ignore_index=True)
                df=(obj.df)

            else:
                obj.df=pd.concat([obj.df,pd2],ignore_index=True)
                df=(obj.df)
            print(obj.df)
        









        else:
            det=''
            re=''
            # red=pd.DataFrame([re])
            df=''

        # dict=[carli,model]
    # obj=bugati()
        return json.dumps([carli,model])
    

@app.route('/plot')
def pl():
    # for ent in obj.df:
    #     print(ent)
    
    i=0
    a=(obj.df).shape[0]

    power=[]
    torque=[]
    name=[]
    rpm1=[]
    rpm2=[]
    ncap=[]
    airbags=[]
    mileage=[]
    kmrange=[]
    # print()
    while i < a: 
            name.append(obj.df['Name'][i],)
            torque.append(obj.df[' Peak Torque (Nm@rpm)'][i][0])
            rpm1.append(obj.df[' Peak Torque (Nm@rpm)'][i][1])
            power.append(obj.df[' Peak Power (bhp@rpm)'][i][0])
            rpm2.append(obj.df[' Peak Power (bhp@rpm)'][i][1])
            airbags.append(obj.df[' Airbags'][i])
            ncap.append(obj.df[' NCAP Rating (Best - 5 Star)'][i])
            mileage.append(float(obj.df[' Mileage - ARAI Reported'][i]))
            kmrange.append(obj.df[' Driving Range (km)'][i]) 
                      # airbags.append(obj.df[' NCAP Rating (Best - 5 Star)'][i])
            i=i+1

     
    print("Ncappppppp :::::  ",ncap)
    # print("airbags :::::  ",airbags)
    # for i in mileage:
    #     print("mileage :::::  ",type(i)," ==== ",i)
    for i in obj.df[' Mileage - ARAI Reported']:
        test=float(i)
        # num=int(test)
        print("ncappp :::::  ",type(test)," ==== ",test)

# torque 
    print("nameeeeess :::::  ",name)
    tor = make_subplots(rows=1, cols=2)

    tor.add_trace(
        go.Bar(x=[name for name in name], y=[torque for torque in torque], name= 'Nm'),
        row=1, col=1
    )

    tor.add_trace(
        go.Bar(x=[name for name in name] ,y=[rpm for rpm in rpm1],name= 'Rpm'),
        row=1, col=2
    )

    tor.update_layout(height=600, width=800, title_text="TORQUE")
    # te.show()
    tor = json.dumps(tor, cls=plotly.utils.PlotlyJSONEncoder)
# torque end

# power
    pow = make_subplots(rows=1, cols=2)

    pow.add_trace(
        go.Bar(x=[name for name in name], y=[power for power in power],name='Bhp',marker_color='lightslategrey'),
        row=1, col=1
    )

    pow.add_trace(
        go.Bar(x=[name for name in name] ,y=[rpm for rpm in rpm2],name='Rpm',marker_color='black'),   
        row=1, col=2
    )

    pow.update_layout(height=600, width=800, title_text="POWER")
    pow = json.dumps(pow, cls=plotly.utils.PlotlyJSONEncoder)
# end power


# ncap and ground clearence

    airncap = make_subplots(rows=1, cols=2)

    airncap.add_trace(
        go.Bar(x=[name for name in name], y=[airbags for airbags in airbags]),
        row=1, col=1
    )

    airncap.add_trace(
        go.Bar(x=[name for name in name],y=[ncap for ncap in ncap]),
        row=1, col=2
    )

    airncap.update_layout(height=450, width=650, title_text="Airbags & NCAP rating")
    airncap = json.dumps(airncap, cls=plotly.utils.PlotlyJSONEncoder)

# milage and km range

    # mk = make_subplots(rows=1, cols=2)

    # mk.add_trace(
    #     go.Bar(x=[name for name in name], y=[kmpl for kmpl in mileage]),
    #     row=1, col=1
    # )

    # mk.add_trace(
    #     go.Bar(x=[name for name in name],y=[km for km in kmrange]),
    #     row=1, col=2
    # )

    # mk.update_layout(height=600, width=800, title_text=" Mileage - ARAI Reported & Driving Range (km)")
    # mk = json.dumps(mk, cls=plotly.utils.PlotlyJSONEncoder)

    specs = [[{'type':'pie'}, {"type": "pie"}]]
    mk = make_subplots(rows=1, cols=2,specs=specs, shared_yaxes = True,subplot_titles=['Pie Chart',
                                                                                     'Grouped Bar Chart'])

    mk.add_trace(
        go.Pie(labels=[name for name in name], values=[kmpl for kmpl in mileage],hole=0.7),
        row=1, col=1
    )

    mk.add_trace(
        go.Pie(labels=[name for name in name],values=[km for km in kmrange],hole=0.7),
        row=1, col=2
    )

    mk.update_layout(height=600, width=800, title_text=" Mileage - ARAI Reported & Driving Range (km)")
    mk = json.dumps(mk, cls=plotly.utils.PlotlyJSONEncoder)





































    return render_template('plot.html', tor=tor,pow=pow,airncap=airncap,mk=mk)







# @app.route('/det')



if __name__=='__main__':
    app.run(debug=True)