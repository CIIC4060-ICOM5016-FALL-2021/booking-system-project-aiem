import React, { Component, useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Grid, Modal, Tab } from "semantic-ui-react";
import BookMeeting from "./BookMeeting";
import Schedule from "./Schedule";
import Cookies from 'universal-cookie';
import Constants from './Constants'
import AccountManagement from './AccountManagement'

function UserView() {
    const [isAdmin, setIsAdmin] = useState(false)
    const [loggedInUser, setUser] = useState(undefined)
    const [LoggedInUserType, setUtype] = useState(undefined)

    const [userCatastrophicError, setUserCatastrophicError] = useState(false)

    if (loggedInUser === undefined) {
        var id = new Cookies().get("SessionID");
        fetch(Constants.ApiURL + "users/" + id)
            .then(response => {
                if (!response.ok) {
                    setUserCatastrophicError(true)
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) { 
                    setUser(data) 
                    return data.ut_id
                }
                return undefined
            }).then(ut_id => {
                if (ut_id===undefined) {return undefined}
                fetch(Constants.ApiURL + "users/user-types/" + ut_id).then(response => {
                    if (!response.ok) {
                        setUserCatastrophicError(true)
                        return undefined
                    }
                    return response.json()
                }).then(data => {
                    console.log(data)
                    if (data !== undefined) {
                        setUtype(data)
                        setIsAdmin(data.ut_isAdmin)
                    }
                })
            }
            )

    }

    const handleEmergencyLogout = (e) => {
        console.log("Ejecting!")
        new Cookies().remove("SessionID")
        window.location.reload()
        console.log("Oops we're really screwed now")
    }


    const adminPanes = [
        {
            menuItem: 'Booking', render: () => <BookMeeting />
        },
        {
            menuItem: 'Schedule', render: () => <Schedule />
        },
        {
            menuItem: 'Room Management', render: () => <BookMeeting /> //There is no room management component we still have to change this
        },
        {
            menuItem: 'Account Management', render: () => <AccountManagement User={loggedInUser} UserType={LoggedInUserType} />
        }
    ]

    const panes = [
        {
            menuItem: 'Booking', render: () => <BookMeeting />
        },
        {
            menuItem: 'Schedule', render: () => <Schedule />
        },
        {
            menuItem: 'Account Management', render: () => <AccountManagement User={loggedInUser} />
        }
    ]


    return <>
        <Modal
            centered={true}
            open={userCatastrophicError}
            onOpen={() => setUserCatastrophicError(true)}
            size="tiny"
            dimmer='blurring'
        >
            <Modal.Header>There has been a catastrophic error</Modal.Header>
            <Modal.Content>
                <Modal.Description>The session you have may no longer be valid, or there may have been a server side error. This may occur if your account has been deleted while you were logged in. Try refreshing this page. If that does not work, an <b>emergency log out button</b> is provided below</Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button color='red' onClick={handleEmergencyLogout}>EJECT</Button>
            </Modal.Actions>
        </Modal>
        <Tab panes={isAdmin ? adminPanes : panes} />
    </>

}

export default UserView;
