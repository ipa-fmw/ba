#!/usr/bin/env python
import roslib, math
roslib.load_manifest( 'navigation_test' )
import rospy, rostopic
import os, logging, sys
import cob_srvs.srv, time
import unittest, rostest
import std_srvs, std_srvs.srv
from navigationStatusPublisher           import NavigationStatusPublisher
from navigation_helper.positionResolver  import PositionResolver
from navigation_helper.metricsObserverTF import MetricsObserverTF
from navigation_helper.tolerance         import Tolerance
from navigation_helper.position          import Position
from navigation_helper.navigator         import Navigator
from navigation_helper.jsonFileHandler   import JsonFileHandler

class TestNavigation( unittest.TestCase ):
    def setUp( self ):

        rospy.loginfo( 'Setting navigator' )
        self.navigator = Navigator( '/move_base' )
        self._metricsObserver = MetricsObserverTF()

        setting = self._getSetting()
        self._navigationStatusPublisher = NavigationStatusPublisher( '~status',
                setting )

        self.tolerance = Tolerance( xy=0.2, theta=.3 )
        self.positionResolver = PositionResolver()
        path = os.path.dirname(os.path.abspath(__file__))
        self.testResultWriter = JsonFileHandler( path + '/metrics.json' )

        rospy.loginfo( 'Waiting for Bag Recorder' )
        self._stopBagRecording = self._waitForBagRecorder()

    def _getSetting( self ):
        return {
            'scenario':   rospy.get_param( '/navigation_test_route/name' ),
            'robot':      rospy.get_param( '~robot' ),
            'navigation': rospy.get_param( '~navigation' )
        }

    def _waitForBagRecorder( self ):
        rospy.wait_for_service( '/logger/stop' )

        stopBagRecordingService  = rospy.ServiceProxy( '/logger/stop',  
                cob_srvs.srv.Trigger )
        rospy.loginfo( 'Logger ready' )
        return stopBagRecordingService


    def testNavigate( self ):
        goals = rospy.get_param( '/navigation_test_route/goals' )
        self._metricsObserver.start()

        i = 0
        for goal in goals:
            self._navigationStatusPublisher.nextWaypoint( goal )
            targetPosition = Position( *goal )

            self.navigator.goTo( targetPosition ) 
            self.navigator.waitForResult( timeout=300.0 )

            errorMsg = 'Position: %s does not match goal %s' % ( 
                    self.positionResolver.getPosition(), goal )
            self.assertTrue( self.positionResolver.inPosition( targetPosition, 
                    self.tolerance ), errorMsg )

            i += 1

        self._navigationStatusPublisher.finished()
        self._metricsObserver.stop()
        self.testResultWriter.write( self._metricsObserver.serialize() )
        
        self._stopBagRecording()
        time.sleep( 2 )

        rospy.signal_shutdown( 'finished' )
        time.sleep( 4 )


if __name__ == '__main__':
    rospy.init_node( 'navigation_test', anonymous=True)
    rostest.rosrun( 'navgation_test', 'test_navigation',
        TestNavigation, sys.argv)
