import React, { Component, useState, Fragment } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Grid, GridColumn, Header, Modal, Placeholder, PlaceholderImage, Statistic, Table } from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import Constants from './Constants';

function RoomManagement(){

    const [RoomData, setRD] = useState(undefined)

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

    }

    console.log("Current state value: " + RoomData)

   /* const getData = async () => {
        let data = await fetch(Constants.ApiURL + "/rooms")
        let rooms = await data.json()
        rooms.then(data => {
            setRD(data)
        })
        return rooms
    }

    const saveData = async () => {
        let jsondata = await getData();
        return jsondata
    }

    console.log(RoomData)


    const populateTable = async () => {
        let test = Promise.resolve(saveData())
        test.then(data =>{
            {data.map((u) => {

            })}
        })
    }*/

    const renderTable = (
              <Table singleLine>
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
    )

    return renderTable

}

export default RoomManagement




