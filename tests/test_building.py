from datetime import timedelta

import pytest

from simplesimple import Building


@pytest.fixture
def building():
    conditioned_floor_area = 100
    return Building(
        heat_mass_capacity=165000 * conditioned_floor_area,
        heat_transmission=200,
        maximum_cooling_power=float("-inf"),
        maximum_heating_power=float("inf"),
        initial_building_temperature=22,
        time_step_size=timedelta(hours=1),
        conditioned_floor_area=conditioned_floor_area)


@pytest.fixture
def fully_damped_building():
    conditioned_floor_area = 1
    return Building(
        heat_mass_capacity=3600 * conditioned_floor_area,
        heat_transmission=0,
        maximum_cooling_power=-1,
        maximum_heating_power=1,
        initial_building_temperature=22,
        time_step_size=timedelta(hours=1),
        conditioned_floor_area=conditioned_floor_area)


def test_maximum_heating_power_cannot_be_negative():
    with pytest.raises(ValueError):
        conditioned_floor_area = 100
        Building(
            heat_mass_capacity=165000 * conditioned_floor_area,
            heat_transmission=200,
            maximum_cooling_power=float("-inf"),
            maximum_heating_power=-0.01,
            initial_building_temperature=22,
            time_step_size=timedelta(hours=1),
            conditioned_floor_area=conditioned_floor_area
        )


def test_maximum_cooling_power_cannot_be_positive():
    with pytest.raises(ValueError):
        conditioned_floor_area = 100
        Building(
            heat_mass_capacity=165000 * conditioned_floor_area,
            heat_transmission=200,
            maximum_cooling_power=0.01,
            maximum_heating_power=float("inf"),
            initial_building_temperature=22,
            time_step_size=timedelta(hours=1),
            conditioned_floor_area=conditioned_floor_area
        )


def test_building_temperature_remains_constant_when_same_temperature_outside(building):
    building.step(outside_temperature=22, heating_setpoint=21.9, cooling_setpoint=26)
    assert building.current_temperature == 22


def test_building_temperature_raises_when_warmer_outside(building):
    building.step(outside_temperature=23, heating_setpoint=21.9, cooling_setpoint=26)
    assert building.current_temperature > 22


def test_building_temperature_sinks_when_colder_outside(building):
    building.step(outside_temperature=21, heating_setpoint=21.9, cooling_setpoint=26)
    assert building.current_temperature < 22


def test_building_gets_heated_when_below_heating_setpoint(building):
    building.step(outside_temperature=22, heating_setpoint=23, cooling_setpoint=26)
    assert building.current_temperature > 22
    assert building.current_temperature <= 23


def test_building_gets_cooled_when_above_cooling_setpoint(building):
    building.step(outside_temperature=22, heating_setpoint=20, cooling_setpoint=21)
    assert building.current_temperature < 22
    assert building.current_temperature >= 21


def test_building_gets_heated_with_max_power_when_too_cold(fully_damped_building):
    fully_damped_building.step(outside_temperature=22, heating_setpoint=23, cooling_setpoint=26)
    assert fully_damped_building.current_temperature == 23


def test_building_does_not_exceed_max_heating_power(fully_damped_building):
    fully_damped_building.step(outside_temperature=22, heating_setpoint=24, cooling_setpoint=26)
    assert fully_damped_building.current_temperature == 23


def test_building_gets_cooled_with_max_power_when_too_warm(fully_damped_building):
    fully_damped_building.step(outside_temperature=22, heating_setpoint=18, cooling_setpoint=21)
    assert fully_damped_building.current_temperature == 21


def test_building_does_not_exceed_max_cooling_power(fully_damped_building):
    fully_damped_building.step(outside_temperature=22, heating_setpoint=18, cooling_setpoint=20)
    assert fully_damped_building.current_temperature == 21
