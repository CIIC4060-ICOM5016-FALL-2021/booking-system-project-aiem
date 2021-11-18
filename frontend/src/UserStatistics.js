import React, { Fragment, useState } from 'react';
import { Button, Grid, Modal, Form, Segment, Placeholder, Statistic, Header, GridColumn, Divider, GridRow } from "semantic-ui-react";
import Constants from './Constants'
import { Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis, ResponsiveContainer } from "recharts";


export default function UserStatistics(props) {

    const [MostBookedRoom, SetMBR] = useState(undefined)
    const [MostBookedUser, SetMBU] = useState(undefined)


    if (props.user !== undefined && MostBookedRoom === undefined) {
        fetch(Constants.ApiURL + "users/most-rooms/" + props.user.us_id)
            .then(response => {
                if (!response.ok) {
                    SetMBR([{ "ro_name": "?", "count": 0 }])
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    SetMBR(data)
                }
            })
    }

    if (props.user !== undefined & MostBookedUser === undefined) {
        fetch(Constants.ApiURL + "users/meetings/" + props.user.us_id)
            .then(response => {
                if (!response.ok) {
                    SetMBU([{ "us_name": "?", "count": 0 }])
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    SetMBU(data)
                }
            })
    }

    return <div style={{ padding: "25px", paddingLeft: "200px", paddingRight: "200px", margin: "auto" }}>
        <Header textAlign='center' size='huge'> Statistics</Header>
        <br />
        <Grid
            columns={2}
            stackable
            centered
            textAlign='center'
        >
            <Grid.Row>
                <Grid.Column>
                    <Segment basic textAlign={"center"}>
                        <Statistic>
                            <Statistic.Value>
                                {
                                    MostBookedRoom === undefined ? <Placeholder><Placeholder.Line></Placeholder.Line></Placeholder>
                                        : <>
                                            {MostBookedRoom.length === 0 ? "None" : MostBookedRoom[0].ro_name}
                                        </>
                                }
                            </Statistic.Value>
                            <Statistic.Label>Most Booked Room</Statistic.Label>
                        </Statistic>
                    </Segment>
                </Grid.Column>
                <Grid.Column>
                    <Segment basic textAlign={"center"}>
                        <Statistic>
                            <Statistic.Value>
                                {
                                    MostBookedUser === undefined ? <Placeholder><Placeholder.Line></Placeholder.Line></Placeholder>
                                        : <>
                                            {MostBookedUser.length === 0 ? "None" : MostBookedUser[0].us_name}
                                        </>
                                }
                            </Statistic.Value>
                            <Statistic.Label>Most Booked User</Statistic.Label>
                        </Statistic>
                    </Segment>
                </Grid.Column>
                <Divider vertical />
            </Grid.Row>
            <Grid.Row>
                <Grid.Column>
                    <Grid columns={2} textAlign='center' >
                        <Grid.Row><Grid.Column><b>Room Name</b></Grid.Column><Grid.Column><b>Meeting Count</b></Grid.Column></Grid.Row>
                        {MostBookedRoom === undefined ? "" : MostBookedRoom.map(x => <Grid.Row><Grid.Column>{x.ro_name}</Grid.Column><Grid.Column>{x.count}</Grid.Column></Grid.Row>)}
                    </Grid>
                </Grid.Column>
                <Grid.Column>
                    <Grid columns={2} textAlign='center' >
                        <Grid.Row><Grid.Column><b>User Name</b></Grid.Column><Grid.Column><b>Meeting Count</b></Grid.Column></Grid.Row>
                        {MostBookedUser === undefined ? "" : MostBookedUser.map(x => <Grid.Row><Grid.Column>{x.us_name}</Grid.Column><Grid.Column>{x.count}</Grid.Column></Grid.Row>)}
                    </Grid>
                </Grid.Column>
                <Divider vertical />
            </Grid.Row>
            <Grid.Row>
                <Grid.Column>
                    <div style={{height:'300px'}}>
                    {MostBookedRoom === undefined ? "" :
                        <ResponsiveContainer>
                            <BarChart data={MostBookedRoom}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="ro_name" />
                                <YAxis /><Tooltip /> <Legend />
                                <Bar dataKey="count" fill="#5a2c8f" />
                            </BarChart>
                        </ResponsiveContainer>
                    }
                    </div>
                </Grid.Column>
                <Grid.Column>
                    {MostBookedUser === undefined ? "" :
                        <ResponsiveContainer>
                            <BarChart data={MostBookedUser} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey='us_name' />
                                <YAxis /><Tooltip /> <Legend />
                                <Bar dataKey='count' fill="#5a2c8f" />
                            </BarChart>
                        </ResponsiveContainer>
                    }
                </Grid.Column>
            </Grid.Row>
        </Grid>
    </div>

}