# Importing the libraries
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from Extract_Preprocess import Extract
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


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
                        background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77700014672.jpg");
                        background-size: cover
                    }

                    .stSpinner,[data-testid="stMarkdownContainer"],.uploadedFile{
                       color:white !important;
                    }

                    .stButton > button,.stDownloadButton > button {
                        background-color: #f54260;
                        color: white;
                    }

                    img{
                       height:400px!important;
                       width:500px!important;
                    }
            </style>""",unsafe_allow_html=True)
        

        
    def home_page(self):
        left,right = st.columns((1,3))
        with right:
            st.markdown('<p style="color: white; font-size:45px; font-weight:bold">Air BNB Data Analysis and Exploration</p>',unsafe_allow_html=True)
            st.markdown("""<p style="color: white; font-size:20px; font-weight:bold"> This application is mainly used to get AirBNB Data using MongoDB Atlas and then do data analysis,exploration and vizualization. It utilizes various technologies such as Streamlit, Python, PyMongo, Matplotlib, Seaborn and MongoDB database to achieve this functionality.""",unsafe_allow_html=True)
            st.markdown('<br>',unsafe_allow_html=True)
            st.markdown("""<p style="color: white; font-size:18px; font-weight:bold">Click on the <span style="color: red; font-size:18px; font-weight:bold">Dropdown Menus</span> option to start exploring.</p>""",unsafe_allow_html=True)
    
    
    def set_sidebar(self):
        with st.sidebar:
            selected = option_menu('Choose your Way!!', ['Home Page',"Extract & Preprocess","Vizualize"],
                    icons=["house",'file-earmark-font','gear'],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#B1A3F7"}})

        if selected == 'Home Page':
            self.home_page()

        if selected == 'Vizualize':
            st.title("Streamlit App with Tableau Visualization")

            # Paste your Tableau embed code here
            tableau_embed_code = """
          
<div id="tableauViz"></div>
<script type="text/javascript">
  function initViz() {
    var containerDiv = document.getElementById("tableauViz");
    var url = "https://public.tableau.com/app/profile/aastha.mukherjee/viz/AirBNB_Dashboard_17035959517120/Dashboard1";
    var options = {
      hideTabs: true,
      width: "800px",
      height: "600px",
    };
    var viz = new tableau.Viz(containerDiv, url, options);
  }

  document.addEventListener("DOMContentLoaded", initViz);
</script>
"""
            

            # Use st.markdown to embed the Tableau visualization
            st.markdown(tableau_embed_code, unsafe_allow_html=True)
        
        if selected == 'Extract & Preprocess':
            csv=""

            e = Extract()
            st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 35px; font-weight: bold;">Data Extraction and Cleaning</div>""", unsafe_allow_html=True)
            left,centre,right = st.columns((1,2,2))
            with centre:
                if st.button("Connect to Mongo Cluster"):
                    df = e.create_dataframe()
                    csv = e.convert_df(df)
            with right:
                if csv =="":
                    st.write("Please click on Connect to Mongo button, then only, go for Downloading ⚠️")
                else:
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='Airbnb_data.csv',
                        mime='text/csv',
                    )   

            st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 35px; font-weight: bold;">Exploratory Data Analysis</div><br><br>""", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

            # Check if a file is uploaded
            if uploaded_file is not None:
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