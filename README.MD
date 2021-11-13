# Gneelight
A Yeelight controller for GNOME

Written in Python and GTK+ 3 using the [Yeelight Python](https://github.com/skorokithakis/python-yeelight) library.

## Installation

### Install using Flatpak (recommended)
The simplest way to install Gneelight is by using the provided Flatpak package:
```bash
wget https://github.com/vinsce/gneelight/blob/master/flatpak/gneelight.flatpak?raw=true -O gneelight.flatpak
flatpak install --user gneelight.flatpak
```

#### Troubleshooting
If you receive the following error `The application me.vinsce.Gneelight/x86_64/master requires the runtime org.gnome.Platform/x86_64/3.38 which was not found` while installing, make sure you have the Flathub repository and the Gnome runtime installed:
```bash
flatpak --user remote-add --from flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak --user install flathub org.gnome.Platform//3.38
```

### Install from source
If you want to install from the source code, first make sure you have the following dependencies installed:
- `AppIndicator3` Library
- `yeelight` python package

In Ubuntu, you can install the dependencies using:
```
sudo apt-get install gir1.2-appindicator3-0.1
pip install yeelight
```

then clone this repository and start using Gneelignt:
```bash
git clone https://github.com/vinsce/gneelight.git
cd gneelight
sudo cp res/me.vinsce.Gneelight.gschema.xml /usr/share/glib-2.0/schemas/
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

python3 src/GneelightApp.py
```

## Screenshot
<img width="345" height="327" align="middle" src="https://i.imgur.com/VA4kaCV.png" alt="screenshot">

##
Note: feel free to contribute to the project and suggest new features.

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details
