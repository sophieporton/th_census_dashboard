# %%
#read in required packages

import streamlit as st 
import plotly.express as px
import pandas as pd
import geopandas as gpd

# %%
#define function for mapping wards by variable

def plot_wards(df, column='', string='', agg='',title=''):
    df=df[df.MEASURES_NAME== 'Value']
    df=df[df[column].str.contains(string)==True]
    fig = px.choropleth(df.dissolve(by='ward_name', aggfunc ={'OBS_VALUE':agg}),
                   geojson=df.dissolve(by='ward_name', aggfunc ={'OBS_VALUE':agg}).geometry,
                   locations=df.dissolve(by='ward_name',aggfunc ={'OBS_VALUE':agg}).index,
                   color="OBS_VALUE",
                   color_continuous_scale = 'viridis_r',
                   projection="mercator",
                   hover_name=df.dissolve(by='ward_name',aggfunc ={'OBS_VALUE':agg}).index )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(coloraxis_colorbar=dict(title=title))
    fig.show()
    #st.plotly_chart(fig,use_container_width = True)

# %%
#define function for merging spatial and variable data 

def merge_spatial_data(gdf, df, left_on="", right_on=""):
    gdf=gdf.merge(df, left_on=left_on, right_on=right_on)
    return gdf

# %%
merged_wd_oa = st.session_state['merged_wd_oa']

# %%
#read in and merge ethncity oa datasets (in 2 parts as nomis only allows download of 25,000 cells at a time)

ethnicity_oa_1=pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2041_1.data.csv?date=latest&geography=629165479...629165982,629303674...629303812,629317322...629317326,629317336...629317343,629317349...629317360,629317362...629317366,629317371,629317374,629317376,629317378,629317379,629317381,629317385,629317388...629317392,629317394...629317397,629317399...629317403,629317405...629317407,629317409,629317411,629317412,629317416...629317420,629317422...629317424,629317426,629317429...629317434,629317436,629317437,629317440...629317442,629317444...629317450,629317452...629317456,629317459...629317461,629317463,629317466...629317468,629317472,629317474...629317479,629317481,629317483,629317486,629317487,629317490,629317492,629317494,629317495,629317497,629317499...629317502,629317504,629317505,629317507...629317509,629317512...629317514,629317517,629317520,629317523,629317525,629317527,629317531,629317534,629317535,629317537,629317538,629317540,629317543...629317548,629317551,629317554,629317555,629317558,629317560,629317562,629317563,629317565,629317566,629317569...629317573,629317576...629317578,629317580,629317582,629317584,629317585,629317587,629317590...629317592,629317594,629317596...629317599,629317601,629317603,629317604,629317606,629317607,629317610,629317612,629317613,629317615...629317617,629317619...629317621,629317623,629317625...629317629,629317631...629317634,629317636,629317640,629317648,629317650...629317659,629317662,629317663,629317666...629317669,629317672...629317687,629317689,629317691,629317694,629317695,629317697,629317698,629317700,629317701,629317703,629317704,629317706,629317707,629317711...629317714,629317716,629317718...629317720,629317722...629317724,629317726,629317729,629317731,629317733,629317736...629317742,629317744,629317746...629317748,629323624,629323625&c2021_eth_20=1001,12,13,10,11,14,1002,16,15,17,1003,8,7,6,9,1004,1...5,1005,18,19&measures=20100,20301&select=date_name,geography_name,geography_code,c2021_eth_20_name,measures_name,obs_value,obs_status_name')

ethnicity_oa_2=pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2041_1.data.csv?date=latest&geography=629165479...629165982,629303674...629303812,629317322...629317326,629317336...629317343,629317349...629317360,629317362...629317366,629317371,629317374,629317376,629317378,629317379,629317381,629317385,629317388...629317392,629317394...629317397,629317399...629317403,629317405...629317407,629317409,629317411,629317412,629317416...629317420,629317422...629317424,629317426,629317429...629317434,629317436,629317437,629317440...629317442,629317444...629317450,629317452...629317456,629317459...629317461,629317463,629317466...629317468,629317472,629317474...629317479,629317481,629317483,629317486,629317487,629317490,629317492,629317494,629317495,629317497,629317499...629317502,629317504,629317505,629317507...629317509,629317512...629317514,629317517,629317520,629317523,629317525,629317527,629317531,629317534,629317535,629317537,629317538,629317540,629317543...629317548,629317551,629317554,629317555,629317558,629317560,629317562,629317563,629317565,629317566,629317569...629317573,629317576...629317578,629317580,629317582,629317584,629317585,629317587,629317590...629317592,629317594,629317596...629317599,629317601,629317603,629317604,629317606,629317607,629317610,629317612,629317613,629317615...629317617,629317619...629317621,629317623,629317625...629317629,629317631...629317634,629317636,629317640,629317648,629317650...629317659,629317662,629317663,629317666...629317669,629317672...629317687,629317689,629317691,629317694,629317695,629317697,629317698,629317700,629317701,629317703,629317704,629317706,629317707,629317711...629317714,629317716,629317718...629317720,629317722...629317724,629317726,629317729,629317731,629317733,629317736...629317742,629317744,629317746...629317748,629323624,629323625&c2021_eth_20=0,1001,12,13,10,11,14,1002,16,15,17,1003,8,7,6,9,1004,1...5,1005,18,19&measures=20100,20301&select=date_name,geography_name,geography_code,c2021_eth_20_name,measures_name,obs_value,obs_status_name&RecordOffset=25001')

ethnicity_oa = pd.concat([ethnicity_oa_1, ethnicity_oa_2])

# %%
#Check the correct number of oas

ethnicity_oa['GEOGRAPHY_NAME'].nunique()

# %%
#merge ethnicity data with spatial data
ethnicity_merge=merge_spatial_data(merged_wd_oa, ethnicity_oa,"OA21CD", "GEOGRAPHY_CODE")

# %%
#plotting 

st.header('Ethnicity')
page= st.sidebar.selectbox('Select variable',
  ['Asian, Asian British or Asian Welsh: Total','Asian, Asian British or Asian Welsh: Bangladeshi','Asian, Asian British or Asian Welsh: Chinese','Asian, Asian British or Asian Welsh: Indian',
  'Asian, Asian British or Asian Welsh: Pakistani','Asian, Asian British or Asian Welsh: Other Asian','Black, Black British, Black Welsh, Caribbean or African: Total','Black, Black British, Black Welsh, Caribbean or African: African',
  'Black, Black British, Black Welsh, Caribbean or African: Caribbean','Black, Black British, Black Welsh, Caribbean or African: Other Black','Mixed or Multiple ethnic groups: Total','Mixed or Multiple ethnic groups: White and Asian',
  'Mixed or Multiple ethnic groups: White and Black African','Mixed or Multiple ethnic groups: White and Black Caribbean',
'Mixed or Multiple ethnic groups: Other Mixed or Multiple ethnic groups','White: Total','White: English, Welsh, Scottish, Northern Irish or British',
'White: Irish','White: Gypsy or Irish Traveller','White: Roma','White: Other White','Other ethnic group: Total','Other ethnic group: Arab',
'Other ethnic group: Any other ethnic group'])

if page== 'Asian, Asian British or Asian Welsh: Total':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh', agg='sum',
  title='Number of people')

elif page== 'Asian, Asian British or Asian Welsh: Bangladeshi':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh: Bangladeshi', agg='sum',
  title='Number of people')

elif page== 'Asian, Asian British or Asian Welsh: Chinese':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh: Chinese', agg='sum',
  title='Number of people')

elif page== 'Asian, Asian British or Asian Welsh: Indian':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh: Indian', agg='sum',
  title='Number of people')

elif page== 'Asian, Asian British or Asian Welsh: Pakistani':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh: Pakistani', agg='sum',
  title='Number of people')

elif page== 'Asian, Asian British or Asian Welsh: Other Asian':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Asian, Asian British or Asian Welsh: Other Asian', agg='sum',
  title='Number of people')

elif page== 'Black, Black British, Black Welsh, Caribbean or African: Total':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Black, Black British, Black Welsh, Caribbean or African', agg='sum',
  title='Number of people')

elif page== 'Black, Black British, Black Welsh, Caribbean or African: African':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Black, Black British, Black Welsh, Caribbean or African: African', agg='sum',
  title='Number of people')

elif page== 'Black, Black British, Black Welsh, Caribbean or African: Caribbean':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Black, Black British, Black Welsh, Caribbean or African: Caribbean', agg='sum',
  title='Number of people')

elif page== 'Black, Black British, Black Welsh, Caribbean or African: Other Black':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Black, Black British, Black Welsh, Caribbean or African: Other Black', agg='sum',
  title='Number of people')

elif page== 'Mixed or Multiple ethnic groups: Total':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Mixed or Multiple ethnic groups', agg='sum',
  title='Number of people')

elif page== 'Mixed or Multiple ethnic groups: White and Asian':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Mixed or Multiple ethnic groups: White and Asian', agg='sum',
  title='Number of people')

elif page== 'Mixed or Multiple ethnic groups: White and Black African':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Mixed or Multiple ethnic groups: White and Black African', agg='sum',
  title='Number of people')

elif page== 'Mixed or Multiple ethnic groups: White and Caribbean':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Mixed or Multiple ethnic groups: White and Caribbean', agg='sum',
  title='Number of people')

elif page== 'Mixed or Multiple ethnic groups: Other Mixed or Multiple ethnic groups':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Mixed or Multiple ethnic groups: Other Mixed or Multiple ethnic groups', agg='sum',
  title='Number of people')

elif page== 'White: Total':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White', agg='sum',
  title='Number of people')

elif page== 'White: English, Welsh, Scottish, Northern Irish or British':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White: English, Welsh, Scottish, Northern Irish or British', agg='sum',
  title='Number of people')

elif page== 'White: Irish':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White: Irish', agg='sum',
  title='Number of people')

elif page== 'White: Gypsy or Irish Traveller':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White: Gypsy or Irish Traveller', agg='sum',
  title='Number of people')

elif page== 'White: Roma':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White: Roma', agg='sum',
  title='Number of people')

elif page== 'White: Other White':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='White: Other White', agg='sum',
  title='Number of people')

elif page== 'Other ethnic group: Total':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Other ethnic group', agg='sum',
  title='Number of people')

elif page== 'Other ethnic group: Arab':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Other ethnic group: Arab', agg='sum',
  title='Number of people')


elif page== 'Other ethnic group: Any other ethnic group':
  plot_wards(ethnicity_merge, column='C2021_ETH_20_NAME', string='Other ethnic group: Any other ethnic group', agg='sum',
  title='Number of people')




