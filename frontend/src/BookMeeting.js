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


function BookMeeting(props) {
    const [dates, setDates] = useState([]);
    const [openReservation, setOpenReservation] = useState(false);
    const [openUnavailable, setopenUnavailableReservation] = useState(false);
    const [openUpdateReservation, setOpenUpdateReservation] = useState(false)
    const [openDeleteReservation, setOpenDeleteReservation] = useState(false)

    const [User, Setuser] = useState(undefined)
    const localizer = momentLocalizer(moment)
    const [DeleteID, setDI] = useState(undefined)
    const [changed, setChanged] = useState(false)
    const [openDel, setOpenDel] = useState(false)
    const [MeetingDeletionInProcess, setMeetingDeletionProgress] = useState(false)
    const [MeetingDeletionError, setMeetingDeletionError]= useState(false)


    const [registerRequest, setRegisterRequest] = useState({
        "name": "",
        "desc": "",
        "date": "",
        "start": "",
        "end": "",
        "ro_id": "",
        "us_id": "",
        "attendees": [],
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


      // class ButtonExampleToggle extends Component {
  //   state = {}
  //   handleClick = () =>
  //   this.setState((prevState) => ({ active: !prevState.active }))
  //
  //   render() {
  //   const { active } = this.state
  //
  //       return (
  //       <Button toggle active={active} onClick={this.handleClick}>
  //           Toggle
  //       </Button>
  //       )
  //   }
  // }

    const handleMeetingSubmission = (e) => {
        console.log(registerRequest)
        setRegistrationInProgress(true)
        setRegistrationError(false)

        //Validation

        if (registerRequest.name === "") {
            setMTNameError("Please input a meetings name")
        } else {
            setMTNameError(false)
        }
         if (registerRequest.desc === "") {
            setMtDescError("Please input a meetings description")
        } else {
            setMtDescError(false)
        }
        if (registerRequest.date === "") {
            setDateError("Please specify date of the meeting")
        } else {
            setDateError(false)
        }
        if (registerRequest.start === "") {
            setStTimeError("Please specify starting time")
        } else {
            setStTimeError(false)
        }
        if (registerRequest.end === "") {
            setEndTimeError("Please specify end time")
        } else {
            setEndTimeError(false)
        }
        if (registerRequest.ro_id === "") {
            setRegRoIdError("Please specify Room")
        } else {
            setRegRoIdError(false)
        }
            if (registerRequest.attendees === []) {
            setAttendeesError("Please specify attendees")
        } else {
            setAttendeesError(false)
        }

        if (registerRequest.name === "" ||
            registerRequest.desc === "" ||
            registerRequest.date === "" ||
            registerRequest.start === "" ||
            registerRequest.end === "" ||
            registerRequest.ro_id === "" ||
            registerRequest.attendees === "") {
            setRegistrationInProgress(false)
            return;
        }

        registerRequest.us_id= props.user.us_id

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(registerRequest)
        };

        fetch(Constants.ApiURL + "/meetings", requestOptions)
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
            setopenUnavailableReservation(false)
            setRegSuccessOpen(true)
        })
    }

 const handleRoomDeletion = (id) => {
        setOpenDel(true)
        setMeetingDeletionProgress(true)
        setDI(id)
    }

    const handleDeleteSubmission = (e) => {
        if (DeleteID !== undefined) {
            const requestOptions = {method: 'DELETE'};

            fetch(Constants.ApiURL + "/meetings/" + props.user.us_id + "/" + DeleteID, requestOptions)
                .then(response => {
                    setMeetingDeletionProgress(false);
                    return response, response.json()
                }).then((response, data) => {
                console.log("Value of changed during delete submission: " + changed)
                setOpenDel(false)
                setChanged(true)
                console.log("Value of change after delete submission: " + changed)
            })
        }

    }

    function ListMaker(temp) {
        let originalstring, separatedArray, separated;
        originalstring = temp;
        separatedArray = [];

        let  previousIndex= 0, i;

        for(i= 0; i<originalstring.length; i++){
            if(originalstring[i]== ','){
                separated = originalstring.slice(previousIndex, i);
                separatedArray.push(separated.toString());
                previousIndex = i + 1;
            }
        }
        separatedArray.push(originalstring.slice(previousIndex,i))
        return separatedArray
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
            open={openReservation}
            onClose={() => setOpenReservation(false)}
            onOpen={() => setOpenReservation(true)}
        >
            <Modal.Header>Create a Meeting </Modal.Header>
                <Modal.Content>
                    <Form>
                        {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                        <Form.Input
                            label='Meeting Name' placeholder='Meeting Name' required
                            error={registrationError ? registrationError : regMtNameError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "name": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting Description' placeholder='Description' required
                            error={registrationError ? registrationError : regMtDescError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "desc": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting Date' placeholder='YYYY-MM-DD' required
                            error={registrationError ? registrationError : regDateError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "date": e.target.value }) }}
                        />

                        {/*<button className="ui toggle button"*/}
                        {/*        aria-pressed="false">All Day</button>*/}

                        <Form.Input
                            label='Meeting Start Time' placeholder='HH:MM:SS' required
                            error={registrationError ? registrationError : regStTimeError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "start": e.target.value }) }}
                        />
                        <Form.Input
                            label='Meeting End Time' placeholder='HH:MM:SS' required
                            error={registrationError ? registrationError : regEndTimeError} disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "end": e.target.value }) }}
                        />
                        <Form.Input
                            label='Room Id' type='Room' required
                            error={registrationError ? registrationError : regRoIdError}
                            disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "ro_id": e.target.value  }) }}
                        />

                        <Form.Input
                            label='Attendees' type='Attendees' required
                            error={registrationError ? registrationError : regAttendeesError}
                            disabled={registrationInProgress}
                            onChange={(e) => { setRegisterRequest({ ...registerRequest, "attendees": ListMaker(e.target.value)}) }}
                        />

                        <Segment basic textAlign={"center"}>
                            <Button loading={registrationInProgress} content='Create Meeting' primary onClick={handleMeetingSubmission} />
                        </Segment>
                    </Form>
                </Modal.Content>
            </Modal>
        <Modal
            centered={false}
            open={openUnavailable}
            onClose={() => setopenUnavailableReservation(false)}
            onOpen={() => setopenUnavailableReservation(true)}
        >
             <Modal.Header>Create a Meeting </Modal.Header>
                <Modal.Content>
                    This is a temporary thing, la cagaste xdxdxd
                    <Segment basic textAlign={"center"}>
                        <Button onClick={ () => setopenUnavailableReservation(false)} > Close </Button>
                        </Segment>
                </Modal.Content>


        </Modal>

        <div class = "fluid">
        <Button
            color={"green"}
            onClick={() => {setOpenReservation(true)}}
            class='ui left floated very compact button negative'
        > Book Meeting </Button
            >
        <Button
            color={"green"}
            onClick={() => {setopenUnavailableReservation(true)}}
            class='ui left floated very compact button negative'
        > Mark as unavailable</Button>
        <Button
            color={"red"}
            onClick={() => {setOpenUpdateReservation()} }
            class='ui left floated very compact button negative'
        > Delete Meeting</Button>
        <Button
            color={"blue"}
            onClick={() => {setOpenUpdateReservation()} }
            class='ui left floated very compact button negative'
         > Update Meeting</Button>
    </div>
    </Container>


}
export default BookMeeting;
