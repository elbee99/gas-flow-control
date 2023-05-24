from alicat import FlowController

flow_controller_O2 = FlowController(port='COM3')
flow_controller_Ar = FlowController(port='COM5')

print(flow_controller_O2.get())
print(flow_controller_Ar.get())

flow_controller_O2.set_gas('O2')
flow_controller_Ar.set_gas('Ar')

flow_controller_O2.set_flow_rate(0)
flow_controller_Ar.set_flow_rate(0)