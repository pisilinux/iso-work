/*
 *   Copyright 2014 Marco Martin <mart@kde.org>
 *   Copyright 2018 Fabian Vogt <fabian@ritter-vogt.de>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License version 2,
 *   or (at your option) any later version, as published by the Free
 *   Software Foundation
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details
 *
 *   You should have received a copy of the GNU General Public
 *   License along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

import QtQuick 2.5
import QtGraphicalEffects 1.0

Image {
    id: root
    source: "images/Nar_Background.jpg"
    fillMode: Image.PreserveAspectCrop

    property int stage

    onStageChanged: {
        if (stage == 1) {
            introAnimation.running = true;
        }
        /*
        else if (stage == 5) {
            introAnimation.target = busyIndicator;
            introAnimation.from = 1;
            introAnimation.to = 0;
            introAnimation.running = true;
        } */
    }




    Image {
        id: topRect
        anchors.horizontalCenter: parent.horizontalCenter
        y: root.height
        source: "images/rectangle.svg"

        Rectangle {
            radius: 2
            color: "#98153d"
            anchors {
                bottom: parent.bottom
                bottomMargin: 3
                horizontalCenter: parent.horizontalCenter
            }
            height: 10
            width: height*50
            Rectangle {
                radius: 3
                anchors {
                    left: parent.left
                    top: parent.top
                    bottom: parent.bottom
                }
                width: (parent.width / 6) * (stage - 1)
                color: "#ffffff"
                Behavior on width {
                    PropertyAnimation {
                        duration: 240
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }
    }



    SequentialAnimation {
        id: introAnimation
        running: false

        ParallelAnimation {
            PropertyAnimation {
                property: "y"
                target: topRect
                to: root.height / 2
                duration: 1000
                easing.type: Easing.InOutBack
                easing.overshoot: 1.0
            }


        }
    }














        
}
