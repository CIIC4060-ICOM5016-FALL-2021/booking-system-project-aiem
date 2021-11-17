import React, { Component, useState } from 'react';
import { Button, Divider, Form, Grid, Header, Modal, Segment, Tab } from 'semantic-ui-react';
import Constants from './Constants'
import Cookies from 'universal-cookie';
import { Navigate } from 'react-router';

const cookies = new Cookies();

function HomePage() {
 
    const [AuthRequest, SetAuthRequest] = useState({
        "username": "",
        "password": ""
    });
    const [loginInProgress, setLoginInProgress] = useState(false)
    const [loginError, setLoginError] = useState(false)

    const [open, setOpen] = useState(false);

    const handleLogin = (e) => {
        console.log(AuthRequest.username)
        setLoginInProgress(true)
        setLoginError(false)

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(AuthRequest)
        };

        console.log(requestOptions.body);

        fetch(Constants.ApiURL + "Auth", requestOptions)
            .then(response => {
                setLoginInProgress(false);
                if (!response.ok) { 
                    setLoginError(true)
                    return undefined
                 }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data !== undefined) {
                    //We logged in, save a cookie, then let's get the heck out of here
                    cookies.set('SessionID', data, { path: '/', maxAge:900 }) //Have the cookie expire in 15 minutes
                    window.location.reload()
                }
            })
    }

    const handleChange = (event, newValue) => { setOpen(true); }

    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to DB Demo</Header>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>Needs changing!</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    This is a modal but it serves to show how buttons and functions can be implemented.
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Segment placeholder>

            <Grid columns={2} relaxed='very' stackable>
                <Grid.Column>
                    <Form>
                        <Form.Input
                            icon='user'
                            iconPosition='left'
                            label='Username'
                            placeholder='Username'
                            error={loginError}
                            disabled={loginInProgress}
                            onChange={(e) => { SetAuthRequest({ ...AuthRequest, "username": e.target.value }) }}
                        />
                        <Form.Input
                            icon='lock'
                            iconPosition='left'
                            label='Password'
                            type='password'
                            error={loginError}
                            disabled={loginInProgress}
                            onChange={(e) => { SetAuthRequest({ ...AuthRequest, "password": e.target.value }) }}
                        />
                        <Button content='Login' primary onClick={handleLogin} />
                    </Form>
                </Grid.Column>
                <Grid.Column verticalAlign='middle'>
                    <Button content='Sign up' icon='signup' size='big' onClick={handleChange} />
                </Grid.Column>
            </Grid>

            <Divider vertical>Or</Divider>
        </Segment>
    </Segment>
    )
}


export default HomePage;
