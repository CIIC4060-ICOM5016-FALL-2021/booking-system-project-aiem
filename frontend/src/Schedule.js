import React, {Children, useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Container} from "semantic-ui-react";
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
        if(event.title === 'Unavailable'){
            title = event.title;
            description = '';
            reservation = 'Reserved by: ' + event.desc.Creator;
        }
        return (
            <span>
              <strong>{title}</strong>
                    <div class="text--wrap">
                        <p>{description}</p>
                        <p>{reservation}</p>
                    </div>
            </span>
        )
    }

    return <Container style={{height: 800}}><Calendar
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
