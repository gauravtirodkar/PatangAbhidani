# Patang Abhidani - A comprehensive guide for lepidopterists and butterfly-enthusiasts.

## Brief Summary :
<h4>The primary motivation for the project was that Skipper butterflies aren’t well documented in India. Due to rapid urbanization, butterfly counts have been receding and it is important to track the migration patterns of these butterflies to prevent them from going extinct. The system built would be able to accomplish this by gathering user submitted data and verifying its validity. This would enable new researchers to get information about skippers without having to go through the plethora of websites online. It would also work as a good platform for users to share photographs clicked by them and hence increase the total data available online.
This repository contains code for full-stack website which was built as a part of our Third Year Engineering project for a local NGO named 'Green Works Trust' and successfully submitted to them after the given period.</h4>

## Tech Stack :
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
- [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))
- [MySQL](https://en.wikipedia.org/wiki/MySQL)
- [Scikit-learn](https://en.wikipedia.org/wiki/Scikit-learn)
- [Keras-Tensorflow](https://en.wikipedia.org/wiki/Keras)
- [Pandas](https://en.wikipedia.org/wiki/Pandas_(software))
- [Numpy](https://en.wikipedia.org/wiki/NumPy)
- [HTML](https://en.wikipedia.org/wiki/HTML)
- [Bootstrap CSS](https://en.wikipedia.org/wiki/Bootstrap_(front-end_framework))
- [Javascript](https://en.wikipedia.org/wiki/JavaScript)
- [SwiperJS](https://swiperjs.com/swiper-api)
- [Selenium](https://en.wikipedia.org/wiki/Selenium_(software))
- [Folium](https://python-visualization.github.io/folium/)

## Table of Contents :
- Home Page
- Upload Page
- Data Page 
- Register/Login Page
- Image Classification Model
- Steps for Installation

### Home Page :
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa1.png)

### Upload Page
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa5.png)
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa4.png)

### Data Page 
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa6.png)
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa7.png)

### Register/Login Page
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa2.png)
![](https://github.com/Aniket-508/PatangAbhidani/blob/main/Screenshots/pa3.png)

### Image Classification Model :
[IPYNB File](https://github.com/Aniket-508/PatangAbhidani/blob/main/model/Classification_using_Transfer_learning.ipynb) 

[Saved Model](https://github.com/Aniket-508/PatangAbhidani/blob/main/model/model.h5)  


### Steps for Installation :
1. Clone this repository
```
$ git clone https://github.com/Aniket-508/PatangAbhidani.git
```
2. Setting up virtual environment for Flask
```
$ python -m venv env
$ python -m pip install flask
```     
(Make sure you have changed the Python Interpreter by going to './env' and selecting the 'python.exe' file)

3. Activating the virtual environment
```
$ env\Scripts\Activate.ps1
```
4. Installing all the requirements
```
$ pip install -r requirements.txt
```
5. Complete the process by executing the following command 
```
$ python user.py
```
### For a detailed report on the project, check [here](https://docs.google.com/document/d/1xEumbL4Hbt-EMJ50DFR8WZnEXBHlCUmx_SOB2FV-SV8/edit?usp=sharing)
