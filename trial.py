import folium
import pandas as pd
import branca
df = pd.read_csv("E:/Project_TE/testing/PatangAbhidani/static/combined.csv")
df=df.loc[df['location'].isin(['Idukki','Calicut'])]
print(df)
# m = folium.Map(location=[20.593684, 78.96288], zoom_start=5, disable_3d=True)

# def get_frame(url, width, height, loc, datee, sn, cb):
#     html = (
#         """ 
#             <!doctype html>
#         <html>
    
#         <img id="myIFrame" class="frame" width="{}px" height="{}px" src=http://localhost:3000/butterfly/{}""".format(
#             width, height, url
#         )
#         + """ frameborder="0" ></img>
#         <p>scientific name :<b>{}</b>""".format(
#             sn
#         )
#         + """<br>date : <b>{}</b>""".format(datee)
#         + """<br>clicked by : <b>{}</b>""".format(cb)
#         + """<br>location : <b>{}</b>""".format(loc)
#         + """</p>
    
    
#         <style>
    
#         .frame {

#             border: 0;
            
#             overflow:hidden;
        
#         }
#         </style>
#         </html>"""
#     )
#     return html

# for img1, lat, lon, loc, datee, sn, cb in zip(
#     df["img"],
#     df["latitude"],
#     df["longitude"],
#     df["location"],
#     df["date"],
#     df["scientific name"],
#     df["click by"],
# ):

#     popup = get_frame(img1, 150, 150, loc, datee, sn, cb)
#     iframe = branca.element.IFrame(html=popup, width=200, height=200)
#     popup = folium.Popup(iframe, max_width=200)
#     marker = folium.Marker([lat, lon], popup=popup)

#     marker.add_to(m)

# m.save("E:/Project_TE/testing/PatangAbhidani/templates/Heatmap33.html")