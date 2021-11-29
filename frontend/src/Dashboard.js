import React, { Component, useState, Fragment } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Grid, GridColumn, Header, Modal, Placeholder, PlaceholderImage, Statistic } from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import Constants from './Constants';

function Dashboard() {

    const [data, setData] = useState([{ "name": 1, "Counts": 5 },
    { "name": 2, "Counts": 4 },
    { "name": 3, "Counts": 3 },
    { "name": 4, "Counts": 2 },
    { "name": 5, "Counts": 1 }]);

    const [BusiestHours, SetBH] = useState(undefined)
    const [BusiestUsers, SetBU] = useState(undefined)
    const [BusiestRooms, SetBR] = useState(undefined)

    //'/users/most-booked' //Busiest user
    //'/meetings/busiest' //Busiest hours
    //'/rooms/most-booked' //Busiest rooms

    if (BusiestHours === undefined) {
        fetch(Constants.ApiURL + "meetings/busiest")
            .then(response => {
                if (!response.ok) {
                    SetBH([{ "period": "00:00:00 - 00:00:00", "count": 0 }])
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    var F = data.map(x => { return { "period": x.re_starTime + " - " + x.re_endTime, count: x.count }; })
                    console.log(F)
                    SetBH(F)
                }
            })
    }

    if (BusiestUsers === undefined) {
        fetch(Constants.ApiURL + "users/most-booked")
            .then(response => {
                if (!response.ok) {
                    SetBU([{ "us_name": "?", "count": 0 }])
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    SetBU(data)
                }
            })
    }

    if (BusiestRooms === undefined) {
        fetch(Constants.ApiURL + "rooms/most-booked")
            .then(response => {
                if (!response.ok) {
                    SetBR([{ "ro_name": "?", "count": 0 }])
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    SetBR(data)
                }
            })
    }

    return <div style={{ padding: '25px' }}>
        <Header size='Huge' textAlign='center'>AMIE Global Statistics</Header>
        <Grid columns={2} stackable>
            <Grid.Column>

                <div style={{ paddingTop: '25px', height: '100%' }}>
                    <div style={{ padding: "20px", margin: 'Auto', backgroundColor: 'lightgray', width: '100%', height: '100%' }}>
                        <Grid columns={3} textAlign='center' verticalAlign='middle' style={{ display: 'flex', justifyContent: 'space-evenly', alignItems: 'center', height: '100%' }} stackable>
                            <Grid.Column>
                                <Statistic size='small'>
                                    <Statistic.Value>
                                        {
                                            BusiestHours === undefined ? <Placeholder><Placeholder.Line></Placeholder.Line></Placeholder>
                                                : <>
                                                    {BusiestHours.length === 0 ? "None" : BusiestHours[0].period}
                                                </>
                                        }
                                    </Statistic.Value>
                                    <Statistic.Label>Busiest Time Period</Statistic.Label>
                                </Statistic>
                            </Grid.Column>
                            <Grid.Column>
                                <Statistic size='small'>
                                    <Statistic.Value>
                                        {
                                            BusiestUsers === undefined ? <Placeholder><Placeholder.Line></Placeholder.Line></Placeholder>
                                                : <>
                                                    {BusiestUsers.length === 0 ? "None" : BusiestUsers[0].us_name}
                                                </>
                                        }
                                    </Statistic.Value>
                                    <Statistic.Label>Busiest User</Statistic.Label>
                                </Statistic>
                            </Grid.Column>
                            <Grid.Column>
                                <Statistic size='small'>
                                    <Statistic.Value>
                                        {
                                            BusiestRooms === undefined ? <Placeholder><Placeholder.Line></Placeholder.Line></Placeholder>
                                                : <>
                                                    {BusiestRooms.length === 0 ? "None" : BusiestRooms[0].ro_name}
                                                </>
                                        }
                                    </Statistic.Value>
                                    <Statistic.Label>Busiest Room</Statistic.Label>
                                </Statistic>
                            </Grid.Column>
                        </Grid>

                    </div>
                </div>

            </Grid.Column>
            <Grid.Column><DataDisplay data={BusiestHours} xname="period" yname="count" title="Top 5 Busiest Hours" /></Grid.Column>
            <Grid.Column><DataDisplay data={BusiestUsers} xname="us_name" yname="count" title="Top 10 Busiest Users" /></Grid.Column>
            <Grid.Column><DataDisplay data={BusiestRooms} xname="ro_name" yname="count" title="Top 10 Busiest Rooms" /></Grid.Column>
        </Grid>
    </div>


}

function DataDisplay(props) {

    return <div style={{ paddingTop: '25px' }}>
        <div style={{ padding: "20px", margin: 'Auto', backgroundColor: 'lightgray', width: '100%' }}>
            <Header textAlign='center' size='large'>{props.title}</Header>
            <Grid columns={2} style={{ padding: "20px" }} >
                <Grid.Column style={{ width: '20%' }}>
                    <Grid columns={2} textAlign='center'>
                        <Grid.Row><Grid.Column><b>{props.xname}</b></Grid.Column><Grid.Column><b>{props.yname}</b></Grid.Column></Grid.Row>
                        {props.data === undefined ? ["", "", "", "", ""].map(x => <Grid.Row><Grid.Column><Placeholder><Placeholder.Line /></Placeholder></Grid.Column><Grid.Column><Placeholder><Placeholder.Line /></Placeholder></Grid.Column></Grid.Row>) :
                            props.data.map(x => <Grid.Row><Grid.Column>{x[props.xname]}</Grid.Column><Grid.Column>{x[props.yname]}</Grid.Column></Grid.Row>)}
                    </Grid>
                </Grid.Column>
                <Grid.Column style={{ width: '80%' }}>
                    {props.data === undefined ? <Placeholder style={{ height: '100%' }}><Placeholder.Image /></Placeholder> :
                        <ResponsiveContainer>
                            <BarChart data={props.data}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey={props.xname} />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey={props.yname} fill="#8884d8" />
                            </BarChart></ResponsiveContainer>
                    }
                </Grid.Column>
            </Grid>
        </div>
    </div>
}

export default Dashboard;
