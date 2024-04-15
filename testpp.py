import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

#DataFrame Creation

#SQL Connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data2",
                      password="karthik")
cursor=mydb.cursor()

#aggregated transaction DF

cursor.execute("SELECT * FROM aggregated_transactionn")
mydb.commit()
table1=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

#aggregated user DF

cursor.execute("SELECT * FROM aggregated_userr")
mydb.commit()
table2=cursor.fetchall()

Aggre_user=pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Brands", "Transaction_Count", "Percentage"))

#map transaction DF

cursor.execute("SELECT * FROM map_transactionn")
mydb.commit()
table3=cursor.fetchall()

Map_transaction=pd.DataFrame(table3, columns=("States", "Years", "Quarter", "District_Names", "Type", "Transaction_Count", "Transaction_Amount"))

#map user DF

cursor.execute("SELECT * FROM map_userr")
mydb.commit()
table4=cursor.fetchall()

Map_user=pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District_Names", "Registered_Users", "Apps_Open"))

#top transaction DF

cursor.execute("SELECT * FROM top_transactionn")
mydb.commit()
table5=cursor.fetchall()

Top_transaction=pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Pincodes", "Type", "Transaction_Count", "Transaction_Amount"))

#top user DF

cursor.execute("SELECT * FROM top_userr")
mydb.commit()
table6=cursor.fetchall()

Top_user=pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Pincodes", "Registered_Users"))


def Transaction_amount_count_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)

        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:    

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="thermal",
                                range_color=(tacyg["Transaction_Amount"].min(), tacyg["Transaction_Amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600, width=550)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:    
        
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="thermal",
                                range_color=(tacyg["Transaction_Count"].min(), tacyg["Transaction_Count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:    

        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)

        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()


        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="thermal",
                                range_color=(tacyg["Transaction_Amount"].min(), tacyg["Transaction_Amount"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
    
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="thermal",
                                range_color=(tacyg["Transaction_Count"].min(), tacyg["Transaction_Count"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return tacy

    
def aggre_Tran_Type(df,state):
    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg= tacy.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=tacyg, names="Transaction_Type",values="Transaction_Amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame=tacyg, names="Transaction_Type",values="Transaction_Count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)

        st.plotly_chart(fig_pie_2)

#aggre_user_analaysis_1

def aggre_user_plot_1(df,year):
    aguy= df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg, x="Brands", y="Transaction_Count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence=px.colors.sequential.Emrld_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy


#aggr_user_analysis_2

def aggre_user_plot_2(df,quarter):
    aguyq= df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_Count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg, x="Brands", y="Transaction_Count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#aggr_user_analysis_3

def aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True, inplace= True)

    fig_line_1= px.line(auyqs, x="Brands",y="Transaction_Count",hover_data="Percentage",
                        title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)


# map transac dis type

def map_transac_district(df,state):
    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg= tacy.groupby("District_Names")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x="Transaction_Amount", y="District_Names", orientation="h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Oranges_r)

        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2=px.bar(tacyg, x="Transaction_Count", y="District_Names", orientation="h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Blackbody_r)

        st.plotly_chart(fig_bar_2)



#map user plot 1
def map_user_plot_1(df,year):

    muy= df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)
    muyg=muy.groupby("States")[["Registered_Users","Apps_Open"]].sum()
    muyg.reset_index(inplace=True)
    fig_line_1= px.line(muyg, x="States",y=["Registered_Users","Apps_Open"],
                        title=f"{year} REGISTERED USER AND APP OPEN",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)

    return muy

#map user plot 2
def map_user_plot_2(df,quarter):

    muyq= df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)
    muyqg=muyq.groupby("States")[["Registered_Users","Apps_Open"]].sum()
    muyqg.reset_index(inplace=True)
    fig_line_1= px.line(muyqg, x="States",y=["Registered_Users","Apps_Open"],
                        title=f"{quarter} Q REGISTERED USER AND APP OPEN",width=1000,height=800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map user plot 3
def map_user_plot_3(df,states):
    muyqs= df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar1=px.bar(muyqs, x="Registered_Users", y="District_Names",orientation="h",
                                title=f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_map_user_bar1)

    with col2:
        fig_map_user_bar2=px.bar(muyqs, x="Apps_Open", y="District_Names",orientation="h",
                                title=f"{states.upper()} APP OPEN", height=800, color_discrete_sequence=px.colors.sequential.Burg)
        st.plotly_chart(fig_map_user_bar2)


# top transaction plot 1
def top_transac_plot_1(df,state):
    
    tty= df[df["States"]==state]
    tty.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_tran_bar1=px.bar(tty, x="Quarter", y="Transaction_Amount",hover_data="Pincodes",
                                title="TRANSACTION AMOUNT ", height=650,width=600, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_top_tran_bar1)

    with col2:
        fig_top_tran_bar2=px.bar(tty, x="Quarter", y="Transaction_Count",hover_data="Pincodes",
                                title="TRANSACTION COUNT", height=650,width=600, color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_tran_bar2)


#top user plot 1
def top_user_plot_1(df,year):
    tuy= df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_Users"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot1=px.bar(tuyg, x="States", y="States",color="Quarter", width=1000, height=800,
                        hover_name="States" ,color_discrete_sequence=px.colors.sequential.Greys_r,
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot1)

    return tuy

#top user plot 2
def top_user_plot_2(df,state):
    tuys= df[df["States"]==state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(tuys, x="Quarter", y="Registered_Users", title="REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height=800, color="Registered_Users", hover_data="Pincodes",color_continuous_scale=px.colors.sequential.Oranges)
    st.plotly_chart(fig_top_plot_2)



#top 10 transaction ammount

def table_view1(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data2",
                        password="karthik")
    cursor=mydb.cursor()

    query1=f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()
    df1= pd.DataFrame(table1, columns=("states","transaction_amount"))

    fig_amount=px.bar(df1, x="states", y="transaction_amount", title="TRANSACTION AMOUNT", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=800, width=1000)
    st.plotly_chart(fig_amount)


#least 10 count in transaction count
def table_view2(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data2",
                        password="karthik")
    cursor=mydb.cursor()

    query2=f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()
    df2= pd.DataFrame(table2, columns=("states","transaction_count"))

    fig_count1=px.bar(df2, x="states", y="transaction_count", title="TRANSACTION COUNT", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Oranges_r, height=800, width=1000)
    st.plotly_chart(fig_count1)

#average transaction amount
def table_average_amount(table_name):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data2",
                        password="karthik")
        cursor=mydb.cursor()

        query3=f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY transaction_amount;'''

        cursor.execute(query3)
        table3= cursor.fetchall()
        mydb.commit()

        df3= pd.DataFrame(table3, columns=("states","transaction_amount"))

        fig_amount3=px.bar(df3, x="states", y="transaction_amount", title="TRANSACTION AMOUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Rainbow, height=800, width=1000)
        st.plotly_chart(fig_amount3)    

#average tansaction count
def table_average_count(table_name):
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data2",
                        password="karthik")
        cursor=mydb.cursor()

        query4=f'''SELECT states, AVG(transaction_count) AS transaction_count
                        FROM {table_name}
                        GROUP BY states
                        ORDER BY transaction_count;'''

        cursor.execute(query4)
        table4= cursor.fetchall()
        mydb.commit()

        df4= pd.DataFrame(table4, columns=("states","transaction_count"))

        fig_amount4=px.bar(df4, x="states", y="transaction_count", title="TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Darkmint_r, height=800, width=1000)
        st.plotly_chart(fig_amount4)



#steamlit Part

st.set_page_config(layout="wide")
st.title(":violet[PhonePe] Data Visualization And Exploration:sparkles:")

with st.sidebar:
    
    st.caption(":violet[Application created by karthik]")
    select=option_menu("Main Menu",["Home", "Data Exploration", "Chart View"])

if select == "Home":
    
    st.header("Welcome to :violet[PhonePe] project")
    st.markdown(":violet[PhonePe] is an Indian digital payments and financial technology company")
    st.image(Image.open(r"C:/Users/Ezhil/OneDrive/Desktop/python pro/How-PhonePe-earns-money-StartupTalky.jpg"))



elif select =="Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method=st.radio("Select Method",["Aggregated Transaction", "Aggregated User"])

        if method == "Aggregated Transaction":

            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("Selet Year", Aggre_transaction["Years"].unique())
            tac_Y= Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select States",tac_Y["States"].unique())

            aggre_Tran_Type(tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Selet Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(),tac_Y["Quarter"].min())

            tac_Y_Q = Transaction_amount_count_Y_Q(tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select States Type",tac_Y_Q["States"].unique())

            aggre_Tran_Type(tac_Y_Q,states)

        elif method == "Aggregated User":

            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("Selet Year", Aggre_user["Years"].unique())
            aggr_user_Y= aggre_user_plot_1(Aggre_user,years)


            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Selet Quarter", aggr_user_Y["Quarter"].min(), aggr_user_Y["Quarter"].max(),aggr_user_Y["Quarter"].min())

            aggr_user_Y_Q = aggre_user_plot_2(aggr_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select States",aggr_user_Y_Q["States"].unique())

            aggre_user_plot_3(aggr_user_Y_Q,states)



    
    with tab2:
        method2=st.radio("Select Method",["Map Transaction","Map User" ])

        if method2 == "Map Transaction":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("SELECT Year", Map_transaction["Years"].unique())
            map_tac_Y= Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States",map_tac_Y["States"].unique())

            map_transac_district(map_tac_Y,states)


            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose Quarter", map_tac_Y["Quarter"].min(), map_tac_Y["Quarter"].max(),map_tac_Y["Quarter"].min())

            map_tac_Y_Q = Transaction_amount_count_Y_Q(map_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("choose States Type",map_tac_Y_Q["States"].unique())

            map_transac_district(map_tac_Y_Q,states)

        elif method2 == "Map User":

            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("SELECT YEAR", Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose  User Quarter", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())

            map_user_Y_Q = map_user_plot_2(map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose_States",map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q,states)

    
    with tab3:
        method3=st.radio("Select Method",["Top Transaction","Top User" ])

        if method3 == "Top Transaction":

            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("SELECT Top Year", Top_transaction["Years"].unique())
            top_tac_Y= Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose Top States",top_tac_Y["States"].unique())

            top_transac_plot_1(top_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose  Top Quarter", top_tac_Y["Quarter"].min(), top_tac_Y["Quarter"].max(),top_tac_Y["Quarter"].min())

            top_tac_Y_Q = Transaction_amount_count_Y_Q(top_tac_Y,quarters)

            

        elif method3 == "Top User":

            col1,col2=st.columns(2)
            with col1:

                years=st.selectbox("SELECT TOP YEAR", Top_user["Years"].unique())
            top_user_Y= top_user_plot_1(Top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose Top States",top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y,states)

elif select =="Chart View":
    
    dropdowns=st.selectbox("Select the Dropdown",["1. Show the top 10 transaction amount of aggregated transaction",
                                                  "2. Show the least 10 transaction count of aggregated transaction",
                                                  "3. Show the top 10 transaction amount of map transaction",
                                                  "4. Show the least 10 transaction count of map transaction",
                                                  "5. Show the top 10 transaction amount of top transaction",
                                                  "6. Show the least 10 transaction count of top transaction",
                                                  "7. Show the average  transaction amount of aggregated transaction",
                                                  "8. Show the average  transaction amount of map transaction",
                                                  "9. Show the average  transaction amount of top transaction",
                                                  "10. Show the average  transaction count of aggregated transaction"])

    if dropdowns== "1. Show the top 10 transaction amount of aggregated transaction":

        table_view1("aggregated_transactionn")

    elif dropdowns== "2. Show the least 10 transaction count of aggregated transaction":

        table_view2("aggregated_transactionn")

    elif dropdowns== "3. Show the top 10 transaction amount of map transaction":
        
        table_view1("map_transactionn")
    
    elif dropdowns== "4. Show the least 10 transaction count of map transaction":

        table_view2("map_transactionn")
    
    elif dropdowns== "5. Show the top 10 transaction amount of top transaction":

        table_view1("top_transactionn")

    elif dropdowns== "6. Show the least 10 transaction count of top transaction":

        table_view2("top_transactionn")
    
    elif dropdowns== "7. Show the average  transaction amount of aggregated transaction":

        table_average_amount("aggregated_transactionn")

    elif dropdowns== "8. Show the average  transaction amount of map transaction":

        table_average_amount("map_transactionn")

    elif dropdowns== "9. Show the average  transaction amount of top transaction":

        table_average_amount("top_transactionn")

    elif dropdowns=="10. Show the average  transaction count of aggregated transaction":

        table_average_count("aggregated_transactionn")










