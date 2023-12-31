# Importing the libraries
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from Extract_Preprocess import Extract
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import folium
from streamlit_folium import st_folium


# Class "App" contains all the utilities
class App:
    def set_page_config(self):
        icon = Image.open("data/icon.jpeg")
        st.set_page_config(page_title= "AirBNB Data Analysis",
                        page_icon= icon,
                        layout= "wide",
                        initial_sidebar_state= "expanded",
                        menu_items={'About': """# This dashboard app is created by Aastha Mukherjee!"""})
        
        st.markdown(""" 
            <style>
                    .stApp,[data-testid="stHeader"] {
                        background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77701657103-1200x901.jpg");
                        background-size: cover
                    }

                    
                    .stSpinner,[data-testid="stMarkdownContainer"],.uploadedFile{
                       color:black !important;
                    }

                    [data-testid="stSidebar"]{
                       background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77700007553.jpg");
                       background-size: cover
                    }

                    .stButton > button,.stDownloadButton > button {
                        background-color: #f54260;
                        color: black;
                    }

                    #custom-container {
                        background-color: #0B030F !important;
                        border-radius: 10px; /* Rounded corners */
                        margin: 20px; /* Margin */
                        padding: 20px;
                    }

            </style>""",unsafe_allow_html=True)
        

        
    def home_page(self):
        left,right = st.columns((1,3))
        with right:
            st.markdown('<p style="color: black; font-size:45px; font-weight:bold">Air BNB Data Analysis and Exploration</p>',unsafe_allow_html=True)
            st.markdown("""<p style="color: black; font-size:20px; font-weight:bold"> This application is mainly used to get AirBNB Data using MongoDB Atlas and then do data analysis,exploration and vizualization. It utilizes various technologies such as Streamlit, Python, PyMongo, Matplotlib, Seaborn and MongoDB database to achieve this functionality.""",unsafe_allow_html=True)
            st.markdown('<br>',unsafe_allow_html=True)
            st.markdown("""<p style="color: black; font-size:18px; font-weight:bold">Click on the <span style="color: red; font-size:18px; font-weight:bold">Dropdown Menus</span> option to start exploring.</p>""",unsafe_allow_html=True)
    

    @st.cache_data
    def read_data(_self,df):
        location_df=df[['Latitude','Longitude','Street']]
        column_name_mapping = {'Latitude': 'lat', 'Longitude': 'lon'}
        # Rename the columns using the rename method
        location_df = location_df.rename(columns=column_name_mapping)
        return location_df

    
    
    def set_sidebar(self):
        with st.sidebar:
            selected = option_menu('Choose your Way!!', ['Home Page',"Extract & Preprocess","Vizualize","View Map","About"],
                    icons=["house",'geo-fill','gear','flag','star'],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#B1A3F7"}})

        if selected == 'Home Page':
            self.home_page()

        if selected == "About":
            col1,col2 = st.columns([3,3],gap="medium")
            with col1:
                st.title(" ")
                st.write(" ")
                st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">About AirBNB:</div>""",unsafe_allow_html=True)
                st.markdown(f"""<div id="custom-container1"> Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations, typically for short stays.</div>""",unsafe_allow_html=True)
                st.markdown(f"""<div id="custom-container1"> In 2008, Brian Chesky (the current CEO), Nathan Blecharczyk, and Joe Gebbia, established the company now known as Airbnb. The idea blossomed after two of the founders started renting air mattresses in their San Francisco home to conference visitors. Hence, the original name of Airbed & Breakfast.</div>""",unsafe_allow_html=True)
                st.markdown(f"""<div id="custom-container1"> The idea behind Airbnb is simple: matching local people with a spare room or entire home to rent to others who are visiting the area. Hosts using the platform get to advertise their rentals to millions of people worldwide, with the reassurance that a big company will handle payments and offer other support. And for guests, Airbnb can provide a homey place to stay, perhaps with a kitchen to save on dining out, often at a lower price than hotels charge.</div>""",unsafe_allow_html=True)
                st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold; text-align:left;">Visit the below website to get more insights ⬇️</div>""",unsafe_allow_html=True)
                st.write("https://www.airbnb.co.in/")
                
            with col2:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                image = Image.open("data/icon.webp")
                new_image = image.resize((300,200))
                st.image(new_image)


        if selected == 'Vizualize':
            option = option_menu(None, ['Select Any Option','Tableau', "Power BI"],
                                 icons=["pencil","image",'exclamation-diamond'], default_index=0)

            if option == "Tableau":
                st.title("Tableau Visualization")
                st.markdown("""<p style="color: black; font-size:18px; font-weight:bold">Click on the <span style="color: red; font-size:18px; font-weight:bold"><a href="https://public.tableau.com/app/profile/aastha.mukherjee/viz/AirBNB_Dashboard_17035959517120/Dashboard1">Link for Tableau Dashboard</a></span></p>""",unsafe_allow_html=True)
                # Paste your Tableau embed code here
                components.html("""<html>
                <div class='tableauPlaceholder' id='viz1703758450311' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ai&#47;AirBNB_Dashboard_17035959517120&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='AirBNB_Dashboard_17035959517120&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ai&#47;AirBNB_Dashboard_17035959517120&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1703758450311');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1620px';vizElement.style.minHeight='787px';vizElement.style.maxHeight='1287px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1620px';vizElement.style.minHeight='787px';vizElement.style.maxHeight='1287px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1477px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);</script>
                </html>""",height=2000,width=2000)

            if option == "Power BI":
                st.title("Power BI Visualization")
                st.markdown("""<p style="color: black; font-size:18px; font-weight:bold">Click on the <span style="color: red; font-size:18px; font-weight:bold"><a href="https://app.powerbi.com/links/G3B4SeGWTu?ctid=0a39200a-744d-41b6-a30a-c810545ff82b&pbi_source=linkShare">Link for Power BI Dashboard</a></span></p>""",unsafe_allow_html=True)
                image = Image.open("data/My_AirBNB_Dashboard-1.png")
                new_image = image.resize((4500,3000))
                st.image(new_image)


        if selected == 'View Map':
            st.title("Geo Map using Folium")
            uploaded_file = st.file_uploader("Upload", type=["csv"])
            # Check if a file is uploaded
            if uploaded_file is not None:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(uploaded_file)
                
                location_df=self.read_data(df)
                # print(location_df)
                # st.map(location_df,zoom=1)
                c1,c2 = st.columns((7,2))
                with c1:
                    zoom_value = st.slider('Zoom Level',2,10,step=1)
                    CONNECTICUT_CENTER = (40.75245,-73.98442)
                    map = folium.Map(location=CONNECTICUT_CENTER,zoom_start=zoom_value,no_wrap=True)
                    
                    i=0
                    for index, row in location_df.iterrows():
                        if i==100:
                            break
                        # print(row)
                        loc=[float(row['lat']),float(row['lon'])]
                        folium.Marker(loc,tooltip=row['Street']).add_to(map)
                        i+=1
                    
                    st_folium(map,width=1500)
                
                with c2:
                    places_count_df = df.groupby('Country')['Street'].count().reset_index(name='Number_of_Places')
                    
                    with st.container():
                        markdown_string="<div id='custom-container'><p style='color: #04D9F6; font-family: 'Arial', sans-serif; font-size: 35px; font-weight: bold;'>Countrywise Count of AirBNB Facilities</p><div style='background-color: #04D9F6; height: 2px;'></div><br>"
                       
                        for index, rows in places_count_df.iterrows():
                            country=str(rows['Country'])
                            place_nos=str(rows['Number_of_Places'])
                            markdown_string+="<p style='color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;'>"+country+"&emsp;<span style='color: #47c3cc;font-size: 15px;'>"+place_nos+"</span></p>"
                        markdown_string+="</div>"
                        st.markdown(markdown_string,unsafe_allow_html=True)
                        # st.markdown(f'''<div style="background-color: #04D9F6; height: 2px;"></div><br>''',unsafe_allow_html=True)
                        
                        
                        # for index, rows in places_count_df.iterrows():
                        #     st.markdown(f'''<p style="color: black; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">{rows['Country']}&emsp;<span style="color: #f5425d;font-size: 15px;">{rows['Number_of_Places']}</span></p>''',unsafe_allow_html=True)
                        
                    
                        # st.markdown(f'''<div id="custom-container">
                        #             <p style="color: #04D9F6; font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold;">Legend</p>
                        #             <div style="background-color: #04D9F6; height: 2px;"></div><br>
                        #             <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">No. of Places&emsp;<span style="color: #04D9F6;font-size: 15px;">1</span></p>
                        #             <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Peer-to-Peer Payments&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">1</span></p>
                        #             <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Recharge and bill payments&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">1</span></p>
                        #             <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Financial Services&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">3</span></p>
                        #             <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Others&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">5</span></p>
                        #             <div style="background-color: #04D9F6; height: 2px;"></div>
                        #             </div>''', unsafe_allow_html=True)

                # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
                st.title("Geo Map using ScatterGeo")
                country = st.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
                room = st.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
                
    
                # CONVERTING THE USER INPUT INTO QUERY
                query = f'Country in {country} & Room_type in {room}'
                country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
                country_df.Availability_365 = country_df.Availability_365.astype(int)
                fig = px.scatter_geo(data_frame=country_df,
                                            locations='Country',
                                            color= 'Availability_365', 
                                            hover_data=['Availability_365'],
                                            locationmode='country names',
                                            size='Availability_365',
                                            title= 'Avg Availability in each Country',
                                            color_continuous_scale='agsunset'
                                    )
                st.plotly_chart(fig,use_container_width=True)
            
        
        if selected == 'Extract & Preprocess':
            csv=""
            e = Extract()
            st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 35px; font-weight: bold;">Data Extraction and Cleaning</div>""", unsafe_allow_html=True)
            left,centre,right = st.columns((1,2,2))
            with centre:
                if st.button("Get Data"):
                    df = e.create_dataframe()
                    csv = e.convert_df(df)
            with right:
                if csv =="":
                    st.write("Please click on Connect to Mongo button, then only, go for Downloading ⚠️")
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='Airbnb_data.csv',
                        mime='text/csv',
                        disabled=True
                    )
                else:
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='Airbnb_data.csv',
                        mime='text/csv',
                    )   

            st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 35px; font-weight: bold;">Exploratory Data Analysis</div><br><br>""", unsafe_allow_html=True)         
            uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

            # Check if a file is uploaded
            if uploaded_file is not None:
                # Get the current date and time
                current_datetime = datetime.now()
                # Get the timestamp (seconds since the epoch)
                timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Uploaded at : {timestamp}</div><br><br>""", unsafe_allow_html=True)
                # Read the CSV file into a DataFrame
                df = pd.read_csv(uploaded_file)
                st.dataframe(df)

                col1,col2=st.columns((2,2))
                with col1:
                    fig, ax = plt.subplots()
                    ax.set_title("Top 10 Property Types available")
                    sns.countplot(y=df.Property_type.values, data=df, ax=ax,order=df.Property_type.value_counts().index[:10])
                    st.pyplot(fig)
                with col2:
                    fig, ax = plt.subplots()
                    ax.set_title("Total Listings in each Room Type")
                    sns.countplot(data=df,x=df.Room_type)
                    st.pyplot(fig)


                col3,col4=st.columns((2,2))
                with col3:
                    fig, ax = plt.subplots()
                    ax.set_title("Top 10 Hosts with Highest number of Listings")
                    sns.countplot(data=df,y=df.Host_name,order=df.Host_name.value_counts().index[:10])
                    st.pyplot(fig)
                with col4:
                    country_df = df.groupby('Country',as_index=False)['Price'].mean()
                    x = country_df['Country']
                    y = country_df['Price']
                    fig, ax = plt.subplots()
                    ax.scatter(x,y)
                    ax.set_xlabel("Country Names")
                    ax.set_ylabel("Price")
                    ax.set_title("Avg Listing Price in each Countries")
                    st.pyplot(fig)
                    
                rev_df = df.groupby('Room_type',as_index=False)['Review_scores'].mean().sort_values(by='Review_scores')
                fig = px.bar(data_frame=rev_df,
                            title='Room Type vs Review_scores',
                            x='Room_type',
                            y='Review_scores',
                            orientation='v',
                            color='Review_scores',
                            color_continuous_scale=px.colors.sequential.Inferno)
                st.plotly_chart(fig,use_container_width=False)   
               
                pr_df = df.groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
                fig = px.bar(data_frame=pr_df,
                            title='Room Type vs Price',
                            x='Room_type',
                            y='Price',
                            orientation='v',
                            color='Price',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=False)   
                    
                    
                    
                    
                    

                
                    
                

    
        
           
                    


if __name__=="__main__":
    a = App()
    a.set_page_config()
    a.set_sidebar()