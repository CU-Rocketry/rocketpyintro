#Environment
from rocketpy import Environment, SolidMotor, Rocket, Flight

env = Environment() 

env.plots.atmospheric_model()

#Motor
motor = SolidMotor(
    thrust_source="AeroTech_M2500T.eng", #Defines the thrust of the motor over time. We need to use a file to specify. 
    dry_mass=3.35,#mass of the rocket body without the motor attatched (kg)
#rotational inertia of the rocket body; calculated about center of mass without the motor
  #dry_inertia is a tuple (I11, I22, I33); I11 and I22 are the inertia of the dry mass (just the rocket body) around the perpendicular axes to the motor. I33 is the inertia around the motor center axis. 
    center_of_dry_mass_position=0.317,#position of the center of mass of the propellant grains
    dry_inertia=[0.1633, 0.1633, 0.0041], 
    grains_center_of_mass_position=0.3175,
    grain_number=4,#number of propellant grains in the solid motor
    grain_density=1815,#the density (mass/volume) of the propellant 
    grain_outer_radius=0.0875/2,#outer radius of each grain of solid propellant 
    grain_initial_inner_radius=0.0285/2, #start of the burn
    grain_initial_height=0.1524,
    grain_separation=0.005,  #spacing between grains
    nozzle_radius=0.085/2, #radius of the motor's nozzle (m)
    nozzle_position=-.115,
    throat_radius=0.0354/2,
    reshape_thrust_curve=False,  # Not implemented in Rocket-Serializer
    interpolation_method="linear",
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)
#motor.all_info()
print(f"Burn Start Time: {motor.burn_start_time}")
print(f"Total Burn Duration: {motor.burn_duration}")
print(f"Burn Out Time: {motor.burn_out_time}")

rocket = Rocket(
    radius=0.065405,
    mass=24.526,
    inertia=[0.089, 0.089, 17.184],
    power_off_drag="drag.csv",
    power_on_drag="drag.csv",
    center_of_mass_without_motor=1.756,
    coordinate_system_orientation="nose_to_tail"
)

#nose to tail (nose tip is at 0.0 and position numbers increase as you move down toward the tail) 

#adding surfaces to rocket
nose_cone = rocket.add_nose(length=0.6604, kind="vonKarman", position=0.0, base_radius=0.065405,name="0.6604") 
rocket.add_motor(motor, position=2.85)


fin_set = rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.2794,
    tip_chord=0.2032,
    span=0.10795,
    position=2.57, 
    cant_angle=0.0,
    sweep_length=0.1016,
    sweep_angle=None,
    name="Trapezoidal Fin Set",
)  

tail = rocket.add_tail(
    top_radius=0.065405, bottom_radius=0.053974999999999995, length=0.07619999999999999, position=2.85115,name="Tailcone"
)

rocket.draw()

#DUAL DEPLOYMENT
#parachutes
alt_deploy_main=304.8 #pick an altitude the main parachute deploys at

Main = rocket.add_parachute(
    "Main",
    cd_s=13.124,
    trigger=alt_deploy_main,
    sampling_rate=100,
    lag=1.5,
)

Drogue = rocket.add_parachute(
    "Drogue",
    cd_s=0.880,
    trigger="apogee",
    sampling_rate=100,
    lag=0.5,
    )

# Flight
test_flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=5.6,
    inclination=85.0,
    heading=90.0,
)

test_flight.plots.trajectory_3d()