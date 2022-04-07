import requests
import numpy as np
import pandas as pd


if __name__ == "__main__":
    host = "http://localhost:5000"

    dat = pd.DataFrame(np.random.uniform(0,1,(10,12)), 
                    columns=[
                            "wind_speed",
                            "power",
                            "nacelle_direction",
                            "wind_direction",
                            "rotor_speed",
                            "generator_speed",
                            "temp_environment",
                            "temp_hydraulic_oil",
                            "temp_gear_bearing",
                            "cosphi",
                            "blade_angle_avg",
                            "hydraulic_pressure"
                        ]
                    )

    data={"data": dat.to_json()}

    print(requests.post(host, json=data).json())