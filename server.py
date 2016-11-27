from flask import Flask, request, abort, jsonify
from requests import get, post
from functools import wraps
import yaml

app = Flask(__name__)

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

DEBUG = False
HA_HOST = cfg["ha_host"]
HA_PASSWORD = cfg["ha_password"]
HA_STATE = cfg["ha_state"]
HOST_IP = cfg.get("host_ip", "0.0.0.0")
HOST_PORT = cfg.get("ha_port", 8124)

HA_STATE_URL = "%s/api/states/%s" % (HA_HOST, HA_STATE)
AUTH_HEADER = "X-HA-Access"


def get_status():
  headers = {
    'x-ha-access': HA_PASSWORD,
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
  
  return jsonify({
    "targetTemperature": target,
    "temperature": temp
  })

@app.route("/targettemperature/<target_temp>")
def set_temp(target_temp):
  headers = {
    'x-ha-access': HA_PASSWORD,
    'Content-Type': "application/json"
  }
  status = get_status().json()
  status["attributes"]["temperature"] = target_temp 
  print(status)
  response = post(HA_STATE_URL, headers=headers, json=status)
  if response.status_code != 200:
    abort(response.status_code, response.text)

  return (jsonify(response.json()), response.status_code)

if __name__ == "__main__":
  app.run(host=HOST_IP, port=HOST_PORT, debug=DEBUG)
