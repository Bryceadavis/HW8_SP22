import Calc_state
from Calc_state import Steam_SI as steam
from Calc_state import SatPropsIsobar
import numpy as np
from matplotlib import pyplot as plt
from Calc_state import UnitConverter


class rankineModel():
    def __init__(self):
        """
        Constructor for rankine power cycle data (in the Model-View-Controller design pattern).  This class
        is for storing data only.  The Controller class should update the model depending on input from the user.
        The View class should display the model data depending on the desired output.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param eff_turbine: isentropic efficiency of the turbine
        :param name: a convenient name
        """
        self.p_low = None
        self.p_high = None
        self.t_high = None
        self.name = None
        self.efficiency = None
        self.turbine_eff = None
        self.turbine_work = None
        self.pump_work = None
        self.heat_added = None
        self.state1 = None
        self.state2s = None
        self.state2 = None
        self.state3 = None
        self.state4 = None


class rankineController():
    def __init__(self, *args):
        """
        Create rankineModel object.  The rankineController class updates the model based on user input
        and updates the rankineView as well
        :param *args: a tuple containing widgets that get updated in the View
        """

        self.Model = rankineModel()
        self.View = rankineView()
        self.Widgets = args[0]

    def updateUnits(self, *args, SI=True):
        """
        Passthrough Function
        :param Model: The proper result of our given inputs.
        :param args: widgets and otherwidgets
        :param SI: Should provide a boolean when the proper rdo buttons are clicked.
        :return:
        """

        # this function will be used as a Passthrough Function to Convert
        metric = SI
        model = self.Model
        self.View.Convert(*args, SI=metric, Model=model)

    def updateModel(self, *args, SI=True):
        """
        I'm expecting a tuple of input widgets from the GUI.  Read and apply them here.
        :param SI: Boolean to indicate that if False, we need to convert input values to SI for instantiation
        and calculation.
        :param args: a tuple of input widgets, other arguments such as SI or ENG
        :return: nothing
        """
        # unpack tuple of input widgets
        le_PHigh, le_PLow, rdo_Quality, le_TurbineInletCondition, le_TurbineEff = args[0]

        # update the model
        self.Model.p_high = le_PHigh  # get the high pressure isobar in kPa
        self.Model.p_low = le_PLow  # get the low pressure isobar in kPa
        self.Model.t_high = None if rdo_Quality.isChecked() else float(le_TurbineInletCondition)
        self.Model.turbine_eff = float(le_TurbineEff.text())
        # do the calculation
        self.calc_efficiency()
        self.updateView(self.Widgets)

    def calc_efficiency(self):
        # calculate the 4 states
        # state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if (self.Model.t_high == None):
            self.Model.state1 = steam(self.Model.p_high, x=1.0,
                                      name='Turbine Inlet')  # instantiate a steam object
            # with conditions of state 1 as saturated steam, named 'Turbine Inlet'
        else:
            self.Model.state1 = steam(self.Model.p_high, T=self.Model.t_high,
                                      name='Turbine Inlet')  # instantiate a steam object with
            # conditions of state 1 at t_high, named 'Turbine Inlet'
        # state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.Model.state2s = steam(self.Model.p_low, s=self.Model.state1.s,
                                   name="Turbine Exit")  # instantiate a steam object with conditions
        # of state 2s, named 'Turbine Exit'
        if self.Model.turbine_eff < 1.0:  # eff=(h1-h2)/(h1-h2s) -> h2=h1-eff(h1-h2s)
            h2 = self.Model.state1.h - self.Model.turbine_eff * (self.Model.state1.h - self.Model.state2s.h)
            self.Model.state2 = steam(self.Model.p_low, h=h2, name="Turbine Exit")
        else:
            self.Model.state2 = self.Model.state2s
        # state 3: pump inlet (p_low, x=0) saturated liquid
        self.Model.state3 = steam(self.Model.p_low, x=0,
                                  name='Pump Inlet')  # instantiate a steam object with conditions
        # of state 3 as saturated liquid, named 'Pump Inlet'
        # state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.Model.state4 = steam(self.Model.p_high, s=self.Model.state3.s, name='Pump Exit')
        self.Model.state4.h = self.Model.state3.h + self.Model.state3.v * (self.Model.p_high - self.Model.p_low)

        self.Model.turbine_work = self.Model.state1.h - self.Model.state2.h  # calculate turbine work
        self.Model.pump_work = self.Model.state4.h - self.Model.state3.h  # calculate pump work
        self.Model.heat_added = self.Model.state1.h - self.Model.state4.h  # calculate heat added
        self.Model.efficiency = 100.0 * (self.Model.turbine_work - self.Model.pump_work) / self.Model.heat_added
        return self.Model.efficiency

    def updateView(self, *args):
        """
        This is a pass-through function that calls and identically named function in the View, but passes along the
        Model as an argument.
        :param args: A tuple of Widgets that get unpacked and updated in the view
        :return:
        """
        self.View.outputToGUI(args[0], Model=self.Model)

    def setRankine(self, p_low=8, p_high=8000, t_high=None, eff_turbine=1.0, name='Rankine Cycle'):
        """
        Set model values for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param eff_turbine: isentropic efficiency of the turbine
        :param name: a convenient name
        """
        self.Model.p_low = p_low
        self.Model.p_high = p_high
        self.Model.t_high = t_high
        self.Model.name = name
        self.Model.efficiency = None
        self.Model.turbine_eff = eff_turbine
        self.Model.turbine_work = 0
        self.Model.pump_work = 0
        self.Model.heat_added = 0
        self.Model.state1 = None
        self.Model.state2s = None
        self.Model.state2 = None
        self.Model.state3 = None
        self.Model.state4 = None

    def print_summary(self):
        """
        A pass-through method for accessing View and passing Model.
        :return:
        """
        self.View.print_summary(Model=self.Model)

    def plot_cycle_TS(self, axObj=None):
        """
        A pass-through method for accessing View and passing Model.
        :return:
        """
        self.View.plot_cycle_TS(axObj=axObj, Model=self.Model)


class rankineView():
    def __init__(self):
        """
        Empty constructor by design
        """
        self.Model = rankineModel()

    def outputToGUI(self, *args, Model=None):
        # unpack the args
        le_H1, le_H2, le_H3, le_H4, le_TurbineWork, le_PumpWork, le_HeatAdded, le_Efficiency, lbl_SatPropHigh, lbl_SatPropLow, ax, canvas = \
        args[0]

        # update the line edits and labels
        le_H1.setText("{:0.2f}".format(Model.state1.h))
        le_H2.setText("{:0.2f}".format(Model.state2.h))
        le_H3.setText("{:0.2f}".format(Model.state3.h))
        le_H4.setText("{:0.2f}".format(Model.state4.h))
        le_TurbineWork.setText("{:0.2f}".format(Model.turbine_work))
        le_PumpWork.setText("{:0.2f}".format(Model.pump_work))
        le_HeatAdded.setText("{:0.2f}".format(Model.heat_added))
        le_Efficiency.setText("{:0.2f}".format(Model.efficiency))
        lbl_SatPropLow.setText(SatPropsIsobar(Model.p_low).txtOut)
        lbl_SatPropHigh.setText(SatPropsIsobar(Model.p_high).txtOut)

        # update the plot
        ax.clear()
        self.plot_cycle_TS(axObj=ax, Model=Model)
        canvas.draw()

    def print_summary(self, Model=None):
        """
        Prints to CLI.
        :param Model: a rankineModel object
        :return: nothing
        """
        if Model.efficiency == None:
            Model.calc_efficiency()
        print('Cycle Summary for: ', Model.name)
        print('\tEfficiency: {:0.2f}%'.format(Model.efficiency))
        print('\tTurbine Eff:  {:0.2f}'.format(Model.turbine_eff))
        print('\tTurbine Work: {:0.2f} kJ/kg'.format(Model.turbine_work))
        print('\tPump Work: {:0.2f} kJ/kg'.format(Model.pump_work))
        print('\tHeat Added: {:0.2f} kJ/kg'.format(Model.heat_added))
        Model.state1.print()
        Model.state2.print()
        Model.state3.print()
        Model.state4.print()

    def Convert(self, *args, SI=True, Model=None):
        metric = SI
        model = self.Model
        # Unpacking *args
        le_H1, le_H2, le_H3, le_H4, le_TurbineWork, le_PumpWork, le_HeatAdded, le_Efficiency, lbl_SatPropHigh, \
        lbl_SatPropLow, ax, canvas = args[0]
        # Unpacking *args
        le_PHigh, le_PLow, le_TurbineInletCondition, lbl_PHigh, lbl_PLow, lbl_H1Units, lbl_H2Units, lbl_H3Units, \
        lbl_H4Units, lbl_TurbineWorkUnits, lbl_PumpWorkUnits, lbl_HeatAddedUnits = args[1]
        PLow = SatPropsIsobar(Model.p_low).getTextOutput(SI)  # Plow SI
        PHigh = SatPropsIsobar(Model.p_high).getTextOutput(SI)
        lbl_SatPropLow.setText(PLow)  # setting labels
        lbl_SatPropHigh.setText(PHigh)  # setting labels
        ax.clear()  # Clear chart display
        self.plot_cycle_TS(axObj=ax, Model=Model, SI=SI)
        canvas.draw()

        if SI is True:
            lbl_H1Units.setText("kJ/kg")
            lbl_H2Units.setText("kJ/kg")
            lbl_H3Units.setText("kJ/kg")
            lbl_H4Units.setText("kJ/kg")
            lbl_PHigh.setText("P High (bar)")
            lbl_PLow.setText("P Low (bar)")
            ModelPHigh = Model.p_high / 100
            ModelPLow = Model.p_low / 100
            lbl_TurbineWorkUnits.setText("kJ/kg")
            lbl_PumpWorkUnits.setText("kJ/kg")
            lbl_HeatAddedUnits.setText("kJ/kg")
            le_PHigh.setText(str("{:0.2f}".format(ModelPHigh)))
            le_PLow.setText(str("{:0.2f}".format(ModelPLow)))
            le_H1.setText("{:0.2f}".format(Model.state1.h))
            le_H2.setText("{:0.2f}".format(Model.state2.h))
            le_H3.setText("{:0.2f}".format(Model.state3.h))
            le_H4.setText("{:0.2f}".format(Model.state4.h))
            le_TurbineWork.setText("{:0.2f}".format(Model.turbine_work))
            le_PumpWork.setText("{:0.2f}".format(Model.pump_work))
            le_HeatAdded.setText("{:0.2f}".format(Model.heat_added))

        if SI is False:
            lbl_H1Units.setText("BTU/lb")
            lbl_H2Units.setText("BTU/lb")
            lbl_H3Units.setText("BTU/lb")
            lbl_H4Units.setText("BTU/lb")
            lbl_PHigh.setText("P High (psi)")
            lbl_PLow.setText("P Low (psi)")
            lbl_TurbineWorkUnits.setText("BTU/lb")
            lbl_PumpWorkUnits.setText("BTU/lb")
            lbl_HeatAddedUnits.setText("BTU/lb")
            le_PHigh.setText(str('{:0.2f}'.format(float(Model.p_high) / 100 * UnitConverter.bar_to_psi)))
            le_PLow.setText(str('{:0.2f}'.format(float(Model.p_low) / 100 * UnitConverter.bar_to_psi)))
            le_H1.setText("{:0.2f}".format(Model.state1.h * UnitConverter.kJperkg_to_BTUperlb))
            le_H2.setText("{:0.2f}".format(Model.state2.h * UnitConverter.kJperkg_to_BTUperlb))
            le_H3.setText("{:0.2f}".format(Model.state3.h * UnitConverter.kJperkg_to_BTUperlb))
            le_H4.setText("{:0.2f}".format(Model.state4.h * UnitConverter.kJperkg_to_BTUperlb))
            le_TurbineWork.setText("{:0.2f}".format(Model.turbine_work * UnitConverter.kJperkg_to_BTUperlb))
            le_PumpWork.setText("{:0.2f}".format(Model.pump_work * UnitConverter.kJperkg_to_BTUperlb))
            le_HeatAdded.setText("{:0.2f}".format(Model.heat_added * UnitConverter.kJperkg_to_BTUperlb))

    def plot_cycle_TS(self, axObj=None, Model=None, SI=True):
        """
        I want to plot the Rankine cycle on T-S coordinates along with the vapor dome and shading in the cycle.
        I notice there are several lines on the plot:
        saturated liquid T(s) colored blue
        saturated vapor T(s) colored red
        The high and low isobars and lines connecting state 1 to 2, and 3 to saturated liquid at phigh
        step 1:  build data for saturated liquid line
        step 2:  build data for saturated vapor line
        step 3:  build data between state 3 and sat liquid at p_high
        step 4:  build data between sat liquid at p_high and state 1
        step 5:  build data between state 1 and state 2
        step 6:  build data between state 2 and state 3
        step 7:  put together data from 3,4,5 for top line and build bottom line
        step 8:  make and decorate plot

        Note:  will plot using pyplot if axObj is None else just returns

        :param axObj:  if None, used plt.subplot else a MatplotLib axes object.
        :return:
        """
        # step 1&2:
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1,
                                                          unpack=True)  # use np.loadtxt to read
        # the saturated properties
        ax = plt.subplot() if axObj is None else axObj
        # listing all entropies and temperatures calculated
        # these will be used in conversions if English units are required
        State1s, State2s, State3s, State4s = Model.state1.s, Model.state2.s, Model.state3.s, Model.state4.s
        State1t, State2t, State3t, State4t = Model.state1.T, Model.state2.T, Model.state3.T, Model.state4.T

        if SI is False:
            ts = UnitConverter.C_to_F(ts)
            ps = ts * UnitConverter.bar_to_psi
            hfs = ts * UnitConverter.kJperkg_to_BTUperlb
            hgs = hgs * UnitConverter.kJperkg_to_BTUperlb
            sfs = sfs * 0.00023884589663
            sgs = sgs * 0.00023884589663
            vfs = vfs * UnitConverter.m3perkg_to_ft3perlb
            vgs = vgs * UnitConverter.m3perkg_to_ft3perlb
            State1s = State1s * 0.00023884589663
            State2s = State2s * 0.00023884589663
            State3s = State3s * 0.00023884589663
            State4s = State4s * 0.00023884589663
            State1t = UnitConverter.C_to_F(State1t)
            State2t = UnitConverter.C_to_F(State2t)
            State3t = UnitConverter.C_to_F(State3t)
            State4t = UnitConverter.C_to_F(State4t)

        ax.plot(sfs, ts, color='blue')
        ax.plot(sgs, ts, color='red')
        ax.plot(sfs, ts, color='blue')
        ax.plot(sgs, ts, color='red')
        state3 = steam(Model.p_high, x=0)  # saturated liquid state at p_high
        stat3s = state3.s  # state3 entropy
        state3t = state3.T  # state3 Temp
        if SI is False:
            stat3s = stat3s * 0.00023884589663  # Convert entropy.
        svals = np.linspace(State3s, stat3s, 20)
        tvals = np.linspace(State3t, state3t, 20)
        line3 = np.column_stack([svals, tvals])

        # step 4:
        sat_pHigh = steam(Model.p_high, x=1.0)  # p high isobar
        Stat1 = Model.state1
        state1s = Stat1.s
        state1T = Stat1.T
        satpHighS = sat_pHigh.s
        satpHighT = sat_pHigh.T
        if SI is False:
            state1s = state1s * 0.00023884589663  # converting entropy
            state1T = UnitConverter.C_to_F(state1T)  # converting temp
            satpHighS = satpHighS * 0.00023884589663  # converting entropy
            satpHighT = UnitConverter.C_to_F(satpHighT)  # converting temp
        svals2p = np.linspace(stat3s, satpHighS, 20)
        tvals2p = [state3t for i in range(20)]
        line4 = np.column_stack([svals2p, tvals2p])

        # step 5:
        svals = np.linspace(State1s, State2s, 20)
        tvals = np.linspace(State1t, State2t, 20)
        line5 = np.array(svals)
        line5 = np.column_stack([line5, tvals])

        # step 6:
        svals = np.linspace(State2s, State3s, 20)
        tvals = np.array([State2t for i in range(20)])
        line6 = np.column_stack([svals, tvals])
        # step 7:
        highiso = np.append(line3, line4, axis=0)
        highiso = np.append(highiso, line5, axis=0)
        xvals = highiso[:, 0]
        y1 = highiso[:, 1]
        y2 = [State3t for l in xvals]
        ax.plot(xvals, y1, color='darkgreen')
        ax.plot(xvals, y2, color='black')
        ax.fill_between(xvals, y1, y2, color='gray', alpha=0.5)
        ax.plot(State1s, State1t, marker='o', markeredgecolor='k', markerfacecolor='w')
        ax.plot(State2s, State2t, marker='o', markeredgecolor='k', markerfacecolor='w')
        ax.plot(State3s, State3t, marker='o', markeredgecolor='k', markerfacecolor='w')
        #  Plot labels need to based on SI boolean. BD
        if SI is True:
            ax.set_xlabel(r's $\left(\frac{kJ}{kg\cdot K}\right)$', fontsize=16)
        if SI is False:
            ax.set_xlabel(r's $\left(\frac{BTU}{lb\cdot R}\right)$', fontsize=16)
        if SI is True:
            ax.set_ylabel(r'T $C$', fontsize=16)
        if SI is False:
            ax.set_ylabel(r'T $F$', fontsize=16)
        ax.set_title(Model.name)
        ax.grid(visible='both', alpha=0.5)
        ax.tick_params(axis='both', direction='in', labelsize=16)
        # using stems from  before here and boolean for text outputs

        sMin = min(sfs)
        sMax = max(sgs)
        ax.set_xlim(sMin, sMax)
        tMin = min(ts)
        tMax = max(max(ts), Stat1.T)
        ax.set_ylim(tMin, tMax * 1.05)
        # boolean for texts and formats, etc.
        if SI is True:
            txt = 'Summary:'
            txt += '\n$\eta_{cycle} = $' + '{:0.2f}%'.format(Model.efficiency)
            txt += '\n$\eta_{turbine} = $' + '{:0.2f}'.format(Model.turbine_eff)
            txt += '\n$W_{turbine} = $' + '{:0.2f}'.format(Model.turbine_work) + r'$\frac{kJ}{kg}$'
            txt += '\n$W_{pump} = $' + '{:0.2f}'.format(Model.pump_work) + r'$\frac{kJ}{kg}$'
            txt += '\n$Q_{in} = $' + '{:0.2f}'.format(Model.heat_added) + r'$\frac{kJ}{kg}$'
            ax.text(sMin + 0.05 * (sMax - sMin), tMax, txt, ha='left', va='top', fontsize=16)
        if SI is False:
            txt = 'Summary:'
            txt += '\n$\eta_{cycle} = $' + '{:0.2f}%'.format(Model.efficiency)
            txt += '\n$\eta_{turbine} = $' + '{:0.2f}'.format(Model.turbine_eff)
            txt += '\n$W_{turbine} = $' + '{:0.2f}'.format(
                Model.turbine_work * UnitConverter.kJperkg_to_BTUperlb) + r'$\frac{BTU}{lb}$'
            txt += '\n$W_{pump} = $' + '{:0.2f}'.format(
                Model.pump_work * UnitConverter.kJperkg_to_BTUperlb) + r'$\frac{BTU}{lb}$'
            txt += '\n$Q_{in} = $' + '{:0.2f}'.format(
                Model.heat_added * UnitConverter.kJperkg_to_BTUperlb) + r'$\frac{BTU}{lb}$'
            ax.text(sMin + 0.05 * (sMax - sMin), tMax, txt, ha='left', va='top', fontsize=16)

        if axObj is None:
            plt.show()


def main():
    RC = rankineController()
    RC.setRankine(8, 8000, t_high=500, eff_turbine=0.9, name='Rankine Cycle - Superheated at turbine inlet')
    # t_high is specified
    # if t_high were not specified, then x_high = 1 is assumed
    eff = RC.calc_efficiency()
    print(eff)
    RC.print_summary()
    RC.plot_cycle_TS()


if __name__ == "__main__":
    main()
