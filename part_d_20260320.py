import pandas as pd
import pypsa
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# LOAD DATA
# -------------------------
df_elec = pd.read_csv('data/electricity_demand.csv', sep=';', index_col=0)
df_elec.index = pd.to_datetime(df_elec.index)

print("Electricity demand head:\n", df_elec.head())


df_onshorewind = pd.read_csv('data/onshore_wind_1979-2017.csv', sep=';', index_col=0)
df_onshorewind.index = pd.to_datetime(df_onshorewind.index)

df_offshorewind = pd.read_csv('data/offshore_wind_1979-2017.csv', sep=';', index_col=0)
df_offshorewind.index = pd.to_datetime(df_offshorewind.index)

df_solar = pd.read_csv('data/pv_optimal.csv', sep=';', index_col=0)
df_solar.index = pd.to_datetime(df_solar.index, utc=True)  

country = 'DNK'

# -------------------------
# NETWORK
# -------------------------
network = pypsa.Network()

# snapshots: create UTC-aware first, then convert to naive for PyPSA
hours_utc = pd.date_range('2015-01-01 00:00','2015-12-31 23:00', freq='h', tz='UTC')
hours_naive = hours_utc.tz_convert(None)  # PyPSA requires naive timestamps
network.set_snapshots(hours_naive)

# Carriers
for c in ["gas","onshorewind","offshorewind","solar","hydro"]:
    network.add("Carrier",c)

# Buses
for c in ["Denmark","Sweden","Norway","Germany"]:
    network.add("Bus",f"bus {c}",v_nom=400)

# Lines
network.add("Line","DK-NO",bus0="bus Denmark",bus1="bus Norway",x=0.1,r=0.001,s_nom=1632)
network.add("Line","DK-DE",bus0="bus Denmark",bus1="bus Germany",x=0.1,r=0.001,s_nom=3485)
network.add("Line","DK-SE",bus0="bus Denmark",bus1="bus Sweden",x=0.1,r=0.001,s_nom=2415)
# network.add("Line","SE-NO",bus0="bus Sweden",bus1="bus Norway",x=0.1,r=0.001,s_nom=3945)
network.add("Line","SE-DE",bus0="bus Sweden",bus1="bus Germany",x=0.1,r=0.001,s_nom=615)
# network.add("Line","NO-DE",bus0="bus Norway",bus1="bus Germany",x=0.1,r=0.001,s_nom=1400)

# -------------------------
# LOADS
# -------------------------
network.add("Load","Denmark load",bus="bus Denmark",
            p_set=df_elec[country].values.flatten())

# network.add("Load","Germany load",bus="bus Germany",p_set=522260)
network.add("Load","Germany load",bus="bus Germany",
            p_set=df_elec["DEU"].reindex(hours_naive).fillna(0).values)
# network.add("Load","Sweden load",bus="bus Sweden",p_set=138710)
network.add("Load","Sweden load",bus="bus Sweden",
            p_set=df_elec["SWE"].reindex(hours_naive).fillna(0).values)
# network.add("Load","Norway load",bus="bus Norway",p_set=136700)
network.add("Load","Norway load",bus="bus Norway",
            p_set=df_elec["NOR"].reindex(hours_naive).fillna(0  ).values)

print("\nAnnual load (TWh):")

print("Denmark:", df_elec["DNK"].sum() / 1e6)
print("Germany:", df_elec["DEU"].sum() / 1e6)
print("Sweden:", df_elec["SWE"].sum() / 1e6)
print("Norway:", df_elec["NOR"].sum() / 1e6)
# -------------------------
# HELPER
# -------------------------
def annuity(n,r):
    return r/(1.-1./(1.+r)**n) if r>0 else 1/n

# -------------------------
# CAPACITY FACTORS
# -------------------------
# Use UTC-aware snapshots to match CSV, then fill missing hours with 0
CF_wind = df_onshorewind[country].reindex(hours_utc, fill_value=0)
CF_off = df_offshorewind[country].reindex(hours_utc, fill_value=0)


CF_solar_de = df_solar["DEU"].reindex(hours_utc, fill_value=0)
print("Solar DEU CF head:\n", CF_solar_de.head(20))
print("Germany solar CF min/max:", CF_solar_de.min(), CF_solar_de.max())
CF_solar_dk = df_solar["DNK"].reindex(hours_utc, fill_value=0)

CF_onshorewind_de = df_onshorewind["DEU"].reindex(hours_utc, fill_value=0)
CF_onshorewind_swe = df_onshorewind["SWE"].reindex(hours_utc, fill_value=0)
# -------------------------
# DENMARK GENERATORS
# -------------------------
network.add("Generator","Onshore wind Denmark",bus="bus Denmark",
            p_nom_extendable=True,
            capital_cost=annuity(27,0.07)*1118775,
            marginal_cost=0,p_max_pu=CF_wind.values)

network.add("Generator","Offshore wind Denmark",bus="bus Denmark",
            p_nom_extendable=True,
            capital_cost=annuity(27,0.07)*2115944,
            marginal_cost=0,p_max_pu=CF_off.values)

network.add("Generator","Solar Denmark",bus="bus Denmark",
            p_nom_extendable=True,
            capital_cost=annuity(25,0.07)*450000,
            marginal_cost=0,p_max_pu=CF_solar_dk.values)

network.add("Generator","OCGT Denmark",bus="bus Denmark",
            p_nom_extendable=True,
            capital_cost=annuity(25,0.07)*453960,
            marginal_cost=30/0.41)

network.add("Generator","CCGT Denmark",bus="bus Denmark",
            p_nom_extendable=True,
            capital_cost=annuity(25,0.07)*880000,
            marginal_cost=30/0.56)

# -------------------------
# NEIGHBOUR GENERATION
# -------------------------
network.add("Generator","Solar Germany",bus="bus Germany",
            p_nom_extendable=True,
            capital_cost=annuity(25,0.07)*450000,
            p_max_pu=CF_solar_de.values,
            marginal_cost=30)

network.add("Generator","Onshore wind Germany",bus="bus Germany",
            p_nom_extendable=True,
            capital_cost=annuity(27,0.07)*1118775,
            p_max_pu=CF_onshorewind_de.values,
            marginal_cost=20)

network.add("Generator","Onshore wind Sweden",bus="bus Sweden",
            p_nom_extendable=True,
            capital_cost=annuity(27,0.07)*1118775,
            p_max_pu=CF_onshorewind_swe.values,
            marginal_cost=20)

network.add("Generator","Gas Norway",bus="bus Norway",
            p_nom_extendable=True,
            marginal_cost=30/0.56)

# -------------------------
# HYDRO 
# -------------------------
# hydro Sweden
_df_hydro = pd.read_csv('data/inflow/Hydro_Inflow_SE.csv')
_df_hydro['date'] = pd.to_datetime(_df_hydro[['Year','Month','Day']])
_df_hydro['doy'] = _df_hydro['date'].dt.dayofyear

_avg_inflow = _df_hydro.groupby('doy')['Inflow [GWh]'].mean()

_inflow_gwh = pd.Series(
    [_avg_inflow.loc[ts.dayofyear] for ts in hours_naive],
    index=hours_naive
)
_inflow_mw_swe = _inflow_gwh * 1000 / 24
network.add(
    "StorageUnit",
    "Hydro Sweden",
    bus="bus Sweden",
    carrier="hydro",
    p_nom=16510,
    max_hours=2,
    inflow=_inflow_mw_swe,
    marginal_cost=20 # increased marginal cost to reflect higher opportunity cost of water in Sweden, which has more hydro resources
)
# hydro Norway


_df_hydro = pd.read_csv('data/inflow/Hydro_Inflow_NO.csv')
_df_hydro['date'] = pd.to_datetime(_df_hydro[['Year','Month','Day']])
_df_hydro['doy'] = _df_hydro['date'].dt.dayofyear

_avg_inflow = _df_hydro.groupby('doy')['Inflow [GWh]'].mean()

_inflow_gwh = pd.Series(
    [_avg_inflow.loc[ts.dayofyear] for ts in hours_naive],
    index=hours_naive
)

_inflow_mw_nor = _inflow_gwh * 1000 / 24

network.add(
    "StorageUnit",
    "Hydro Norway",
    bus="bus Norway",
    carrier="hydro",
    p_nom=16510,
    max_hours=2,
    inflow=_inflow_mw_nor,
    marginal_cost=20 # increased marginal cost to reflect higher opportunity cost of water in Norway, which has more hydro resources
)

# -------------------------
# OPTIMIZATION
# -------------------------
network.optimize(solver_name='highs')

network.storage_units_t.p_dispatch
print("\nHydro generation (TWh):")
print(network.storage_units_t.p_dispatch.sum() / 1e6)
print(network.storage_units_t.p_dispatch.describe())

print("Status:", network.model.status)
print("Termination:", network.model.termination_condition)

# -------------------------
# RESULTS
# -------------------------
if network.model.status == "ok":

    print("\nInstalled capacities (GW):")
    print(network.generators.p_nom_opt.div(1e3))

    print("\nTotal generation (TWh):")
    print(network.generators_t.p.sum().div(1e6))



else:
    print("Optimization failed.")