import React, { Fragment, useState } from 'react';
import { Button, Grid, Modal, Form, Segment, Placeholder} from "semantic-ui-react";
import Constants from './Constants'
import Cookies from 'universal-cookie';


const colors = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'grey', 'black']

export default function AccountManagement(props) {

    const [registerRequest, setRegisterRequest] = useState({
        "us_name": "",
        "us_username": "",
        "us_password": "",
        "ut_id": -1
    })

    const [registrationInProgress, setRegistrationInProgress] = useState(false)
    const [registrationError, setRegistrationError] = useState(false)
    const [registrationErrorText, setRegistrationErrorText] = useState("Help! I don't know what happened!")

    const [regSuccessOpen, setRegSuccessOpen] = useState(false)

    const [deletePromptOpen, setDelPromptOpen] = useState(false)
    const [deleteInProgress, setDelInProgress] = useState(false)

    const [deleteResult, setDelResult] = useState({
        "Open": false,
        "Reason": ""
    })

    const [deleteResultSuccess, setDelResultSuccess] = useState(false)


    const handleRegister = (e) => {
        console.log(registerRequest)
        setRegistrationInProgress(true)
        setRegistrationError(false)

        //Validation
        var UpdateUser = {
            "us_name": registerRequest.us_name === "" ? props.user.us_name : registerRequest.us_name,
            "us_username": registerRequest.us_username === "" ? props.user.us_username : registerRequest.us_username,
            "us_password": registerRequest.us_password === "" ? props.user.us_password : registerRequest.us_password,
            "ut_id": props.user.ut_id
        }

        //Build a re
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(UpdateUser)
        };

        fetch(Constants.ApiURL + "users/" + props.user.us_id, requestOptions)
            .then(response => {
                setRegistrationInProgress(false);
                if (!response.ok) {
                    setRegistrationError(true)
                    setRegistrationErrorText("An unknown error occurred on the server")
                    return undefined
                }
                return response.json()
            }).then(data => {
                console.log(data)
                if (data === undefined) { return }
                setRegSuccessOpen(true)
            })
    }

    const handleRegularLogout = (e) => {
        console.log("OK, Time to leave")
        new Cookies().remove("SessionID")
        window.location.reload()
        console.log("Oops we're really screwed now")
    }

    const handleDelete = (e) => {
        console.log("oh boy")
        setDelInProgress(true)
        console.log(registerRequest)

        //Build a re
        const requestOptions = { method: 'DELETE' };

        fetch(Constants.ApiURL + "users/" + props.user.us_id, requestOptions)
            .then(response => {
                setRegistrationInProgress(false);
                setDelResultSuccess(response.ok)
                console.log(response)
                return response, response.json()
            }).then((response, data) => {
                console.log(data)
                setDelPromptOpen(false)
                setDelResult({...deleteResult,"Open" : true, "Reason" : data})
            })
            
    }

    return <Fragment>

        <Modal
            centered={true}
            open={deleteResult.Open}
            onClose={deleteResultSuccess ? (e) => setDelPromptOpen(false) : (e) => {
                console.log(deleteResult)
                setDelResult({ ...deleteResult, "Open": false })}}
            size="tiny"
            dimmer='blurring'
        >
            <Modal.Header>{deleteResultSuccess ? "Your account has been deleted" : "An error occured while deleting your account"}</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    {deleteResultSuccess ? 
                    <p>Your account has been successfully deleted. We are a bit sad to see you go, but you know, such is life. You can log out with the button below</p>
                    :
                    <p>Yur account wasn't deleted, because something happened. Here is some information that may help:<br/><br/>{deleteResult.Reason}</p>
                }
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                {deleteResultSuccess ? <Button color='red' onClick={handleRegularLogout}>Adiosito</Button>
                    : <Button primary onClick={() => setDelResult({ ...deleteResult, "Open": false })}>Ok</Button>
                }

            </Modal.Actions>
        </Modal>

        <Modal
            open={deletePromptOpen}
            size='small'
            onClose={deleteInProgress ? (e) => setDelPromptOpen(true) : (e) => setDelPromptOpen(false)}
        >
            <Modal.Header>Delete Your Account</Modal.Header>
            <Modal.Content>
                {deleteInProgress ?
                    <p>It is too late now. Your account is being deleted. Please wait</p>
                    : <p>This is a Permanent operation. Along with deleting yourself, you will also delete all meetings you have reserved (past, present, and future),
                        and remove yourself from any meetings you have or will attend. There is also a non-zero chance that you will delete yourself in another random database app accidentally,
                        and do you really want to risk that?<br /> <br /> Again, <b>this is permanent!</b> Maybe think about this before saying yes</p>
                }
            </Modal.Content>
            <Modal.Actions>
                {
                    deleteInProgress ? "" : <>
                        <Button onClick={(e) => setDelPromptOpen(false)} negative icon='cancel' content='No' />
                        <Button onClick={handleDelete} positive icon='trash' content='Yes' /></>

                }
            </Modal.Actions>
        </Modal>
        <br /><br /><br />
        <Grid
            verticalAlign='middle'
            columns='3'
            stackable
            centered
            padded
            relaxed='very'
        >
            <Grid.Row color='grey'><Grid.Column>
                {
                    props.user === undefined ? <Placeholder><Placeholder.Line /></Placeholder> :
                        <h1> {props.user.us_name} ({props.user.us_username})</h1>
                }

            </Grid.Column></Grid.Row>
            <Grid.Row>
                {
                    props.userType === undefined ? <Grid.Column color='grey'><Placeholder><Placeholder.Line /></Placeholder></Grid.Column>
                        : <Grid.Column color={colors[props.userType.ut_level % colors.length]}><b>{props.userType.ut_name} : {props.userType.ut_isAdmin ? "Administrator " : "Power Level " + props.userType.ut_level}</b></Grid.Column>
                }
            </Grid.Row>
            <Grid.Column width={5}><Segment basic textAlign={"center"}>
                <Button disabled={registrationInProgress} primary icon='logout' content='Logout' onClick={handleRegularLogout} />
            </Segment></Grid.Column>
            <Grid.Row><Grid.Column>
                <h4>
                    Account Management
                </h4>
                The following section will allow you to update your account's details. Leaving any of these fields blank will leave them unchanged <br /><br />
                <Form>
                    <Form.Input
                        icon='user' iconPosition='left' label='Name' placeholder='Name' disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_name": e.target.value }) }}
                    />
                    <Form.Input
                        icon='user' iconPosition='left' label='Username' placeholder='Username' disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_username": e.target.value }) }}
                    />
                    <Form.Input
                        icon='lock' iconPosition='left' label='Password' type='password' disabled={registrationInProgress}
                        onChange={(e) => { setRegisterRequest({ ...registerRequest, "us_password": e.target.value }) }}
                    />
                </Form>
            </Grid.Column></Grid.Row>
            {regSuccessOpen ? <Grid.Row><Grid.Column color='green'><b>Details successfully updated!</b></Grid.Column></Grid.Row> : ""}
            {registrationError ? <Grid.Row><Grid.Column color='red'> <b>Error: {registrationErrorText}</b> </Grid.Column></Grid.Row> : ""}
            <Grid.Row><Grid.Column>
                <Grid
                    columns={2}
                    stackable
                    centered
                    textAlign='center'

                >
                    <Grid.Column><Segment basic textAlign={"center"}>
                        <Button loading={registrationInProgress} primary content='Update User Details' onClick={handleRegister} />
                    </Segment></Grid.Column>
                    <Grid.Column><Segment basic textAlign={"center"}>
                        <Button disabled={registrationInProgress} secondary icon='trash' content='Delete Account' onClick={(e) => { setDelPromptOpen(true) }} />
                    </Segment></Grid.Column>
                </Grid>
            </Grid.Column></Grid.Row>
        </Grid>
    </Fragment >

}
