###########################################################################
# This file is part of 'You Done, Bro?'.
#
# 'You Done, Bro?' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'You Done, Bro?' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'You Done, Bro?'.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

from __future__ import print_function

import time
import datetime

import os

import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

class StopWatch(EventDispatcher):
    __members = 0
    
    def get_member_count(self):
        return self.__members
    
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

    def dec(self):
        if( self.__members > 0 ):
            self.__members -= 1

    def inc(self):
        self.__members += 1

    def __init__(self):
        self.__offset = 0
        self.__start_time = 0
        self.__running = False
    
    def __repr__(self):
        hours, remainder = divmod( int( self.get_elapsed() ) , 3600 )
        minutes, seconds = divmod( remainder , 60 )
        return '{:02d}:{:02d}:{:02d} ({})'.format( hours , minutes , seconds ,
                                                   self.__members )

from kivy.clock import Clock
from functools import partial

class ScreenManagement( ScreenManager ):
    pass

class AboutScreen(Screen):
    __version__ = '17.49.2'
    
    def version( self , *args ):
        return self.__version__

class RootWidget(Screen): ##FloatLayout
    fac_bro_watch = ObjectProperty(None)
    fac_nd_watch = ObjectProperty(None)
    nf_bro_watch = ObjectProperty(None)
    nf_nd_watch = ObjectProperty(None)
    clear_event = ObjectProperty(None)
    save_event = ObjectProperty(None)

    ## TODO - clicking directly on popup also dismisses it
    save_popup = Popup( title = 'Saved Timings',
                        content = Label( text = '...somewhere...' ) ,
                        size_hint = ( 0.75 , 0.4 ) )
    
    def clear_time( self , *args ):
        self.ids[ 'about_save_btn' ].text = 'about'
        self.fac_bro_watch.reset()
        self.fac_nd_watch.reset()
        self.nf_bro_watch.reset()
        self.nf_nd_watch.reset()
        ## Clear the displayed times
        self.ids[ 'fac_bro_time' ].text = '{}'.format( self.fac_bro_watch )
        self.ids[ 'fac_nd_time' ].text = '{}'.format( self.fac_nd_watch )
        self.ids[ 'nf_bro_time' ].text = '{}'.format( self.nf_bro_watch )
        self.ids[ 'nf_nd_time' ].text = '{}'.format( self.nf_nd_watch )
        ## Clear the displayed percentages
        self.ids[ 'fac_bro_pct' ].text = '{:0.02f}%'.format( 0 )
        self.ids[ 'fac_nd_pct' ].text = '{:0.02f}%'.format( 0 )
        self.ids[ 'nf_bro_pct' ].text = '{:0.02f}%'.format( 0 )
        self.ids[ 'nf_nd_pct' ].text = '{:0.02f}%'.format( 0 )

    def save_to_disk( self , *args ):
        ## Stop all the watches
        self.fac_bro_watch.stop()
        self.fac_nd_watch.stop()
        self.nf_bro_watch.stop()
        self.nf_nd_watch.stop()
        ## Update the screen display
        self.update()
        ##
        now_time = datetime.datetime.now()
        now_stamp = now_time.strftime( "%Y-%m-%d %H:%M:%S" )
        now_filesafe = now_time.strftime( "%Y-%m-%d_%H%M%S" )
        filename = 'youdonebro_{}.csv'.format( now_filesafe )
        save_file = os.path.join( App.get_running_app().user_data_dir ,
                                  'data' ,
                                  filename )
        with open( save_file , 'w' ) as fp:
            fp.write( '{}\t{}\t{}\t{}\t{}\t{}\n'.format( 'Timestamp' ,
                                                         'Status' ,
                                                         'Gender' ,
                                                         'RawTime' ,
                                                         'PercentageTime' ,
                                                         'Members' ) )
            ##
            fp.write( '{}\t{}\t{}\t{}\t{}\t{}\n'.format( now_stamp ,
                                                         'facilitator' ,
                                                         'a bro' ,
                                                         self.ids[ 'fac_bro_time' ].text ,
                                                         self.ids[ 'fac_bro_pct' ].text ,
                                                         self.fac_bro_watch.get_member_count() ) )
            #
            fp.write( '{}\t{}\t{}\t{}\t{}\t{}\n'.format( now_stamp ,
                                                         'facilitator' ,
                                                         'not a bro' ,
                                                         self.ids[ 'fac_nd_time' ].text ,
                                                         self.ids[ 'fac_nd_pct' ].text ,
                                                         self.fac_nd_watch.get_member_count() ) )
            #
            fp.write( '{}\t{}\t{}\t{}\t{}\t{}\n'.format( now_stamp ,
                                                         'non-facilitator' ,
                                                         'a bro' ,
                                                         self.ids[ 'nf_bro_time' ].text ,
                                                         self.ids[ 'nf_bro_pct' ].text ,
                                                         self.nf_bro_watch.get_member_count() ) )
            #
            fp.write( '{}\t{}\t{}\t{}\t{}\t{}\n'.format( now_stamp ,
                                                         'non-facilitator' ,
                                                         'not a bro' ,
                                                         self.ids[ 'nf_nd_time' ].text ,
                                                         self.ids[ 'nf_nd_pct' ].text ,
                                                         self.nf_nd_watch.get_member_count() ) )
        self.save_popup.content.text = filename
        self.save_popup.open()
    
    def press(self, button):
        if( button == 'clear' ):
            self.clear_event = partial( self.clear_time )
            Clock.schedule_once( self.clear_event , 2 )
        elif( button == 'about' ):
            screen_mngr.transition.direction = 'down'
            screen_mngr.current = 'About'
        elif( button == 'save' ):
            self.save_event = partial( self.save_to_disk )
            Clock.schedule_once( self.save_event , 2 )
            
    def release(self, button):
        if( button == 'clear' ):
            Clock.unschedule( self.clear_event )
            self.clear_event = ObjectProperty(None)
        elif( button == 'save' ):
            Clock.unschedule( self.save_to_disk )
            self.save_event = ObjectProperty(None)

    def tap(self, button):
        self.ids[ 'about_save_btn' ].text = 'save'
        if( button == 'pause' ):
            self.fac_bro_watch.stop()
            self.fac_nd_watch.stop()
            self.nf_bro_watch.stop()
            self.nf_nd_watch.stop()
        elif( button == 'dec_fac_bro' ):
            self.fac_bro_watch.dec()
        elif( button == 'inc_fac_bro' ):
            self.fac_bro_watch.inc()
        elif( button == 'fac_bro' ):
            if( self.fac_bro_watch.get_running() ):
                self.fac_bro_watch.stop()
            else:
                self.fac_bro_watch.start()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.stop()
        elif( button == 'dec_fac_nd' ):
            self.fac_nd_watch.dec()
        elif( button == 'inc_fac_nd' ):
            self.fac_nd_watch.inc()
        elif( button == 'fac_nd' ):
            if( self.fac_nd_watch.get_running() ):
                self.fac_nd_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.start()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.stop()
        elif( button == 'dec_nf_bro' ):
            self.nf_bro_watch.dec()
        elif( button == 'inc_nf_bro' ):
            self.nf_bro_watch.inc()
        elif( button == 'nf_bro' ):
            if( self.nf_bro_watch.get_running() ):
                self.nf_bro_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.start()
                self.nf_nd_watch.stop()
        elif( button == 'dec_nf_nd' ):
            self.nf_nd_watch.dec()
        elif( button == 'inc_nf_nd' ):
            self.nf_nd_watch.inc()
        elif( button == 'nf_nd' ):
            if( self.nf_nd_watch.get_running() ):
                self.nf_nd_watch.stop()
            else:
                self.fac_bro_watch.stop()
                self.fac_nd_watch.stop()
                self.nf_bro_watch.stop()
                self.nf_nd_watch.start()
        
    def update( self, *args ):
        self.ids[ 'fac_bro_time' ].text = '{}'.format( self.fac_bro_watch )
        self.ids[ 'fac_nd_time' ].text = '{}'.format( self.fac_nd_watch )
        self.ids[ 'nf_bro_time' ].text = '{}'.format( self.nf_bro_watch )
        self.ids[ 'nf_nd_time' ].text = '{}'.format( self.nf_nd_watch )
        total_time = self.fac_bro_watch.get_elapsed() + \
                     self.fac_nd_watch.get_elapsed() + \
                     self.nf_bro_watch.get_elapsed() + \
                     self.nf_nd_watch.get_elapsed()
        if( total_time > 0 ):
            self.ids[ 'fac_bro_pct' ].text = '{:0.02f}%'.format( 100 * self.fac_bro_watch.get_elapsed() / total_time )
            self.ids[ 'fac_nd_pct' ].text = '{:0.02f}%'.format( 100 * self.fac_nd_watch.get_elapsed() / total_time )
            self.ids[ 'nf_bro_pct' ].text = '{:0.02f}%'.format( 100 * self.nf_bro_watch.get_elapsed() / total_time )
            self.ids[ 'nf_nd_pct' ].text = '{:0.02f}%'.format( 100 * self.nf_nd_watch.get_elapsed() / total_time )
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.fac_bro_watch = StopWatch()
        self.fac_nd_watch = StopWatch()
        self.nf_bro_watch = StopWatch()
        self.nf_nd_watch = StopWatch()
        Clock.schedule_interval( self.update , 1 )

screen_mngr = Builder.load_file( "main.kv" )
about_screen = AboutScreen( name = 'About' )
screen_mngr.add_widget( about_screen )
screen_mngr.add_widget( RootWidget( name = 'Four-Way Tracker' ) )

class YouDoneBroApp(App):
    def build(self):
        self.initilize_global_dirs()
        return screen_mngr
    
    def initilize_global_dirs(self):
        data_dir = os.path.join( App.get_running_app().user_data_dir , 'data' )
        if( not os.path.exists( data_dir ) ):
            os.makedirs( data_dir )

if __name__ == '__main__':
    YouDoneBroApp().run()
