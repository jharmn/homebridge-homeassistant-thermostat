# homebridge-homeassistant-thermostat

Provides compatibility for [Home Assistant's generic thermostat](https://home-assistant.io/components/climate.generic_thermostat/) with [homebridge-thermostat](https://github.com/PJCzx/homebridge-thermostat).

This is a bridge of a bridge, proxying [Home Assistant REST API](https://home-assistant.io/developers/rest_api/) for generic thermostat, a climate component. Useful if you are using a generic thermostat with [homebridge-homeassistant](https://github.com/home-assistant/homebridge-homeassistant). In short, set this up, and you can set the thermostat temperature with Siri.

DOES NOT support humidity, as generic thermostat doesn't provide it.

Works with Python 2 or 3.

## Get it running

First, the usual Python/virtualenv stuff:

``` bash
virtualenv env
. env/bin/activate
```

Then, setup a configuration file. Copy the provided `config-sample.yaml` to `config.yaml`, and adjust for your needs.

* `host_ip` (optional): defaults to `0.0.0.0` (i.e. any IP bound to the machine)
* `host_port` (optional): defaults to `8124`
* `ha_host`: the IP/hostname of your Home Assistant server
* `ha_password`: the password for your Home Assistant server
* `ha_state`: the state variable of your thermostat (should be `climate.something`)


Then run the server:

``` bash
python server.py
```

You can also specify a config file with `-c` or `--config`

``` bash
python server.py -c my_config.yaml
```

## Try it out

### Get status
``` bash
curl "http://localhost:8124/status"
```

### Set target temp
``` bash
curl "http://localhost:8124/targettemperature/22"
```
