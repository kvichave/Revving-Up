import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

from flask import Flask,render_template,request

class bugati:
    cars_list = {}
    models = {}
    detailofcar = {}
    domain = "https://www.cartrade.com"
    brands = {}

    def brand(self):

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
    def details(self, var):
        url = self.models.get(var)
        # print(url)
        detailofcar = {}
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        spe = soup.find_all("div", class_="spec-details")
        for div in spe:
            text = div.find('div', class_='text').text
            if div.find('div', class_='val') != None:
                val = div.find('div', class_='val').text
            else:
                val = "No information"
            detailofcar[text] = val
        # print (self.a)
        return (detailofcar)

    def reg(self, det):
        try:
            power = re.findall(r'\d+', det[" Peak Power (bhp@rpm)"])
            det[' Peak Power (bhp@rpm)'] = [int(i) for i in power]
        except:
            print('Null')

        try:
            torque = re.findall(r'\d+', det[" Peak Torque (Nm@rpm)"])
            det[' Peak Torque (Nm@rpm)'] = [int(i) for i in torque]
        except:
            print('Null')

        try:
            det[' Bootspace / Dicky Capacity (L)'] = int(det[' Bootspace / Dicky Capacity (L)'])
        # print(bootspace)
        except:
            print('Null')

        try:
            det[' Fuel Tank Capacity (L)'] = int(det[" Fuel Tank Capacity (L)"])
        # print(fueltank)
        except:
            print('Null')

        try:
            det[' Passenger Capacity'] = int(det[' Passenger Capacity'])
        # print(passengercapacity)
        except:
            print('Null')

        try:

            det[' Ground Clearance (mm)'] = int(det[' Ground Clearance (mm)'])
        # print(gclearnece)
        except:
            print('Null')

        try:
            det[' No of Seating Rows'] = int(det[' No of Seating Rows'])
        except:
            print('Null')

        try:
            ncap = re.findall(r'\d+', det[" NCAP Rating (Best - 5 Star)"])
            det[' NCAP Rating (Best - 5 Star)'] = int(ncap[0])
        except:
            print('Null')

        try:
            det[' Airbags'] = int(re.findall(r'\d+', det[" Airbags"])[0])
        # print(airbags)
        except:
            print('Null')

        try:
            det[' Braking Performance'] = float(det[' Braking Performance'])
        # print(breakingper)
        except:
            print('Null')

        try:
            det[' Warranty (Years)'] = int(det[' Warranty (Years)'])
        # print(warranty)
        except:
            print('Null')

        try:
            det[' Transmission'] = int(re.findall(r'\d+', det[" Transmission"])[0])
        # print(transmission)
        except:
            print('Null')

        try:
            engin = re.findall(r'\d+', det[" Engine"])
            det[' Engine'] = [int(i) for i in engin]
        # print(engin)
        except:
            print('Null')

        try:
            milage = re.findall(r'\d+', det[" Mileage - ARAI Reported"])
            det[' Mileage - ARAI Reported'] = [int(i) for i in milage]
        except:
            print('Null')

        try:
            det[' Driving Range (km)'] = int(det[' Driving Range (km)'])
        except:
            print('Null')
        return det
        # print(milage)




obj = bugati()



# print(obj.cars(option))





# obj = bugati()

# # obj.brand()
# # print(obj.cars('Tata'))
# obj.variant('Tata Punch')
# name = 'Tata Punch Pure MT'
# det = obj.details(name)
# det['Name'] = name
#
# reg = obj.reg(det)
#
# obj2 = bugati()
# obj2.brand()
# print(obj2.cars('Maruti Suzuki'))
# print(obj2.variant('Maruti Suzuki Ciaz'))
# name2 = 'Maruti Suzuki Ciaz Sigma 1.5'
# det2 = obj2.details(name2)
# det2['Name'] = name2
#
# reg2 = obj2.reg(det2)
# df1=pd.DataFrame([det])
# print(df1)
