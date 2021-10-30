# MoonPlotter
A small app which scrapes a persons logbook data from the moonboard website and provides some interesting graphs.


**Setup for development :**
Install 'geckodriver' (driver for firefox) 

Using the aur (which threw a bunch of 404s for me):
`yay -S aur/geckodriver-hg`

Using pip:
`pip install get-gecko-driver`

If necessary install 'Selenium' (for scraping).
`pip install selenium`

And also 'kivy' (for UI).
`pip install kivy`

Install 'matplotlib' (for plotting the data).
`pip install "matplotlib<3.3.0"`
and
`garden install matplotlib`

**Building for production :**

Install 'buildozer' for building the app for android.
`pip install buildozer`

Build with
`buildozer android release`
The .apk is then placed in the created bin folder.
First builds take some time because buildozer installs a bunch of tools.

The config file is located in `./buildozer/buildozer.spec`.

**Problems :**
I ran into a problem with the build process on Manjaro Linux.
The error occured on executing `gradlew assembleRelease` (it's executed in a subfolder so the actual command may be much longer).

The answer was found here : 
https://stackoverflow.com/questions/67079327/how-to-fix-unsupported-class-file-major-version-60-in-intellij

And it was to install and use openjdk 11 as follows.

```
yay -S jdk11-openjdk
sudo archlinux-java set java-11-openjdk   
```

which one you're currently using may be checked with 
`archlinux-java status`

**Options for starting MoonPlotter.py :**

| description                     | usage                                  |
|---------------------------------|----------------------------------------|
| username of a moonboard account | -u <username> or --username <username> |
| password to the username        | -p <password> or --password <password> |
| whether to (user) cache data    | -c or --cache                          |
| debug mode shows the browser    | -d or --debug                          |
