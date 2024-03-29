import React, {useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './RoomManagement.css'
import {Button, Form, Modal, Placeholder, Segment, Table} from "semantic-ui-react";
import Constants from './Constants';
import Schedule from './Schedule';

export default function RoomManagement(props) {

    const [RoomData, setRD] = useState(undefined)
    const [DeleteID, setDI] = useState(undefined)
    const [SchedID, setSID] = useState(undefined)
    const [changed, setChanged] = useState(false)
    const [SchedData, setSchedData] = useState(undefined)
    const [RoomCreationInProgress, setRoomCreationProgress] = useState(false)
    const [RoomCreationError, setRoomCreationError] = useState(false)
    const [RTypes, setRTypes] = useState(undefined)


    const [regNameError, setRegNameError] = useState(false)
    const [regLocationError, setRegLocationError] = useState(false)
    const [regTypeError, setRegTypeError] = useState(false)

    const [UnavailError, setUnavailError] = useState(false)
    const [UnavailErrorText, setUnavailErrorText] = useState(undefined)
    const [UnavailDateError, setUnavailDateError] = useState(false)
    const [UnavailStartError, setUnavailStartError] = useState(false)
    const [UnavailEndError, setUnavailEndError] = useState(false)
    const [UnavailInProgress, setUnavailInProgress] = useState(false)
    const [UnavailWindowOpen, setUnavailWindowOpen] = useState(false)

    const [upNameError, setUpNameError] = useState(false)
    const [upLocationError, setUpLocationError] = useState(false)
    const [upTypeError, setUpTypeError] = useState(false)

    const [open, setOpen] = useState(false)
    const [openDel, setOpenDel] = useState(false)
    const [openUpd, setOpenUpd] = useState(false)
    const [openSched, setOpenSched] = useState(false)

    const [RoomDeletionInProgress, setRoomDeletionProgress] = useState(false)
    const [RoomDeletionError, setRoomDeletionError] = useState(false)

    const [RoomUpdateRequest, setRoomUpdateRequest] = useState({
        "ro_name": "",
        "ro_location": "",
        "rt_id": ""
    })

    const [RoomUnavailabilityRequest, setRoomUnavailabilityRequest] = useState({
        "ru_date": "",
        "ru_startTime": "",
        "ru_endTime": "",
        "us_id": ""
    })

    const [RoomCreationRequest, setRoomCreationRequest] = useState({
        "ro_name": "",
        "ro_location": "",
        "rt_id": ""
    });

    const [roName, setRoName] = useState(undefined)
    const [roLocation, setRoLocation] = useState(undefined)
    const [roType, setRtype] = useState(undefined)
    const [roID, setRoID] = useState(undefined)

    const [RoomUpdateInProgress, setRoomUpdateProgress] = useState(false)
    const [RoomUpdateError, setRoomUpdateError] = useState(false)

    let payload = (<Table singleLine>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>ID</Table.HeaderCell>
                    <Table.HeaderCell>Name</Table.HeaderCell>
                    <Table.HeaderCell>Location</Table.HeaderCell>
                    <Table.HeaderCell>Type ID</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
        </Table>
    )

    const closeDelWindow = (e) => {
        setOpenDel(false)
    }

    const closeUpdWindow = (e) => {
        setOpenUpd(false)
    }

    const closeSchedWindow = (e) => {
        setOpenSched(false)
    }

    const closeUnavailWindow = (e) => {
        setUnavailWindowOpen(false)
    }

    const handleUnavail = (e) => {
        setUnavailWindowOpen(true)
    }

    const refreshData = (e) => {
        fetch(Constants.ApiURL + "/rooms")
            .then(response => {
                if (!response.ok) {
                    console.log("There has been an error getting all rooms")
                    return undefined
                }
                return response.json()
            }).then(data => {
            if (data !== undefined) {
                setRD(data)
            }
        })

        return (
            <div style={{
                padding: '15px',
                margin: 'auto',
                width: 'auto',
                paddingTop: '3%',
                backgroundColor: 'lightgray'
            }}>

                <Modal
                    centered={true}
                    open={open}
                    onClose={() => {
                        RoomCreationInProgress ? setOpen(true) :
                            setOpen(false)
                    }
                    }
                    onOpen={() => setOpen(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Creation</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Name' placeholder='Name' required
                                error={RoomCreationError ? RoomCreationError : regNameError}
                                disabled={RoomCreationInProgress}
                                onChange={(e) => {
                                    setRoomCreationRequest({...RoomCreationRequest, "ro_name": e.target.value})
                                }}
                            />
                            <Form.Input
                                label='Location' placeholder='Location' required
                                error={RoomCreationError ? RoomCreationError : regLocationError}
                                disabled={RoomCreationInProgress}
                                onChange={(e) => {
                                    setRoomCreationRequest({...RoomCreationRequest, "ro_location": e.target.value})
                                }}
                            />
                            {
                                RTypes === undefined ?
                                    <Placeholder>
                                        <Placeholder.Line/>
                                    </Placeholder> :
                                    <Form.Dropdown
                                        label="Room Type" placeholder='' required
                                        search selection options={RTypes} disabled={RoomCreationInProgress}
                                        error={RoomCreationError ? RoomCreationError : regTypeError}
                                        onChange={(event, data) => {
                                            setRoomCreationRequest({...RoomCreationRequest, "rt_id": data.value})
                                            console.log(data.value)
                                        }}
                                    />

                            }
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive' loading={RoomCreationInProgress}
                                        content='Create Room' primary onClick={handleSubmission}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={openUpd}
                    onOpen={() => setOpenUpd(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Update</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Name' placeholder='' required
                                disabled={RoomUpdateInProgress}
                                onChange={(e) => {
                                    setRoomUpdateRequest({...RoomUpdateRequest, "ro_name": e.target.value})
                                }}
                            />
                            <Form.Input
                                label='Location' placeholder='' required
                                disabled={RoomUpdateInProgress}
                                onChange={(e) => {
                                    setRoomUpdateRequest({...RoomUpdateRequest, "ro_location": e.target.value})
                                }}
                            />
                            {
                                RTypes === undefined ?
                                    <Placeholder>
                                        <Placeholder.Line/>
                                    </Placeholder> :
                                    <Form.Dropdown
                                        label="Room Type" placeholder='' required
                                        search selection options={RTypes} disabled={RoomUpdateInProgress}
                                        onChange={(event, data) => {
                                            setRoomUpdateRequest({...RoomUpdateRequest, "rt_id": data.value})
                                            console.log(data.value)
                                        }}
                                    />

                            }
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive' loading={RoomUpdateInProgress}
                                        content='Update Room' primary onClick={handleRoomUpdateSubmission}/>
                                <Button className='ui button ' content='No, take me back' onClick={closeUpdWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={UnavailWindowOpen}
                    onOpen={() => setUnavailWindowOpen(true)}
                    size="tiny"
                >
                    <Modal.Header>Mark Room Unavailability</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Date' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_date": e.target.value
                                    })
                                }}
                            />
                            <Form.Input
                                label='Start Time' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_startTime": e.target.value
                                    })
                                }}
                            />
                            <Form.Input
                                label='End Time' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_endTime": e.target.value
                                    })
                                }}
                            />
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive'
                                        content='Submit' primary onClick={handleUnavailableSubmission}/>
                                <Button className='ui button ' content='No, take me back'
                                        onClick={closeUnavailWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={openDel}
                    onOpen={() => setOpenDel(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Deletion</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <p>Are you sure you would like to delete this room?</p>
                        </Modal.Description>
                        <Form>
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button negative' content='Yes, I am sure' primary
                                        onClick={handleDeleteSubmission}/>
                                <Button className='ui button ' content='No, take me back' onClick={closeDelWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>

                <Modal
                    centered={true}
                    open={openSched}
                    onOpen={() => setOpenSched(true)}
                    size="large"
                >
                    <Modal.Header>Room Schedule</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Schedule room={SchedID}/>
                        </Modal.Description>
                        <Form>
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button primary positive ' content='Mark Unavail.'
                                        onClick={handleUnavail}/>
                                <Button className='ui button ' content='Close' onClick={closeSchedWindow}/>
                            </Segment>
                            <Segment>{UnavailError}</Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>

                <Table className={"ui selectable celled table"} singleLine>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>ID</Table.HeaderCell>
                            <Table.HeaderCell>Name</Table.HeaderCell>
                            <Table.HeaderCell>Location</Table.HeaderCell>
                            <Table.HeaderCell>Type ID</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {RoomData.map((u) => {
                            return (
                                <Table.Row key={u.ro_id} positive>
                                    <Table.Cell>{u.ro_id}</Table.Cell>
                                    <Table.Cell>{u.ro_name}
                                        <div className='ui right floated buttons'>
                                            <button onClick={handleRoomDeletion.bind(this, u.ro_id)}
                                                    className='ui right floated very compact button negative'>Delete
                                            </button>
                                            <button onClick={handleRoomUpdate.bind(this, u)}
                                                    className='ui right floated very compact button primary'>Update
                                            </button>
                                            <button onClick={handleSchedule.bind(this, u.ro_id)}
                                                    className='ui right floated very compact button'>Schedule
                                            </button>
                                        </div>
                                    </Table.Cell>
                                    <Table.Cell>{u.ro_location}</Table.Cell>
                                    <Table.Cell>{u.rt_id}</Table.Cell>
                                </Table.Row>
                            );
                        })}
                    </Table.Body>
                </Table>
                <div>
                    <button className='ui button positive' onClick={handleRoomCreation}>Create new room</button>
                </div>
            </div>

        )
    }

    const handleUnavailableSubmission = (e) => {

        console.log(props.user.us_id)

        setRoomUnavailabilityRequest({
            ...RoomUnavailabilityRequest,
            "us_id": props.user.us_id
        })

        console.log(RoomUnavailabilityRequest)
        setUnavailInProgress(true)
        setUnavailError(false)

        //Validation
        if (RoomUnavailabilityRequest.ru_date === "") {
            setUnavailDateError("Please specify date")
        } else {
            setUnavailDateError(false)
        }
        if (RoomUnavailabilityRequest.ru_startTime === "") {
            setUnavailStartError("Please specify starting time")
        } else {
            setUnavailStartError(false)
        }
        if (RoomUnavailabilityRequest.ru_endTime === "") {
            setUnavailEndError("Please specify end time")
        } else {
            setUnavailEndError(false)
        }
        if (RoomUnavailabilityRequest.ru_date === "" ||
            RoomUnavailabilityRequest.ru_startTime === "" ||
            RoomUnavailabilityRequest.ru_endTime === ""
        ) {
            setUnavailInProgress(false)
            return;
        }


        const UnavailRequestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(RoomUnavailabilityRequest)
        };

        fetch(Constants.ApiURL + "rooms/" + SchedID + "/schedule-unavailable", UnavailRequestOptions)
            .then(response => {
                setUnavailInProgress(false);
                if (response.status === 500) {
                    setUnavailError(true)
                    setUnavailErrorText("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    setUnavailErrorText("Unavailability already exists!")
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data === undefined) {
                return
            }
            if (data.ru_id === null) {
                setUnavailErrorText("Reservation already exists!")
                return undefined
            }
            setUnavailInProgress(false)
            setUnavailWindowOpen(false)
            setOpenSched(false)
        })
    }

    const handleRoomUpdate = (room) => {
        if (RTypes === undefined) {
            fetch(Constants.ApiURL + "rooms/room-types")
                .then(response => {
                    setRoomCreationProgress(false);
                    if (!response.ok) {
                        return undefined
                    }
                    return response.json()
                }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    let R = data.map(x => ({
                        key: x.rt_id,
                        text: x.rt_name,
                        value: x.rt_id
                    }))
                    setRTypes(R)
                }
            })
        }

        setRoomUpdateRequest({...RoomUpdateRequest, "ro_name": room.ro_name})
        setRoomUpdateRequest({...RoomUpdateRequest, "ro_location": room.ro_location})
        setRoomUpdateRequest({...RoomUpdateRequest, "rt_id": room.rt_id})

        setRoName(room.ro_name)
        setRoLocation(room.ro_location)
        setRtype(room.rt_id)
        setRoID(room.ro_id)

        setUpNameError(false)
        setUpLocationError(false)
        setUpTypeError(false)

        setOpenUpd(true);
    }

    const handleRoomUpdateSubmission = (e) => {
        setRoomUpdateProgress(true)
        setRoomUpdateError(false)

        //Validation

        if (RoomUpdateRequest.ro_name === "") {
            setUpNameError("Please input a name")
        } else {
            setUpNameError(false)
        }
        if (RoomUpdateRequest.ro_location === "") {
            setUpLocationError("Please specify a location")
        } else {
            setUpLocationError(false)
        }
        if (RoomUpdateRequest.rt_id === "") {
            setUpTypeError("Please specify a type")
        } else {
            setUpTypeError(false)
        }

        if (RoomUpdateRequest.ro_name === "" ||
            RoomUpdateRequest.ro_location === "" ||
            RoomUpdateRequest.rt_id === "") {
            setRoomUpdateProgress(false)
            return;
        }

        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(RoomUpdateRequest)
        };

        fetch(Constants.ApiURL + "/rooms/" + roID, requestOptions)
            .then(response => {
                setRoomUpdateProgress(false);
                if (response.status === 500) {
                    setRoomUpdateError(true)
                    console.log("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    console.log("Room already exists!")
                    return undefined
                }

                return response.json()
            }).then(data => {
            console.log(data)
            setOpenUpd(false)
            setChanged(true)
            console.log("Value of changed in creation:" + changed)
        })
    }

    const handleRoomDeletion = (id) => {
        setOpenDel(true)
        setRoomDeletionProgress(true)
        setDI(id)
    }

    const handleDeleteSubmission = (e) => {
        if (DeleteID !== undefined) {
            const requestOptions = {method: 'DELETE'};

            fetch(Constants.ApiURL + "rooms/" + DeleteID, requestOptions)
                .then(response => {
                    setRoomDeletionProgress(false);
                    return response, response.json()
                }).then((response, data) => {
                console.log("Value of changed during delete submission: " + changed)
                setOpenDel(false)
                setChanged(true)
                console.log("Value of change after delete submission: " + changed)
            })
        }

    }

    const handleRoomCreation = (e) => {
        if (RTypes === undefined) {
            fetch(Constants.ApiURL + "rooms/room-types")
                .then(response => {
                    setRoomCreationProgress(false);
                    if (!response.ok) {
                        return undefined
                    }
                    return response.json()
                }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    let R = data.map(x => ({
                        key: x.rt_id,
                        text: x.rt_name,
                        value: x.rt_id
                    }))
                    setRTypes(R)
                }
            })
        }

        //Clear it because the fields automatically clear themselves
        setRoomCreationRequest({
            "ro_name": "",
            "ro_location": "",
            "rt_id": "",
        })

        //also clear all the errors
        setRegNameError(false)
        setRegLocationError(false)
        setRegTypeError(false)

        setOpen(true);
    }

    const handleSubmission = (e) => {
        console.log(RoomCreationRequest)
        setRoomCreationProgress(true)
        setRoomCreationError(false)

        //Validation

        if (RoomCreationRequest.ro_name === "") {
            setRegNameError("Please input a name")
        } else {
            setRegNameError(false)
        }
        if (RoomCreationRequest.ro_location === "") {
            setRegLocationError("Please specify a location")
        } else {
            setRegLocationError(false)
        }
        if (RoomCreationRequest.rt_id === "") {
            setRegTypeError("Please specify a type")
        } else {
            setRegTypeError(false)
        }

        if (RoomCreationRequest.ro_name === "" ||
            RoomCreationRequest.ro_location === "" ||
            RoomCreationRequest.rt_id === "") {
            setRoomCreationProgress(false)
            return;
        }

        //Build a re

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(RoomCreationRequest)
        };

        fetch(Constants.ApiURL + "/rooms", requestOptions)
            .then(response => {
                setRoomCreationProgress(false);
                if (response.status === 500) {
                    setRoomCreationError(true)
                    console.log("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    console.log("Room already exists!")
                    return undefined
                }

                return response.json()
            }).then(data => {
            console.log(data)
            if (data === undefined) {
                return
            }
            if (data.ro_id === null) {
                setRoomCreationError("Room already exists!")
                return undefined
            }
            setOpen(false)
            setChanged(true)
            console.log("Value of changed in creation:" + changed)
        })
    }

    const handleSchedule = (ro_id) => {
        setOpenSched(true)
        setSID(ro_id)
    }

    if (RoomData === undefined) {
        fetch(Constants.ApiURL + "/rooms")
            .then(response => {
                if (!response.ok) {
                    console.log("There has been an error getting all rooms")
                    return undefined
                }
                return response.json()
            }).then(data => {
            console.log(data)
            if (data !== undefined) {
                setRD(data)
            }
        })

    } else {
        payload = (
            <div style={{
                padding: '15px',
                margin: 'auto',
                width: 'auto',
                paddingTop: '3%',
                backgroundColor: 'lightgray'
            }}>

                <Modal
                    centered={true}
                    open={open}
                    onClose={() => {
                        RoomCreationInProgress ? setOpen(true) :
                            setOpen(false)
                    }
                    }
                    onOpen={() => setOpen(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Creation</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Name' placeholder='Name' required
                                error={RoomCreationError ? RoomCreationError : regNameError}
                                disabled={RoomCreationInProgress}
                                onChange={(e) => {
                                    setRoomCreationRequest({...RoomCreationRequest, "ro_name": e.target.value})
                                }}
                            />
                            <Form.Input
                                label='Location' placeholder='Location' required
                                error={RoomCreationError ? RoomCreationError : regLocationError}
                                disabled={RoomCreationInProgress}
                                onChange={(e) => {
                                    setRoomCreationRequest({...RoomCreationRequest, "ro_location": e.target.value})
                                }}
                            />
                            {
                                RTypes === undefined ?
                                    <Placeholder>
                                        <Placeholder.Line/>
                                    </Placeholder> :
                                    <Form.Dropdown
                                        label="Room Type" placeholder='' required
                                        search selection options={RTypes} disabled={RoomCreationInProgress}
                                        error={RoomCreationError ? RoomCreationError : regTypeError}
                                        onChange={(event, data) => {
                                            setRoomCreationRequest({...RoomCreationRequest, "rt_id": data.value})
                                            console.log(data.value)
                                        }}
                                    />

                            }
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive' loading={RoomCreationInProgress}
                                        content='Create Room' primary onClick={handleSubmission}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={UnavailWindowOpen}
                    onOpen={() => setUnavailWindowOpen(true)}
                    size="tiny"
                >
                    <Modal.Header>Mark Room Unavailability</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Date' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_date": e.target.value
                                    })
                                }}
                            />
                            <Form.Input
                                label='Start Time' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_startTime": e.target.value
                                    })
                                }}
                            />
                            <Form.Input
                                label='End Time' placeholder='' required
                                disabled={UnavailInProgress}
                                onChange={(e) => {
                                    setRoomUnavailabilityRequest({
                                        ...RoomUnavailabilityRequest,
                                        "ru_endTime": e.target.value
                                    })
                                }}
                            />
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive'
                                        content='Submit' primary onClick={handleUnavailableSubmission}/>
                                <Button className='ui button ' content='No, take me back'
                                        onClick={closeUnavailWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={openUpd}
                    onOpen={() => setOpenUpd(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Update</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Input
                                label='Name' placeholder='' required
                                disabled={RoomUpdateInProgress}
                                onChange={(e) => {
                                    setRoomUpdateRequest({...RoomUpdateRequest, "ro_name": e.target.value})
                                }}
                            />
                            <Form.Input
                                label='Location' placeholder='' required
                                disabled={RoomUpdateInProgress}
                                onChange={(e) => {
                                    setRoomUpdateRequest({...RoomUpdateRequest, "ro_location": e.target.value})
                                }}
                            />
                            {
                                RTypes === undefined ?
                                    <Placeholder>
                                        <Placeholder.Line/>
                                    </Placeholder> :
                                    <Form.Dropdown
                                        label="Room Type" placeholder='' required
                                        search selection options={RTypes} disabled={RoomUpdateInProgress}
                                        onChange={(event, data) => {
                                            setRoomUpdateRequest({...RoomUpdateRequest, "rt_id": data.value})
                                            console.log(data.value)
                                        }}
                                    />

                            }
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button positive' loading={RoomUpdateInProgress}
                                        content='Update Room' primary onClick={handleRoomUpdateSubmission}/>
                                <Button className='ui button ' content='No, take me back' onClick={closeUpdWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
                <Modal
                    centered={true}
                    open={openDel}
                    onOpen={() => setOpenDel(true)}
                    size="tiny"
                >
                    <Modal.Header>Room Deletion</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <p>Are you sure you would like to delete this room?</p>
                        </Modal.Description>
                        <Form>
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button negative' content='Yes, I am sure' primary
                                        onClick={handleDeleteSubmission}/>
                                <Button className='ui button ' content='No, take me back' onClick={closeDelWindow}/>
                            </Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>

                <Modal
                    centered={true}
                    open={openSched}
                    onOpen={() => setOpenSched(true)}
                    size="large"
                >
                    <Modal.Header>Room Schedule</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Schedule room={SchedID}/>
                        </Modal.Description>
                        <Form>
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button primary positive ' content='Mark Unavail.'
                                        onClick={handleUnavail}/>
                                <Button className='ui button ' content='Close' onClick={closeSchedWindow}/>
                            </Segment>
                            <Segment>{UnavailError}</Segment>
                        </Form>

                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>

                <Table className={"ui selectable celled table"} singleLine>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>ID</Table.HeaderCell>
                            <Table.HeaderCell>Name</Table.HeaderCell>
                            <Table.HeaderCell>Location</Table.HeaderCell>
                            <Table.HeaderCell>Type ID</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {RoomData.map((u) => {
                            return (
                                <Table.Row key={u.ro_id} positive>
                                    <Table.Cell>{u.ro_id}</Table.Cell>
                                    <Table.Cell>{u.ro_name}
                                        <div className='ui right floated buttons'>
                                            <button onClick={handleRoomDeletion.bind(this, u.ro_id)}
                                                    className='ui right floated very compact button negative'>Delete
                                            </button>
                                            <button onClick={handleRoomUpdate.bind(this, u)}
                                                    className='ui right floated very compact button primary'>Update
                                            </button>
                                            <button onClick={handleSchedule.bind(this, u.ro_id)}
                                                    className='ui right floated very compact button'>Schedule
                                            </button>
                                        </div>
                                    </Table.Cell>
                                    <Table.Cell>{u.ro_location}</Table.Cell>
                                    <Table.Cell>{u.rt_id}</Table.Cell>
                                </Table.Row>
                            );
                        })}
                    </Table.Body>
                </Table>
                <div>
                    <button className='ui button positive' onClick={handleRoomCreation}>Create new room</button>
                </div>
            </div>

        )
    }


    if (changed) {
        payload = refreshData()
        setChanged(false)
    }

    return payload

}

function timeout(delay) {
    return new Promise(res => setTimeout(res, delay));
}





