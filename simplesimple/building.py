class Building():
    """A simple Building Energy Model.

    Consisting of one thermal capacity and one resistance, this model is derived from the
    hourly dynamic model of the ISO 13790. It models heating and cooling energy demand only.

    Parameters:
        * heat_mass_capacity:           capacity of the building's heat mass [J/K]
        * heat_transmission:            heat transmission to the outside [W/K]
        * maximum_cooling_power:        [W] (<= 0)
        * maximum_heating_power:        [W] (>= 0)
        * initial_building_temperature: building temperature at start time [℃]
        * time_step_size:               [s]
        * conditioned_floor_area:       [m**2]
    """

    def __init__(self, heat_mass_capacity, heat_transmission,
                 maximum_cooling_power, maximum_heating_power,
                 initial_building_temperature, time_step_size,
                 conditioned_floor_area):
        if maximum_heating_power < 0:
            raise ValueError("Maximum heating power [W] must not be negative.")
        if maximum_cooling_power > 0:
            raise ValueError("Maximum cooling power [W] must not be positive.")
        self.__heat_mass_capacity = heat_mass_capacity
        self.__heat_transmission = heat_transmission
        self.__maximum_cooling_power = maximum_cooling_power
        self.__maximum_heating_power = maximum_heating_power
        self.current_temperature = initial_building_temperature
        self.thermal_power = 0
        self.__time_step_size = time_step_size
        self.__conditioned_floor_area = conditioned_floor_area

    def step(self, outside_temperature, heating_setpoint, cooling_setpoint):
        """Performs building simulation for the next time step.

        Parameters:
            * outside_temperature: [℃]
            * heating_setpoint: heating setpoint of the HVAC system [℃]
            * cooling_setpoint: cooling setpoint of the HVAC system [℃]
        """
        def next_temperature(heating_cooling_power):
            return self._next_temperature(
                outside_temperature=outside_temperature,
                heating_setpoint=heating_setpoint,
                cooling_setpoint=cooling_setpoint,
                heating_cooling_power=heating_cooling_power
            )
        next_temperature_no_power = next_temperature(0)
        if (next_temperature_no_power >= heating_setpoint and
                next_temperature_no_power <= cooling_setpoint):
            self.current_temperature = next_temperature_no_power
        else:
            if next_temperature_no_power < heating_setpoint:
                setpoint = heating_setpoint
                max_power = self.__maximum_heating_power
            else:
                setpoint = cooling_setpoint
                max_power = self.__maximum_cooling_power
            ten_watt_per_square_meter_power = 10 * self.__conditioned_floor_area
            next_temperature_power_10 = next_temperature(ten_watt_per_square_meter_power)
            unrestricted_power = (ten_watt_per_square_meter_power *
                                  (setpoint - next_temperature_no_power) /
                                  (next_temperature_power_10 - next_temperature_no_power))
            if abs(unrestricted_power) <= abs(max_power):
                self.thermal_power = unrestricted_power
            else:
                self.thermal_power = max_power
            next_temperature_heating_cooling = next_temperature(self.thermal_power)
            self.current_temperature = next_temperature_heating_cooling

    def _next_temperature(self, outside_temperature, heating_setpoint, cooling_setpoint,
                          heating_cooling_power):
        dt_by_cm = self.__time_step_size.total_seconds() / self.__heat_mass_capacity
        return (self.current_temperature * (1 - dt_by_cm * self.__heat_transmission) +
                dt_by_cm * (heating_cooling_power + self.__heat_transmission * outside_temperature))
