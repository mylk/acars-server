# acars-server

A python3 implementation of an ACARS server, storing and displaying ACARS messages.

## Demo

This is a real deployment of the application, displaying reatime data as received by my station at home (Palaio Falioro, Athens, Greece).

[TBD](#)

The setup is, an `acars-server` "client" running on my home computer (may not be always online) connected with the required equipment (described below) that decodes the ACARS messages and sends them to a remote `acars-server` "listener" that parses and stores them in order to be displayed on the web interface.

## What is ACARS

[Source](https://en.wikipedia.org/wiki/ACARS)

In aviation, ACARS (Aircraft Communications Addressing and Reporting System) is the transmission system of short messages between aircrafts and ground stations via radio (VHF or HF), directly or via sattelite.

ACARS messages are transmited on [specific frequencies](https://www.acarsd.org/ACARS_frequencies.html) based the ground station and aircraft locations.

### ACARS messages

Messages may be about air traffic control in order to request or provide clearances, OOOI events (are described below), flight plans, status of connecting flights, weather information, equipment health (faults and abnormal events). This gives an importart role to ACARS on air incidents and accidents.

A major function of ACARS is to detect and report major flight phases, called OOOI events (Out of the gate, Off the ground, On the ground, and Into the gate) using input from aircraft sensors mounted on doors, parking brakes and struts. Such ACARS messages describe the flight phase, the time it occurred and other related information such as the amount of fuel on board or the flight origin and destination.

Ping messages can also be sent through ACARS. If an aircraft has been silent for longer than a preset time interval, the ground station can ping the aircraft. A ping response indicates a healthy ACARS communication.

Manual messages can also be sent. ACARS interfaces with interactive display units in the cockpit, which flight crews can use to send and receive technical messages and reports, such as weather information, clearances or the status of connecting flights.

Messages can also be about airline administrative control, for communication between aircrafts with their airline.

ACARS messages are either standardized according to the ARINC Standard 633, or user-defined in accordance with the ARINC Standard 618.

Hear an [example of an ACARS message](https://en.wikipedia.org/wiki/File:Acars_sample.ogg). 

## Application components

This project consists of three application components:

- client  
uses `acarsdec` to decode ACARS messages and send them to the listener component.
  
- listener  
receives messages from the ACARS client, parses them to usable information and stores it to the databse.
  
- web interface  
produces a web interface to display the ACARS messages and other related information.

## Equipment

If you wish to receive ACARS messages, there is required equipment, as they are transfered via radio. I use the [RTL-SDR](https://www.amazon.com/RTL-SDR-Blog-RTL2832U-Software-Defined/dp/B011HVUEME) which is [SDR (Software Defined Radio) equipment](https://en.wikipedia.org/wiki/Software-defined_radio). SDR is a software radio communication component which traditionally was implemented by multiple hardware components (amplifiers, modulators / demodulators, detectors, etc.).

## Usage

### Prerequesites

(acardec)[https://github.com/TLeconte/acarsdec] is required to be installed, if you wish to receive ACARS messages, as well as the required equipment described above. Python3 is also required to run this application.

### Installing

Clone this repository:

```
git clone https://github.com/mylk/acars-server
```

Check if your system has the required system dependencies (acarsdec installed).

```
make sys_deps
```

Install python package dependencies:

```
make deps
```

Create the database:

```
make db_migrate
```

### Running

If you own the required equipment, you can run the client yourself:

```
ENV=production make client
```

The client assumes that a local instance of `acars-server` run and send the messages there. In case that the listener component is installed on a remote machine, edit the file `acars-server/acarsserver/config/environments/production.py` and change `listener_host` and `listener_port` settings to the values that fit your needs.

By default, the client scans the European ACARS radio frequencies. In case you want to change them, please advice [this document](https://www.acarsd.org/ACARS_frequencies.html) for the appropriate frequencies of your location and then change them in `acars-server/acarsserver/config/settings.py`.

Run the listener to receive the messages from the client:

```
ENV=production make listener
```

Run the web interface:

```
ENV=production make web
```

Note that, currently, the web interface has to be hosted along with the listener component, as they share a local embeded database.


## Contributing

`acars-server` is open source and of course you can contribute. Just fork the project, have fun and then create a pull request.

But first, you need to install the development dependencies:

```
make deps_dev
```

You don't need an SDR for development. You can simulate the client component by running the `fake client` which will send fake ACARS messages to the listener component:

```
ENV=development make client_fake
```

## Built with

- [acarsdec](https://github.com/TLeconte/acarsdec) - The utility that decodes the ACARS messages and sends them to the `acars-server`.
- [bottle](https://bottlepy.org/docs/dev/) - The python web framework used to create the web component.


## Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available, see the [tags](https://github.com/mylk/acars-server/tags).

## Authors

See the list of [contributors](https://github.com/mylk/acars-server/contributors).

## License

This project is licensed under the GPLv2 License - see the [LICENSE](https://github.com/mylk/acars-server/blob/master/LICENSE) file for details.
