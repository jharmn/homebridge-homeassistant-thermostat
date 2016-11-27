from __future__ import unicode_literals
from flask import Flask, request, abort, jsonify
from requests import get, post
from functools import wraps
import argparse, sys, getopt, yaml
from future.utils import raise_from

DEBUG = False

app = Flask(__name__)

# Process arguments
parser = argparse.ArgumentParser(description="Start thermostat server for Home Assistant.")
parser.add_argument("-c", "--config", default="config.yaml", dest="config", metavar="CONFIG_FILE.YAML", help="Optional config file")
args = parser.parse_args()

# Open config yaml
class ConfigFile:
  def __init__(self, filename):
    try:
      self.file = open(filename)
    except IOError as exc:
      print("An error occurred loading the config: ", exc) 
      sys.exit(0)

cfg = ""
try:
  ymlfile = ConfigFile(args.config).file
  cfg = yaml.load(ymlfile)
except Exception as e:
    assert isinstance(e.__cause__, IOError)

# Required
HA_HOST = cfg.get("ha_host")
HA_PASSWORD = cfg.get("ha_password")
HA_STATE = cfg.get("ha_state")
# Optional
HOST_IP = cfg.get("host_ip", "0.0.0.0")
HOST_PORT = cfg.get("ha_port", 8124)

HA_STATE_URL = "%s/api/states/%s" % (HA_HOST, HA_STATE)
HA_SET_URL = "%s/api/services/climate/set_temperature" % (HA_HOST)
AUTH_HEADER = "X-HA-Access"


def get_status():
  headers = {
    "x-ha-access": HA_PASSWORD,
  }
  upstream_response = get(HA_STATE_URL, headers=headers)
  if upstream_response.status_code != 200:
    abort(upstream_response.status_code)
  return upstream_response


@app.route("/status")
def status():
  response = get_status().json()
  attr = response.get("attributes")
  target = attr.get("temperature")
  temp = attr.get("current_temperature")
  unit = attr.get("unit_of_measurement")
  if unit == u"\xc2C":
    unit = 0
  else:
    unit = 1
  
  return jsonify({
    "targetTemperature": target,
    "temperature": temp,
    "targetState":"HEAT",
    "targetStateCode":1,
    "currentHeatingCoolingState":1,
    "humidity":0,
    "temperatureDisplayUnits": 0
  })

@app.route("/targetTemperature/<target_temp>")
def set_temp(target_temp):
  headers = {
    "x-ha-access": HA_PASSWORD,
    "Content-Type": "application/json"
  }
  status = {
    "entity_id": HA_STATE,
    "temperature": target_temp
  }
  response = post(HA_SET_URL, headers=headers, json=status)
  if response.status_code != 200:
    abort(response.status_code, response.text)

  return (jsonify(response.json()), response.status_code)

if __name__ == "__main__":
  app.run(host=HOST_IP, port=HOST_PORT, debug=DEBUG)
