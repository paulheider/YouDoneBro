from __future__ import print_function

import time
import datetime

import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

class StopWatch(EventDispatcher):
    
    def get_running(self):
        return self.__start_time != 0
    
    def get_elapsed(self):
        if( self.__running ):
            return self.__offset + ( time.time() - self.__start_time )
        
        return self.__offset
    
    def start(self):
        """Starts the stopwatch."""
        
        self.__start_time = time.time()
        self.__running = True
    
    def stop(self):
        """Stops the stopwatch and returns the elapsed time."""

        if( self.__running ):
            self.__offset += time.time() - self.__start_time
            self.__start_time = 0
            self.__running = False
        return self.get_elapsed()
    
    def reset(self):
        """Clears any accrued time on the stopwatch."""

        self.__offset = 0
        self.__start_time = 0
        self.__running = False
    
    def __init__(self):
        self.__offset = 0
        self.__start_time = 0
        self.__running = False
    
    
    def __repr__(self):
        hours, remainder = divmod( int( self.get_elapsed() ) , 3600 )
        minutes, seconds = divmod( remainder , 60 )
        return '{:02d}:{:02d}:{:02d}'.format( hours , minutes , seconds )

from kivy.clock import Clock
from functools import partial

class RootWidget(FloatLayout):
    fac_bro_watch = ObjectProperty(None)
    fac_nd_watch = ObjectProperty(None)
    nf_bro_watch = ObjectProperty(None)
    nf_nd_watch = ObjectProperty(None)
    clear_event = ObjectProperty(None)
    
    def clear_time( self , *args ):
        self.fac_bro_watch.reset()
        self.fac_nd_watch.reset()
        self.nf_bro_watch.reset()
        self.nf_nd_watch.reset()
        ## Clear the displayed times
        four_way_timers.ids[ 'fac_bro_time' ].text = '{}'.format( self.fac_bro_watch )
        four_way_timers.ids[ 'fac_nd_time' ].text = '{}'.format( self.fac_nd_watch )
        four_way_timers.ids[ 'nf_bro_time' ].text = '{}'.format( self.nf_bro_watch )
        four_way_timers.ids[ 'nf_nd_time' ].text = '{}'.format( self.nf_nd_watch )
        ## Clear the displayed percentages
        four_way_timers.ids[ 'fac_bro_pct' ].text = '{:0.02f}%'.format( 0 )
        four_way_timers.ids[ 'fac_nd_pct' ].text = '{:0.02f}%'.format( 0 )
        four_way_timers.ids[ 'nf_bro_pct' ].text = '{:0.02f}%'.format( 0 )
        four_way_timers.ids[ 'nf_nd_pct' ].text = '{:0.02f}%'.format( 0 )
    
    def press(self, button):
        if( button == 'clear' ):
            self.clear_event = partial( self.clear_time )
            Clock.schedule_once( self.clear_event , 2 )
            
    def release(self, button):
        if( button == 'clear' ):
            Clock.unschedule( self.clear_event )
            self.clear_event = ObjectProperty(None)

    def tap(self, button):
        if( button == 'pause' ):
            self.fac_bro_watch.stop()
            self.fac_nd_watch.stop()
            self.nf_bro_watch.stop()
            self.nf_nd_watch.stop()
        elif( button == 'fac_bro' ):
            if( self.fac_bro_watch.get_running() ):
                self.fac_bro_watch.stop()
            else:
                self.fac_bro_watch.start()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.stop()
        elif( button == 'fac_nd' ):
            if( self.fac_nd_watch.get_running() ):
                self.fac_nd_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.start()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.stop()
        elif( button == 'nf_bro' ):
            if( self.nf_bro_watch.get_running() ):
                self.nf_bro_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.start()
                self.nf_nd_watch.stop()
        elif( button == 'nf_nd' ):
            if( self.nf_nd_watch.get_running() ):
                self.nf_nd_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.start()
        
    def update( self, *args ):
        four_way_timers.ids[ 'fac_bro_time' ].text = '{}'.format( self.fac_bro_watch )
        four_way_timers.ids[ 'fac_nd_time' ].text = '{}'.format( self.fac_nd_watch )
        four_way_timers.ids[ 'nf_bro_time' ].text = '{}'.format( self.nf_bro_watch )
        four_way_timers.ids[ 'nf_nd_time' ].text = '{}'.format( self.nf_nd_watch )
        total_time = self.fac_bro_watch.get_elapsed() + \
                     self.fac_nd_watch.get_elapsed() + \
                     self.nf_bro_watch.get_elapsed() + \
                     self.nf_nd_watch.get_elapsed()
        if( total_time > 0 ):
            four_way_timers.ids[ 'fac_bro_pct' ].text = '{:0.02f}%'.format( 100 * self.fac_bro_watch.get_elapsed() / total_time )
            four_way_timers.ids[ 'fac_nd_pct' ].text = '{:0.02f}%'.format( 100 * self.fac_nd_watch.get_elapsed() / total_time )
            four_way_timers.ids[ 'nf_bro_pct' ].text = '{:0.02f}%'.format( 100 * self.nf_bro_watch.get_elapsed() / total_time )
            four_way_timers.ids[ 'nf_nd_pct' ].text = '{:0.02f}%'.format( 100 * self.nf_nd_watch.get_elapsed() / total_time )
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.fac_bro_watch = StopWatch()
        self.fac_nd_watch = StopWatch()
        self.nf_bro_watch = StopWatch()
        self.nf_nd_watch = StopWatch()
        Clock.schedule_interval( self.update , 1 )

four_way_timers = Builder.load_file( "main.kv" )

class YouDoneBroApp(App):
    
    def build(self):
        return four_way_timers

if __name__ == '__main__':
    YouDoneBroApp().run()
