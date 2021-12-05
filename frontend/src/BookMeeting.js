import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Divider, Form, Grid, Header, Modal, Placeholder, Segment} from "semantic-ui-react";
import Constants from './Constants'

// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting(props){
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [User, Setuser] = useState(undefined)
    const localizer = momentLocalizer(moment)

       const [registerRequest, setRegisterRequest] = useState({
        "mt_name": "",
        "mt_desc": "",
        "re_date": "",
        "re_startTime": "",
        "re_endTime": "",
        "ro_id": "",
        "attendees": "",
    })
    const [loginInProgress, setLoginInProgress] = useState(false)
    const [MeetingError, setMeetingError] = useState(false)

    const [registrationInProgress, setRegistrationInProgress] = useState(false)
    const [registrationError, setRegistrationError] = useState(false)
    const [registrationErrorText, setRegistrationErrorText] = useState("Help! I don't know what happened!")

    const [regMtNameError, setMTNameError] = useState(false)
    const [regMtDescError, setMtDescError] = useState(false)
    const [regDateError, setDateError] = useState(false)
    const [regStTimeError, setStTimeError] = useState(false)
    const [regEndTimeError, setEndTimeError] = useState(false)
    const [regRoIdError, setRegRoIdError] = useState(false)
    const [regAttendeesError, setAttendeesError] = useState(false)

    const [Checkbox, setCheckbox]= useState(false)

    const [regSuccessOpen, setRegSuccessOpen] = useState(false)

    const createMeeting = (e) => {
        console.log(registerRequest)
        setRegistrationInProgress(true)
        setRegistrationError(false)

  class ButtonExampleToggle extends Component {
    state = {}
    handleClick = () =>
    this.setState((prevState) => ({ active: !prevState.active }))

    render() {
    const { active } = this.state

        return (
        <Button toggle active={active} onClick={this.handleClick}>
            Toggle
        </Button>
        )
    }
  }

        //Validation

        if (registerRequest.mt_name === "") {
            setMTNameError("Please input a meetings name")
        } else {
            setMTNameError(false)
        }
         if (registerRequest.mt_desc === "") {
            setMtDescError("Please input a meetings description")
        } else {
            setMtDescError(false)
        }
        if (registerRequest.re_date === "") {
            setDateError("Please specify date of the meeting")
        } else {
            setDateError(false)
        }
        if (registerRequest.re_startTime === "") {
            setStTimeError("Please specify starting time")
        } else {
            setStTimeError(false)
        }
        if (registerRequest.re_endTime === "") {
            setEndTimeError("Please specify end time")
        } else {
            setEndTimeError(false)
        }
        if (registerRequest.ro_id === "") {
            setRegRoIdError("Please specify Room")
        } else {
            setRegRoIdError(false)
        }
            if (registerRequest.attendees === "") {
            setAttendeesError("Please specify attendees")
        } else {
            setAttendeesError(false)
        }

        if (registerRequest.mt_name === "" ||
            registerRequest.mt_desc === "" ||
            registerRequest.re_date === "" ||
            registerRequest.re_startTime === "" ||
            registerRequest.re_endTime === "" ||
            registerRequest.ro_id === "" ||
            registerRequest.attendees === "") {
            setRegistrationInProgress(false)
            return;
        }

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(registerRequest)
        };

        fetch(Constants.ApiURL + "meetings", requestOptions)
            .then(response => {
                setRegistrationInProgress(false);
                if (response.status === 500) {
                    setRegistrationError(true)
                    setRegistrationErrorText("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    setMTNameError("Meeting already exists!")
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data === undefined) {
                return
            }
            if (data.mt_id === null) {
                setMTNameError("Meeting already exists!")
                return undefined
            }
            setOpen(false)
            setRegSuccessOpen(true)
        })
    }


    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelecting = {(selected) =>{ setDates([{
                        'title': 'Selection',
                        'allDay': false,
                        'start': new Date(selected.start),
                        'end': new Date(selected.end)
                    }] ) } }
    >

    </Calendar>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>Create a Meeting </Modal.Header>
                <Modal.Content>
                    <Form>
                        {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                        <Form.Input
                            label='Meeting Name' placeholder='Meeting Name' required
                            error={registrationError ? registrationError : regMtNameError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "mt_name": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting Description' placeholder='Description' required
                            error={registrationError ? registrationError : regMtDescError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "mt_desc": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting Date' placeholder='year:month:date' required
                            error={registrationError ? registrationError : regDateError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "re_date": e.target.value }) }}
                        />

                        <button className="ui toggle button"
                                aria-pressed="false">All Day</button>

                        <Form.Input
                            label='Meeting Start Time' placeholder='Starttime: HH:MM:SS' required
                            error={registrationError ? registrationError : regStTimeError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "re_starttime": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting End Time' placeholder='Endtime: HH:MM:SS' required
                            error={registrationError ? registrationError : regEndTimeError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "re_endtime": e.target.value }) }}
                        />
                        <Form.Input
                            label='Room Id' type='Room' required
                            error={registrationError ? registrationError : regRoIdError}
                            disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "ro_id": e.target.value }) }}
                        />

                        {
                            // utypes === undefined ?
                            //     <Placeholder>
                            //         <Placeholder.Line />
                            //     </Placeholder> :
                            //     <Form.Dropdown
                            //         label="User Type" placeholder='' required
                            //         search selection options={utypes} disabled={registrationInProgress}
                            //         error={registrationError ? registrationError : regUtIdError}
                            //         onChange={(event, data) => {
                            //             setRegisterRequest({ ...registerRequest, "ut_id": data.value })
                            //             console.log(data.value)
                            //         }}
                            //     />

                        }
                        <Form.Input
                            label='Attendees' type='Attendees' required
                            error={registrationError ? registrationError : regAttendeesError}
                            disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "attendees": e.target.value }) }}
                        />

                        <Segment basic textAlign={"center"}>
                            <Button loading={registrationInProgress} content='Register' primary onClick={createMeeting} />
                        </Segment>
                    </Form>

                    <Modal.Description> <br />By signing up, you agree to the Terms and Conditions of AMIE </Modal.Description>
                </Modal.Content>
            </Modal>

        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Mark as unavailable</Button>
    </Container>
    </Container>


}
export default BookMeeting;
