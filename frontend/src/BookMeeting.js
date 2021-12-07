import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Form, Header, Modal, Placeholder, Segment} from "semantic-ui-react";
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
    const [MeetingData, setMT] = useState(undefined);
    const [openReservation, setOpenReservation] = useState(false);
    const [openUnavailable, setopenUnavailableReservation] = useState(false);
    const [openUpdateReservation, setOpenUpdateReservation] = useState(false)
    const [openDel, setOpenDel] = useState(false)

    const [EventMenu, setEventMenu] = useState(false)

    const [User, Setuser] = useState(undefined)
    const localizer = momentLocalizer(moment)
    const [changed, setChanged] = useState(false)

    const [MeetingDeletionInProcess, setMeetingDeletionProgress] = useState(false)
    const [MeetingUpdateProcess, setMeetingUpdateProcess] = useState(false)
    const [MeetingDeletionError, setMeetingDeletionError] = useState(false)

    const [MeetingID, setDI] = useState({
        "meeting_id": "",
    })
    const [registerUpdateMeeting, setRegisterUpdateMeeting] = useState({
        "id": "",
        "name": "",
        "desc": "",
    })
    const [registerRequestReservation, setRegisterRequestReservation] = useState({
        "name": "",
        "desc": "",
        "date": "",
        "start": "",
        "end": "",
        "ro_id": "",
        "us_id": "",
        "attendees": [],
    })
    const [registerRequestUnavailability, setRegisterRequestUnavailability] = useState({
        "uu_date": "",
        "uu_startTime": "",
        "uu_endTime": "",
        "us_id": "",
    })

    const [roomDetails, setRoomDetails] = useState({
        "date": "",
        "start": "",
        "end": ""
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
    const [regIdError, setIdError] = useState(false)
    const [MeetingUpdateError, setMeetingUpdateError] = useState(false)

    const [regSuccessOpen, setRegSuccessOpen] = useState(false)

    const [timeSlot, setTimeSlot] = useState(false)
    const [roomSlot, setRoomSlot] = useState(false)
    const [otherTimeSlot, setOtherTimeSlot] = useState(false)
    const [attendeesSelected, setAttendeesSelected] = useState(true)
    const [roomSelected, setRoomSelected] = useState(true)

    const handleTimeSlot = (e) => {
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "attendees": registerRequestReservation.attendees,
                "date": registerRequestReservation.date
            }),
            redirect: 'follow'
        };

        fetch(Constants.ApiURL + "meetings/users/available", requestOptions)
            .then(response => {
                if (!response.ok) {
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data !== undefined) {
                let t = data.map(x => ({
                    value: x.start_time,
                    key: x.start_time,
                    text: x.start_time
                }))
                setTimeSlot(t)
            }
        });

    }

    const handleOtherTimeSlot = (e) => {
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "attendees": registerRequestReservation.attendees,
                "date": registerRequestReservation.date
            }),
            redirect: 'follow'
        };

        fetch(Constants.ApiURL + "meetings/users/available", requestOptions)
            .then(response => {
                if (!response.ok) {
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data !== undefined) {
                let t = data.map(x => ({
                    value: x.end_time,
                    key: x.end_time,
                    text: x.end_time
                }))
                setOtherTimeSlot(t)
            }
        });

    }

    const handleRoomSlots = (e) => {

        if (props.user !== undefined) {
            fetch(Constants.ApiURL + "rooms/available/" + props.user.us_id + "?date=" +
                roomDetails.date + "&start=" + roomDetails.start + "&end=" + roomDetails.end)
                .then(response => {
                    if (!response.ok) {
                        return undefined
                    }
                    return response.json()
                }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    let t = data.map(x => ({
                        value: x.ro_id,
                        text: x.ro_name,
                        key: x.ro_id
                    }))
                    setRoomSlot(t)
                }
            })
        }
    }

    const handleSetAttendees = (e) => {
        handleTimeSlot();
        handleOtherTimeSlot();
        setAttendeesSelected(false);
    }

    const handleGetRooms = (e) => {
        if (registerRequestReservation.date === "") {
            setDateError("Please specify date")
        } else {
            setDateError(false)
        }

        if (registerRequestReservation.start === "") {
            setStTimeError("Please specify starting time")
        } else {
            setStTimeError(false)
        }

        if (registerRequestReservation.end === "") {
            setEndTimeError("Please specify end time")
        } else {
            setEndTimeError(false)
        }

        if (registerRequestReservation.date === "" ||
            registerRequestReservation.start === "" ||
            registerRequestReservation.end === ""
        ) {
            setRegistrationInProgress(false)
            return;
        }

        // setRoomDetails({...roomDetails,
        //     "date": registerRequestReservation.date,
        //     "start": registerRequestReservation.start,
        //     "end": registerRequestReservation.end
        // })

        roomDetails.date = registerRequestReservation.date
        roomDetails.start = registerRequestReservation.start
        roomDetails.end = registerRequestReservation.end


        handleRoomSlots();
        setRoomSelected(false);
    }

    const handleUnavailableSubmission = (e) => {
        console.log(registerRequestUnavailability)
        setRegistrationInProgress(true)
        setRegistrationError(false)

        //Validation
        if (registerRequestUnavailability.uu_date === "") {
            setDateError("Please specify date")
        } else {
            setDateError(false)
        }
        if (registerRequestUnavailability.uu_startTime === "") {
            setStTimeError("Please specify starting time")
        } else {
            setStTimeError(false)
        }
        if (registerRequestUnavailability.uu_endTime === "") {
            setEndTimeError("Please specify end time")
        } else {
            setEndTimeError(false)
        }
        if (registerRequestUnavailability.uu_date === "" ||
            registerRequestUnavailability.uu_startTime === "" ||
            registerRequestUnavailability.uu_endTime === ""
        ) {
            setRegistrationInProgress(false)
            return;
        }

        registerRequestUnavailability.us_id = props.user.us_id

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(registerRequestUnavailability)
        };

        fetch(Constants.ApiURL + "/users/availability/" + props.user.us_id, requestOptions)
            .then(response => {
                setRegistrationInProgress(false);
                if (response.status === 500) {
                    setRegistrationError(true)
                    setRegistrationErrorText("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    setMTNameError("Unavailability already exists!")
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data === undefined) {
                return
            }
            if (data.uu_id === null) {
                setMTNameError("Reservation already exists!")
                return undefined
            }
            setopenUnavailableReservation(false)
            setRegSuccessOpen(true)
        })
    }


    const handleMeetingSubmission = (e) => {
        console.log(registerRequestReservation)
        setRegistrationInProgress(true)
        setRegistrationError(false)

        //Validation

        if (registerRequestReservation.name === "") {
            setMTNameError("Please input a meetings name")
        } else {
            setMTNameError(false)
        }
        if (registerRequestReservation.desc === "") {
            setMtDescError("Please input a meetings description")
        } else {
            setMtDescError(false)
        }
        if (registerRequestReservation.date === "") {
            setDateError("Please specify date of the meeting")
        } else {
            setDateError(false)
        }
        if (registerRequestReservation.start === "") {
            setStTimeError("Please specify starting time")
        } else {
            setStTimeError(false)
        }
        if (registerRequestReservation.end === "") {
            setEndTimeError("Please specify end time")
        } else {
            setEndTimeError(false)
        }
        if (registerRequestReservation.ro_id === "") {
            setRegRoIdError("Please specify Room")
        } else {
            setRegRoIdError(false)
        }
        if (registerRequestReservation.attendees === []) {
            setAttendeesError("Please specify attendees")
        } else {
            setAttendeesError(false)
        }

        if (registerRequestReservation.name === "" ||
            registerRequestReservation.desc === "" ||
            registerRequestReservation.date === "" ||
            registerRequestReservation.start === "" ||
            registerRequestReservation.end === "" ||
            registerRequestReservation.ro_id === "" ||
            registerRequestReservation.attendees === "") {
            setRegistrationInProgress(false)
            return;
        }

        registerRequestReservation.us_id = props.user.us_id

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(registerRequestReservation)
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
            setOpenReservation(false)
            setRegSuccessOpen(true)
        })
    }
    const handleUpdateSubmission = (e) => {
        console.log(registerUpdateMeeting)
        setMeetingUpdateProcess(true)
        setRegistrationError(false)

        //Validation
        if (registerUpdateMeeting.name === "") {
            setMTNameError("Please specify new name")
        } else {
            setMTNameError(false)
        }
        if (registerUpdateMeeting.desc === "") {
            setMtDescError("Please specify new description")
        } else {
            setMtDescError(false)
        }

        if (registerUpdateMeeting.name === "" ||
            registerUpdateMeeting.desc === ""
        ) {
            setRegistrationInProgress(false)
            return;
        }
        registerUpdateMeeting.id = MeetingData
        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(registerUpdateMeeting)
        };
        if (props.user !== undefined) {
            let user = props.user.us_id
            fetch(Constants.ApiURL + "/meetings/" + MeetingData + "/" + user, requestOptions)
                .then(response => {
                    setMeetingUpdateProcess(false);
                    if (response.status === 500) {
                        setMeetingUpdateError(true)
                        console.log("An unknown error occurred on the server")
                    }
                    if (response.status !== 201) {
                        console.log("Meeting created by another user")
                        return undefined
                    }

                    return response.json()
                }).then(data => {
                console.log(data)
                setOpenUpdateReservation(false)
                setChanged(true)
                console.log("Value of changed in creation:" + changed)
            })
        }
    }


    const handleMeetingDelete = (e) => {
        setOpenDel(true)
    }
    const handleDeleteClose = (e) => {
        setOpenDel(false)
    }
    const handleMenu = (id) => {
        setMT(id)
        setEventMenu(true)
    }
    const handleMeetingUpdate = (e) => {
        setOpenUpdateReservation(true)
    }

    const handleDeleteSubmission = (e) => {

        if (MeetingData === "") {
            setIdError("Meeting does not exist")
        } else {
            setIdError(false)
        }
        if (props.user !== undefined) {
            let user = props.user.us_id
            const requestOptions = {method: 'DELETE'};

            fetch(Constants.ApiURL + "/meetings/" + MeetingData + "/" + user, requestOptions)
                .then(response => {
                    setMeetingDeletionProgress(false);
                    return response, response.json()
                }).then((response, data) => {
                console.log("Value of changed during delete submission: " + changed)
                setOpenDel(false)
                setChanged(true)
                console.log("Value of change after delete submission: " + changed)
            })
            setEventMenu(false)
            fetch(Constants.ApiURL)
        }

    }

    function ListMaker(temp) {
        let originalstring, separatedArray, separated;
        originalstring = temp;
        separatedArray = [];

        let previousIndex = 0, i;

        for (i = 0; i < originalstring.length; i++) {
            if (originalstring[i] == ',') {
                separated = originalstring.slice(previousIndex, i);
                separatedArray.push(separated.toString());
                previousIndex = i + 1;
            }
        }
        separatedArray.push(originalstring.slice(previousIndex, i))
        return separatedArray
    }

    //Adding calendar effect, to see Reservation & Unavailability
    useEffect(() => {
        if (props.user !== undefined) {
            fetch(Constants.ApiURL + "users/" + props.user.us_id + "/schedule")
                .then(response => {
                    if (!response.ok) {
                        setDates([{
                            'title': 'Selection',
                            'allDay': false,
                            'start': new Date(moment.now()),
                            'end': new Date(moment.now())
                        }])
                        return undefined
                    }
                    return response.json()
                }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    let events = data.map(event => ({
                        title: event.title,
                        desc: {
                            'Room': event.room,
                            'Description': event.desc,
                            'Creator': event.creator,
                            'Username': event.username,
                            'Meeting_Id': event.mt_id
                        },
                        start: new Date(event.date + ' ' + event.start),
                        end: new Date(event.date + ' ' + event.end),
                        allDay: false
                    }))
                    setDates(events)
                }
            })
        } else {
            if (props.room !== undefined) {
                fetch(Constants.ApiURL + "rooms/" + props.room + "/schedule")
                    .then(response => {
                        if (!response.ok) {
                            setDates([{
                                'title': 'Selection',
                                'allDay': false,
                                'start': new Date(moment.now()),
                                'end': new Date(moment.now())
                            }])
                            return undefined
                        }
                        return response.json()
                    }).then(data => {
                    console.log(data)
                    if (data !== undefined) {
                        let events = data.map(event => ({
                            title: event.title,
                            desc: {
                                'Room': event.room,
                                'Creator': event.creator,
                                'Username': event.username
                            },
                            start: new Date(event.date + ' ' + event.start),
                            end: new Date(event.date + ' ' + event.end),
                            allDay: false
                        }))
                        setDates(events)
                    }
                })
            }
        }
    }, []);

    function EventPropGetter(event, start, end, isSelected) {
        return {
            style: {backgroundColor: event.title === 'Unavailable' ? 'crimson' : 'steelblue'}
        }
    }

    function Event({event}) {
        if (event !== undefined || event !== "") {
            let title = event.title + ' - Room: ' + event.desc.Room;
            let description = 'Description: ' + event.desc.Description;
            let reservation = 'Reserved by: ' + event.desc.Creator + ' (' + event.desc.Username + ')';
            let id = 'Reservation Id:' + event.desc.Meeting_Id;

            if (event.title === 'Unavailable') {
                title = event.title;
                description = '';
                reservation = 'Reserved by: ' + event.desc.Creator;
                id = 'Reservation Id:' + event.desc.Meeting_Id;
            }
            return (
                <span>
              <strong>{title}</strong>
                    <div class="text--wrap">
                        <p>{description}</p>
                        <p>{reservation}</p>
                        <p>{id}</p>
                    </div>
            </span>
            )
        }
    }

    return <Container style={{height: 800}}><Calendar
        selectable
        localizer={localizer}
        components={{event: Event}}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelectEvent={event => handleMenu(event.desc.Meeting_Id)}

        onSelecting={(selected) => {
            setDates([{
                'title': 'Selection',
                'allDay': false,
                'start': new Date(selected.start),
                'end': new Date(selected.end)
            }])
        }}
        eventPropGetter={EventPropGetter}
    >

    </Calendar>

        {/*Reservation Creation*/}
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
                        onChange={(e) => {
                            setRegisterRequestReservation({...registerRequestReservation, "name": e.target.value})
                        }}
                    />
                    <Form.Input
                        label='Meeting Description' placeholder='Description' required
                        error={registrationError ? registrationError : regMtDescError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestReservation({...registerRequestReservation, "desc": e.target.value})
                        }}
                    />
                    <Form.Input
                        label='Meeting Date' placeholder='YYYY-MM-DD' required
                        error={registrationError ? registrationError : regDateError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestReservation({...registerRequestReservation, "date": e.target.value})
                        }}
                    />
                    <Form.Input
                        label='Attendees' type='Attendees' required
                        error={registrationError ? registrationError : regAttendeesError}
                        disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestReservation({
                                ...registerRequestReservation,
                                "attendees": ListMaker(e.target.value)
                            })
                        }}
                    />

                    <Button loading={registrationInProgress} content='Generate Time Slots' primary
                            onClick={handleSetAttendees}/>

                    <Form.Input
                        label='Meeting Start Time' placeholder='HH:MM:SS' required
                        error={registrationError ? registrationError : regStTimeError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestReservation({...registerRequestReservation, "start": e.target.value})
                        }}
                    />

                    {/*                        {
                            timeSlot === undefined ?
                            <Placeholder>
                                <Placeholder.Line/>
                            </Placeholder> :
                            <Form.Dropdown
                                label="Meeting Start Time" placeholder='HH:MM:SS' required
                                search selection options={timeSlot} disabled={attendeesSelected}
                                onChange={(e, data) => {
                                    setRegisterRequestReservation({...registerRequestReservation, "start": data.value})
                                    console.log(data.value)
                                }}
                            />

                        }*/}
                    <Form.Input
                        label='Meeting End Time' placeholder='HH:MM:SS' required
                        error={registrationError ? registrationError : regEndTimeError}
                        disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestReservation({...registerRequestReservation, "end": e.target.value})
                        }}
                    />
                    {/*{
                            otherTimeSlot === undefined ?
                            <Placeholder>
                                <Placeholder.Line/>
                            </Placeholder> :
                            <Form.Dropdown
                                label="Meeting End Time" placeholder='HH:MM:SS' required
                                search selection options={otherTimeSlot} disabled={attendeesSelected}
                                onChange={(e, data) => {
                                    setRegisterRequestReservation({...registerRequestReservation, "end": data.value})
                                    console.log(data.value)
                                }}
                            />

                        }*/}
                    <Button loading={registrationInProgress} content='Check Available Rooms' primary
                            onClick={handleGetRooms}/>

                    {
                        roomSlot === undefined ?
                            <Placeholder>
                                <Placeholder.Line/>
                            </Placeholder> :
                            <Form.Dropdown
                                label="Rooms" placeholder='Select' required
                                error={registrationError ? registrationError : regRoIdError}
                                search selection options={roomSlot} disabled={roomSelected}
                                onChange={(e, data) => {
                                    setRegisterRequestReservation({...registerRequestReservation, "ro_id": data.value})
                                    console.log(data.value)
                                }}
                            />
                    }

                    <Segment basic textAlign={"center"}>
                        <Button loading={registrationInProgress} content='Create Meeting' primary
                                onClick={handleMeetingSubmission}/>
                    </Segment>
                </Form>
            </Modal.Content>
        </Modal>

        {/*Create Unavailability*/}
        <Modal
            centered={false}
            open={openUnavailable}
            onClose={() => setopenUnavailableReservation(false)}
            onOpen={() => setopenUnavailableReservation(true)}
        >
            <Modal.Header> Mark Unavailable time </Modal.Header>
            <Modal.Content>
                {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                <Form>
                    <Form.Input
                        label='Unavailability Date' placeholder='YYYY-MM-DD' required
                        error={registrationError ? registrationError : regDateError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestUnavailability({
                                ...registerRequestUnavailability,
                                "uu_date": e.target.value
                            })
                        }}
                    />

                    {/*<button className="ui toggle button"*/}
                    {/*        aria-pressed="false">All Day</button>*/}

                    <Form.Input
                        label='Meeting Start Time' placeholder='HH:MM:SS' required
                        error={registrationError ? registrationError : regStTimeError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestUnavailability({
                                ...registerRequestUnavailability,
                                "uu_startTime": e.target.value
                            })
                        }}
                    />
                    <Form.Input
                        label='Meeting End Time' placeholder='HH:MM:SS' required
                        error={registrationError ? registrationError : regEndTimeError}
                        disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterRequestUnavailability({
                                ...registerRequestUnavailability,
                                "uu_endTime": e.target.value
                            })
                        }}
                    />
                    <Segment basic textAlign={"center"}>
                        <Button loading={registrationInProgress} content='Mark Unavailable' primary
                                onClick={handleUnavailableSubmission}/>

                    </Segment>
                </Form>
            </Modal.Content>
        </Modal>

        {/*Reservation Menu*/}
        <Modal
            centered={true}
            open={EventMenu}
            onClose={() => setEventMenu(false)}
            onOpen={() => setEventMenu(true)}
        >
            <Modal.Header>Meeting options </Modal.Header>
            <Modal.Content>
                {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                <Form>

                    <Segment basic textAlign={"center"}>
                        <Button content='Delete' className='ui button inverted' primary onClick={handleMeetingDelete}/>
                        <Button content='Update' className='ui button inverted' primary onClick={handleMeetingUpdate}/>
                    </Segment>
                </Form>
            </Modal.Content>
        </Modal>

        {/*Update Reservation*/}
        <Modal
            centered={false}
            open={openUpdateReservation}
            onClose={() => setOpenUpdateReservation(false)}
            onOpen={() => setOpenUpdateReservation(true)}
        >
            <Modal.Content>
                {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                <Form>
                    <Form.Input
                        label='Meeting Name' placeholder='New Name:' required
                        error={registrationError ? registrationError : regMtNameError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterUpdateMeeting({...registerUpdateMeeting, "name": e.target.value})
                        }}
                    />
                    <Form.Input
                        label='Meeting Description' placeholder='New Description:' required
                        error={registrationError ? registrationError : regMtDescError} disabled={registrationInProgress}
                        onChange={(e) => {
                            setRegisterUpdateMeeting({...registerUpdateMeeting, "desc": e.target.value})
                        }}
                    />

                    <Segment basic textAlign={"center"}>

                        <Button loading={registrationInProgress} content='Update' primary
                                onClick={handleUpdateSubmission}/>
                    </Segment>
                </Form>
            </Modal.Content>
        </Modal>

        {/*Deleting Reservation*/}
        <Modal
            centered={true}
            open={openDel}
            onClose={() => setOpenDel(false)}
            onOpen={() => setOpenDel(true)}
        >
            <Modal.Content>
                {registrationError ? <Header textAlign="center"
                                             size="medium">{registrationErrorText}</Header> : "Are you Sure You Want to Delete This Meeting?"}

                <Segment basic textAlign={"center"}>

                    <Button loading={registrationInProgress} content='Delete' className='ui button negative' primary
                            onClick={handleDeleteSubmission}/>
                    <Button loading={registrationInProgress} content='Go Back' className='ui button positive' primary
                            onClick={handleDeleteClose}/>
                </Segment>

            </Modal.Content>
        </Modal>

        <div class="fluid">
            <Button
                color={"green"}
                onClick={() => {
                    setOpenReservation(true)
                }}
                class='ui left floated very compact button negative'
            > Book Meeting </Button
            >
            <Button
                color={"green"}
                onClick={() => {
                    setopenUnavailableReservation(true)
                }}
                class='ui right floated very compact button negative'
            > Mark as unavailable</Button>


        </div>
    </Container>


}

export default BookMeeting;
