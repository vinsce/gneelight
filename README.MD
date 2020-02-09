# Gneelight
A Yeelight controller for GNOME

Written in Python and GTK+ 3 using the [Yeelight Python](https://github.com/skorokithakis/python-yeelight) library.

## Installation
You can install Gneelight using the provided Flatpak package:
```bash
wget https://github.com/vinsce/gneelight/blob/master/flatpak/gneelight.flatpak?raw=true -O gneelight.flatpak
flatpak install --user gneelight.flatpak
```
Alternatively download the entire source and run
```bash
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
