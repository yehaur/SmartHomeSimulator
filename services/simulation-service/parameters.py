Paras = {
  'T_end': 96, # 24 hours, each divided by 15 minutes (0.25 below) 
  'DeltaT': 0.25, # 15 minutes
  # Grid
  'IBR': 1.4423,  # IBR factor
  'PowerGridMax': 6,  # max power limit from grid 6 kW
  # PV
  'ConversionEfficiency': 0.2,
  'Area': 15,
  # Neural network
  'Layers': 3,  # 3 hidden layers
  'NeuronsPerLayer': 128,
  # Shiftable Appliances
  #              kW       t_ini          t_end
  'DishWasher': [1.8, [40,44,42,2], [58,62,60,2]], # t_ini, t_end truncated normal distribution TN (μ, σ, min, max) 
  'K_DishWasher': 3,
  'WashMachine': [0.4, [6,10,8,4], [36,44,40,4]],
  'K_WashMachine': 6,
  'ClothesDryer': 1.2,   # t_ini = WashMachine t_end; t_end = t_ini + 8
  'K_ClothesDryer': 5,
  # Controllable appliances
  #      kW  t_ini t_end
  'AC': [2.5, 0, 96],
  'EWH': [4.5, 0, 96],
  'EV': [6.0, [36,44,40,4], [92,96,94,2]],
  'ESS': [2.4, 0, 96],
     #Paras of controllable appliances
     'HVAC_iner': 0.968,  # factor of inertia
     'HVAC_conv': 1.0,  # thermal conversion efficiency
     'HVAC_cond': 0.00727,  # mean thermal conductivity of house (kW/celsius)
     'HVAC_conv_in': 0.01,  #  conversion coefficient of indoor temperature comfort
     'HVAC_set': 22,  # preset value of indoor temperature (celsius, paper said 22, this dataset temperature not high)
     'HVAC_max_dev': 2,  # maximum allowable deviation of the indoor temperature (celsius)
     'EWH_den': 1,  # water density (kg/liter) #### wrong unit in paper!
     'EWH_cap': 4200,  # heat capacity of water (J/ (kg * celsus))
     'EWH_cond': 2.6,  # thermal conductivity of the water tank (kW/celsius)
     'EWH_cold': 15,  # temperature of the replenishing cold water (celsius)
     'EWH_hwf': [0.01, 0.025, 0.016, 0.01],  # Hot water flow rate (L / s)
                     #!!!!!!!!!!!!!!!!!!! the original paper only said it's randomly generated by TN, but didn't give any parameters, so I made up 
     'EWH_conv': 0.01,  # conversion coefficient of water temperature comfort
     'EWH_set': 60,  # preset water temperature
     'EWH_max_dev': 3, # max allowable deviation of water temperature
     'EV_effi': 0.95,  # EV charging efficiency
     'EV_cap': 24,  # battery capacity of EV (kWh)
     'EV_anxiety': 0.05,  # ange anxiety conversion factor ($/kWh^2)
     'ESS_effi_ch': 0.95,  # charging efficiencies of ESS
     'ESS_effi_dis': 0.95,  # discharging efficiencies of ESS
     'ESS_cap': 6.4,  # battery capacity of ESS (kWh)
     'ESS_cost': 6.4 * 120,  # cost of the battery units ($/kWh)
     'ESS_Fmax': 0.2,  # maximum capacity fade constant
  # Non shiftable appliances
  #      KW       t_ini     duration
  'TV': [0.1, [40,44,42,2], [14,18,16,2]],
  'refrige': [0.2, 0, 96],
  'light': [0.2, [32,40,36,4], [18,22,20,2]],
  'vacuum': [1.2, [24,32,28,4], [1,5,3,2]],
  'hairdryer': [1.0, [48,52,50,2], 1],
  # PPO agent parameters
  'proc_size': 60,  # trajectory size
  'Mep': 2500,  # max number of episodes
  'N': 20,  # iteration
  'c1': 0.01,  # hyper para in loss function
  'c2': 0.5,  # hyper para in loss
  'epsilon': 0.2,  # para in clip(...) function (1-epsilon, 1+epsilon)*A_t
  'gamma': 0.995,  # Discount factor
  'lambda': 0.97,  # estimating factor
}

from scipy.stats import truncnorm

def TN(left, right, mu, sigma, size=1):
  if left >= right:
    raise ValueError(f"Invalid range: left bound ({left}) must be less than right bound ({right}).")
  if not (left < mu < right):
    raise ValueError(f"Invalid mu: mu ({mu}) must be between ({left}) and  ({right}).")
  if sigma <= 0:
    raise ValueError(f"Invalid sigma: sigma ({sigma}) must be greater than 0.")
  if size <= 0:
    raise ValueError(f"Invalid size: size ({size}) must be greater than 0.")

  lower, upper = (left - mu) / sigma, (right - mu) / sigma 
  res = truncnorm(lower, upper, loc=mu, scale=sigma).rvs(size=size)
  if(size == 1):
    return res[0]
  return res