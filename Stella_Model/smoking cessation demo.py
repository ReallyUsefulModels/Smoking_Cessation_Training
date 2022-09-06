"""
Python model 'smoking cessation demo.py'
Translated using PySD
"""

from pathlib import Path
import xarray as xr

from pysd.py_backend.statefuls import Integ, Initial
from pysd import Component

__pysd_version__ = "3.6.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


_subscript_dict = {"Dim_Name_1": []}

component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 36,
    "time_step": lambda: 0.25,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="INITIAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Effect on spend per quitter",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"current_smokers": 1, "_initial_effect_on_spend_per_quitter": 1},
    other_deps={
        "_initial_effect_on_spend_per_quitter": {
            "initial": {"current_smokers": 1},
            "step": {},
        }
    },
)
def effect_on_spend_per_quitter():
    return current_smokers() / _initial_effect_on_spend_per_quitter()


_initial_effect_on_spend_per_quitter = Initial(
    lambda: current_smokers(), "_initial_effect_on_spend_per_quitter"
)


@component.add(
    name="Smokers quitting",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smoking_cessation_service_funding": 1, "spend_per_quitter": 1},
)
def smokers_quitting():
    return smoking_cessation_service_funding() / spend_per_quitter()


@component.add(
    name="Healthcare savings",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ex_smokers": 1, "monthly_cost_savings_per_ex_smoker": 1},
)
def healthcare_savings():
    return ex_smokers() * monthly_cost_savings_per_ex_smoker()


@component.add(
    name="Monthly cost savings per ex smoker",
    comp_type="Constant",
    comp_subtype="Normal",
)
def monthly_cost_savings_per_ex_smoker():
    return 50


@component.add(
    name="Smoking cessation service funding",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"healthcare_savings": 1, "percentage_of_savings_spent_on_cessation": 1},
)
def smoking_cessation_service_funding():
    return healthcare_savings() * (percentage_of_savings_spent_on_cessation() / 100)


@component.add(
    name="Spend per quitter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_on_spend_per_quitter": 1},
)
def spend_per_quitter():
    return 200 / effect_on_spend_per_quitter()


@component.add(
    name="Percentage of savings spent on cessation",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_of_savings_spent_on_cessation():
    return 80


@component.add(
    name="Average quitter failure rate", comp_type="Constant", comp_subtype="Normal"
)
def average_quitter_failure_rate():
    return 0.05


@component.add(
    name="Ex smokers starting again",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ex_smokers": 1, "average_quitter_failure_rate": 1},
)
def ex_smokers_starting_again():
    return ex_smokers() * average_quitter_failure_rate()


@component.add(
    name="Current smokers",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_current_smokers": 1},
    other_deps={
        "_integ_current_smokers": {"initial": {}, "step": {"smokers_quitting": 1}}
    },
)
def current_smokers():
    return _integ_current_smokers()


_integ_current_smokers = Integ(
    lambda: -smokers_quitting(), lambda: 900, "_integ_current_smokers"
)


@component.add(
    name="Ex smokers",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ex_smokers": 1},
    other_deps={
        "_integ_ex_smokers": {
            "initial": {},
            "step": {"smokers_quitting": 1, "ex_smokers_starting_again": 1},
        }
    },
)
def ex_smokers():
    return _integ_ex_smokers()


_integ_ex_smokers = Integ(
    lambda: smokers_quitting() - ex_smokers_starting_again(),
    lambda: 100,
    "_integ_ex_smokers",
)


@component.add(
    name="Lapsed ex smokers",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lapsed_ex_smokers": 1},
    other_deps={
        "_integ_lapsed_ex_smokers": {
            "initial": {},
            "step": {"ex_smokers_starting_again": 1},
        }
    },
)
def lapsed_ex_smokers():
    return _integ_lapsed_ex_smokers()


_integ_lapsed_ex_smokers = Integ(
    lambda: ex_smokers_starting_again(), lambda: 0, "_integ_lapsed_ex_smokers"
)
