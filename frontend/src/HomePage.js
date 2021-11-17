import React, { useState } from 'react';
import { Button, Divider, Form, Grid, Header, Modal, Placeholder, Segment } from 'semantic-ui-react';
import Constants from './Constants'
import Cookies from 'universal-cookie';

const cookies = new Cookies();

function HomePage() {

    const [AuthRequest, SetAuthRequest] = useState({
        "username": "",
        "password": ""
    });

    const [registerRequest, setRegisterRequest] = useState({
        "us_name": "",
        "us_username": "",
        "us_password": "",
        "ut_id": -1
    })

    const [utypes, setUtypes] = useState(undefined)

    const [loginInProgress, setLoginInProgress] = useState(false)
    const [loginError, setLoginError] = useState(false)

    const [registrationInProgress, setRegistrationInProgress] = useState(false)
    const [registrationError, setRegistrationError] = useState(false)
    const [registrationErrorText, setRegistrationErrorText] = useState("Help! I don't know what happened!")

    const [regNameError, setRegNameError] = useState(false)
    const [regUserError, setRegUserError] = useState(false)
    const [regPassError, setRegPassError] = useState(false)
    const [regUtIdError, setRegUtIdError] = useState(false)

    const [regSuccessOpen, setRegSuccessOpen] = useState(false)
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
                    cookies.set('SessionID', data, { path: '/', maxAge: 900 }) //Have the cookie expire in 15 minutes
                    window.location.reload()
                }
            })
    }

    const handleRegister = (e) => {
        console.log(registerRequest)
        setRegistrationInProgress(true)
        setRegistrationError(false)

        //Validation

        if (registerRequest.us_name === "") { setRegNameError("Please input a name") } else { setRegNameError(false) }
        if (registerRequest.us_username === "") { setRegUserError("Please specify a Username") } else { setRegUserError(false) }
        if (registerRequest.us_password === "") { setRegPassError("Please specify a password") } else { setRegPassError(false) }
        if (registerRequest.ut_id === -1) { setRegUtIdError("Please specify a Type") } else { setRegUtIdError(false) }

        if (registerRequest.us_name === "" ||
            registerRequest.us_password === "" ||
            registerRequest.us_username === "" ||
            registerRequest.ut_id === -1) {
            setRegistrationInProgress(false)
            return;
        }

        //Build a re

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(registerRequest)
        };

        fetch(Constants.ApiURL + "users", requestOptions)
            .then(response => {
                setRegistrationInProgress(false);
                if (response.status === 500) {
                    setRegistrationError(true)
                    setRegistrationErrorText("An unknown error occurred on the server")
                }
                if (response.status !== 201) {
                    setRegUserError("User already exists!")
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data === undefined) { return }
                if (data.us_id === null) {
                    setRegUserError("User already exists!")
                    return undefined
                }
                setOpen(false)
                setRegSuccessOpen(true)
            })
    }

    const handleChange = (event, newValue) => {
        if (utypes === undefined) {
            fetch(Constants.ApiURL + "users/user-types")
                .then(response => {
                    setLoginInProgress(false);
                    if (!response.ok) { return undefined }
                    return response.json()
                }).then(data => {
                    console.log(data)
                    if (data !== undefined) {
                        var R = data.map(x => ({
                            key: x.ut_id,
                            text: x.ut_name,
                            value: x.ut_id
                        }))
                        console.log(R)
                        setUtypes(R)
                    }
                })
        }

        //Clear it because the fields automatically clear themselves
        setRegisterRequest({
            "us_name": "",
            "us_username": "",
            "us_password": "",
            "ut_id": -1
        })

        //also clear all the errors
        setRegNameError(false)
        setRegUserError(false)
        setRegPassError(false)
        setRegUtIdError(false)

        setOpen(true);
    }



    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to the AMIE Scheduling System</Header>

        <Modal
            centered={true}
            open={regSuccessOpen}
            onClose={() => setRegSuccessOpen(false)}
            onOpen={() => setRegSuccessOpen(true)}
            size="tiny"
        >
            <Modal.Header>Success!</Modal.Header>
            <Modal.Content>
                <Modal.Description>You have successfully registered onto AMIE. Please log in now</Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setRegSuccessOpen(false)}>OK</Button>
            </Modal.Actions>

        </Modal>

        <Modal
            centered={true}
            open={open}
            onClose={() => {
                registrationInProgress ? setOpen(true) :
                setOpen(false)}
            }
            onOpen={() => setOpen(true)}
            size="tiny"
        >
            <Modal.Header>Signup</Modal.Header>
            <Modal.Content>
                <Form>
                    {registrationError ? <Header textAlign="center" size="tiny">{registrationErrorText}</Header> : ""}
                    <Form.Input
                        icon='user' iconPosition='left' label='Name' placeholder='Name' required
                        error={registrationError ? registrationError : regNameError} disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_name": e.target.value }) }}
                    />
                    <Form.Input
                        icon='user' iconPosition='left' label='Username' placeholder='Username' required
                        error={registrationError ? registrationError : regUserError} disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_username": e.target.value }) }}
                    />
                    <Form.Input
                        icon='lock' iconPosition='left' label='Password' type='password' required
                        error={registrationError ? registrationError : regPassError}
                        disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_password": e.target.value }) }}
                    />
                    {
                        utypes === undefined ?
                            <Placeholder>
                                <Placeholder.Line />
                            </Placeholder> :
                            <Form.Dropdown
                                label="User Type" placeholder='' required
                                search selection options={utypes} disabled={registrationInProgress}
                                error={registrationError ? registrationError : regUtIdError}
                                onChange={(event, data) => {
                                    setRegisterRequest({ ...registerRequest, "ut_id": data.value })
                                    console.log(data.value)
                                }}
                            />

                    }
                    <Segment basic textAlign={"center"}>
                        <Button loading={registrationInProgress} content='Register' primary onClick={handleRegister} />
                    </Segment>
                </Form>

                <Modal.Description> <br />By signing up, you agree to the Terms and Conditions of AMIE </Modal.Description>
            </Modal.Content>
        </Modal>
        <Segment placeholder>

            <Grid columns={2} relaxed='very' stackable>
                <Grid.Column>
                    <Form>
                        {loginError ? <Header textAlign="center" size="tiny">Incorrect Username or Password</Header> : ""}
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
                        <Button loading={loginInProgress} content='Login' primary onClick={handleLogin} />
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
