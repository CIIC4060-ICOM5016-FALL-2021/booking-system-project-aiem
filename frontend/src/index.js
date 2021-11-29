import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Route, BrowserRouter, Routes, Navigate} from 'react-router-dom';
import HomePage from "./HomePage";
import BookMeeting from "./BookMeeting";
import 'semantic-ui-css/semantic.min.css'
import UserView from "./UserView";
import Dashboard from "./Dashboard";
import Cookies from 'universal-cookie';

const cookies = new Cookies();

ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route exact path ="/" element = {<Navigate to="/Home"/>}/>
            <Route exact path="/Home" element={cookies.get("SessionID")!==undefined ? <Navigate to='/UserView'/> : <HomePage/>} />
            <Route exact path="/UserView" element={cookies.get("SessionID")===undefined ? <Navigate to='/Home'/> : <UserView/>} />
            <Route exact path="/Dashboard" element={cookies.get("SessionID")===undefined ? <Navigate to='/Home'/> : <Dashboard/>} />
        </Routes>
    </BrowserRouter>,
    document.getElementById('root')
);
