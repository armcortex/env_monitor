# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
# import webrepl_setup
import webrepl
import network

# AP will start by default
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

webrepl.start(password='12345678')
gc.collect()

