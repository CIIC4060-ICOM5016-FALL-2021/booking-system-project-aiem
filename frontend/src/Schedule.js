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
                        desc: ' Room: ' + event.room + ' Description: ' + event.desc + ' Reserved by: ' + event.creator + ' (' + event.username + ')',
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
                        desc: ': ' + event.desc,
                        start: new Date(event.date + ' ' + event.start),
                        end: new Date(event.date + ' ' + event.end),
                        allDay: false
                    }))
                    setDates(events)
                }
            })
        }
    }, []);

    const EventWrapper = ({event, children}) =>
        React.cloneElement(Children.only(children), {
            style: {
                ...children.style,
                backgroundColor: event.title === 'Unavailable' ? 'crimson' : 'steelblue',
            },
        });

    function Event({event}) {
        return (
            <span>
          <strong>{event.title}</strong>
                {event.desc}
        </span>
        )
    }

    return <Container style={{height: 800}}><Calendar
        localizer={localizer}
        components={{
            eventWrapper: EventWrapper,
            event: Event
        }}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={['month', 'day']}
        defaultDate={Date.now()}
    >

    </Calendar>
    </Container>


}
