[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/e8a203b006c5460bb2295c25419d294c)](https://www.codacy.com/app/paulheider/YouDoneBro?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=paulheider/YouDoneBro&amp;utm_campaign=Badge_Grade)

You Done, Bro?
==============

Monitor gender and status biases in conversational turn-taking patterns.

Installation
------------

"You Done, Bro?" is still in beta.  If you'd like to help with beta-testing, email [me](mailto:paul.heider+youdonebro@gmail.com) with the address that you have associated with your Google Play account.  I'm still working on the iPhone build.  (If you have any experience building an iPhone app with Kivy and would like to help, definitely email me!)

Because Kivy is built on top of Python, you can also run "You Done, Bro?" as an application on your computer.  First, you'll need to [install Kivy](https://kivy.org/docs/installation/installation.html#stable-version).  Next, you'll need to download (or clone) the [latest release](https://github.com/paulheider/YouDoneBro/releases).  From the folder containing this release, run the following:

```
python main.py
```

Usage
-----

The main app screen provides four buttons for tracking conversational
turn length in terms of strict time and overall percentage of time.

The buttons are superficially split into a 2x2 grid.  High- vs.
low-status contributions can be compared by looking at total time
facilitators speak vs. non-facilitators.  Gendered contributions can be
compared by looking at total time bros vs. non-bros speak.

This 4-way division can be recast to other categories as your needs
require.

Tapping a main button starts or stops that particular category's timer.
If you start the timer for one category, all other categories' timers
will be stopped.

The 'Pause' button will stop all timers.

A long-press on the 'clear' button will clear all timers of any accrued
time.

The 'about' screen is only available when all timers are at zero.

If any timers have any time on them, the 'save' button is available.
It stops (pauses) all timers, updates the displayed calculations,
and save all timers to disk.  The pop-up tells you the new file's
name.  The 'save' button requires a long-press.

A count of group members is displayed near the outside edge of each
category.  You can adjust the tally for each group using the +/- buttons
beside the count.

For more information or to post bugs, issues, and recommendations,
please visit the app's GitHub pages:
- https://github.com/paulheider/YouDoneBro
- https://github.com/paulheider/YouDoneBro/issues


License
-------

See [LICENSE](LICENSE) file.

See Also
--------

- [Are men talking too much?](http://arementalkingtoomuch.com/)
- [WomanInterrupted](http://www.womaninterruptedapp.com/)
