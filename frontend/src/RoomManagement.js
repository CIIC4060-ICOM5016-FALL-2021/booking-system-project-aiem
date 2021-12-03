import React, { Component, useState, Fragment } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {
    Button,
    Card,
    Container,
    Form,
    Grid,
    GridColumn,
    Header,
    Modal,
    Placeholder,
    PlaceholderImage, Segment,
    Statistic,
    Table
} from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import Constants from './Constants';

function RoomManagement(){

    const [RoomData, setRD] = useState(undefined)

    const [RoomCreationRequest, setRoomCreationRequest] = useState({
        "ro_name": "",
        "ro_location": "",
        "rt_id": ""
    });
    const [RoomCreationInProgress, setRoomCreationProgress] = useState(false)
    const [RoomCreationError, setRoomCreationError] = useState(false)
    const [RTypes, setRTypes] = useState(undefined)

    const [regNameError, setRegNameError] = useState(false)
    const [regLocationError, setRegLocationError] = useState(false)
    const [regTypeError, setRegTypeError] = useState(false)

    const [open, setOpen] = useState(false)

    const handleRoomCreation = (e) => {
                if (RTypes === undefined) {
                    fetch(Constants.ApiURL + "rooms/room-types")
                .then(response => {
                    setRoomCreationProgress(false);
                    if (!response.ok) { return undefined }
                    return response.json()
                }).then(data => {
                    console.log(data)
                    if (data !== undefined) {
                        let R = data.map(x => ({
                            key: x.rt_id,
                            text: x.rt_name,
                            value: x.rt_id
                        }))
                        console.log(R)
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

        if (RoomCreationRequest.ro_name === "") { setRegNameError("Please input a name") } else { setRegNameError(false) }
        if (RoomCreationRequest.ro_location === "") { setRegLocationError("Please specify a location") } else { setRegLocationError(false) }
        if (RoomCreationRequest.rt_id === "") { setRegTypeError("Please specify a type") } else { setRegTypeError(false) }

        if (RoomCreationRequest.ro_name === "" ||
            RoomCreationRequest.ro_location === "" ||
            RoomCreationRequest.rt_id === "") {
            setRoomCreationProgress(false)
            return;
        }

        //Build a re

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
                if (data === undefined) { return }
                if (data.ro_id === null) {
                    setRoomCreationError("Room already exists!")
                    return undefined
                }
                setOpen(false)
            })

    }

    let payload =  (             <Table singleLine>
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

    if(RoomData === undefined){
        fetch(Constants.ApiURL + "/rooms")
            .then(response => {
                if(!response.ok){
                    console.log("There has been an error getting all rooms")
                    return undefined
                }
                return response.json()
            }).then(data =>{
                console.log(data)
                if(data !== undefined){
                    setRD(data)
                }
        })

    }else{
                            payload = (
                                <div style={{ padding: '10px', margin: 'auto', width:'800px', paddingTop:'1%', backgroundColor:'lightgray'}}>
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
                            error={RoomCreationError ? RoomCreationError : regNameError} disabled={RoomCreationInProgress}
                            onChange={(e) => { setRoomCreationRequest({ ...RoomCreationRequest, "ro_name": e.target.value }) }}
                        />
                        <Form.Input
                            label='Location' placeholder='Location' required
                            error={RoomCreationError ? RoomCreationError : regLocationError} disabled={RoomCreationInProgress}
                            onChange={(e) => { setRoomCreationRequest({ ...RoomCreationRequest, "ro_location": e.target.value }) }}
                        />
                        {
                            RTypes === undefined ?
                                <Placeholder>
                                    <Placeholder.Line />
                                </Placeholder> :
                                <Form.Dropdown
                                    label="Room Type" placeholder='' required
                                    search selection options={RTypes} disabled={RoomCreationInProgress}
                                    error={RoomCreationError ? RoomCreationError : regTypeError}
                                    onChange={(event, data) => {
                                        setRoomCreationRequest({ ...RoomCreationRequest, "rt_id": data.value })
                                        console.log(data.value)
                                    }}
                                />

                        }
                        <Segment basic textAlign={"center"}>
                            <Button loading={RoomCreationInProgress} content='Create Room' primary onClick={handleSubmission} />
                        </Segment>
                    </Form>

                    <Modal.Description> <br />Developed by AMIE </Modal.Description>
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
                                          {RoomData.map((u) =>{
                                              return (
                                      <Table.Row key={u.ro_id}>
                                        <Table.Cell>{u.ro_id}</Table.Cell>
                                        <Table.Cell>{u.ro_name}</Table.Cell>
                                        <Table.Cell>{u.ro_location}</Table.Cell>
                                        <Table.Cell>{u.rt_id}</Table.Cell>
                                      </Table.Row>
                                    );
                                          })}
                                      </Table.Body>
                                  </Table>
                                    <div>
                                        <button onClick={handleRoomCreation}>Create new room</button>
                                    </div>
                                </div>

                    )
    }


    return payload

}

export default RoomManagement




