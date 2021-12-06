import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Form, Modal, Segment} from "semantic-ui-react";
import Constants from "./Constants";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


export default function Schedule(props) {
    const [dates, setDates] = useState(undefined);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    const [reservationState, setReservation] = useState(undefined)
    const [titleState, setTitle] = useState(undefined)
    const [descriptionState, setDescription] = useState(undefined)

    const closeWindow = (e) => {
        setOpen(false)
    }

    const openWindow = (e) => {

        setOpen(true)

        if (e.title === 'Unavailable') {
            setTitle(e.title)
            setDescription('')
            setReservation('Reserved by: ' + e.desc.Creator)
        }

        setTitle(e.title)
        setDescription('Description: ' + e.desc.Description)
        setReservation('Reserved by: ' + e.desc.Creator + ' (' + e.desc.Username + ')')
        console.log("Value of title: " + e.title)
        console.log("Description: " + e.desc.Description)
        console.log("Reserved by: " + e.desc.Creator)
        console.log("Value of open: " + open)

    }

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
                            'Username': event.username
                        },
                        start: new Date(event.date + ' ' + event.start),
                        end: new Date(event.date + ' ' + event.end),
                        allDay: false
                    }))
                    setDates(events)
                }
            })
        } else {
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
    }, []);

    function EventPropGetter(event, start, end, isSelected) {
        return {
            style: {backgroundColor: event.title === 'Unavailable' ? 'crimson' : 'steelblue'}
        }
    }

    function Event({event}) {
        let title = event.title + ' - Room: ' + event.desc.Room;
        let description = 'Description: ' + event.desc.Description;
        let reservation = 'Reserved by: ' + event.desc.Creator + ' (' + event.desc.Username + ')';
        if (event.title === 'Unavailable') {
            title = event.title;
            description = '';
            reservation = 'Reserved by: ' + event.desc.Creator;
        }
        return (
            <span>
              <strong>{title}</strong>
                    <div class="text--wrap" onClick={openWindow.bind(this, event)}>
                        <p>{description}</p>
                        <p>{reservation}</p>
                    </div>
                <Modal
                    centered={true}
                    open={open}
                    onOpen={() => setOpen(true)}
                    size="tiny"
                >
                    <Modal.Header><strong>{titleState}</strong></Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <p>{descriptionState}</p>
                            <p>{reservationState}</p>
                        </Modal.Description>
                        <Form>
                            <Segment basic textAlign={"center"}>
                                <Button className='ui button ' content='Close' onClick={closeWindow}/>
                            </Segment>
                        </Form>
                        <Modal.Description> <br/>Developed by AMIE </Modal.Description>
                    </Modal.Content>
                </Modal>
            </span>

        )
    }

    return <Container style={{height: 1000}}><Calendar
        localizer={localizer}
        components={{event: Event}}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={['month', 'day']}
        defaultDate={Date.now()}
        eventPropGetter={EventPropGetter}
    >

    </Calendar>
    </Container>


}
