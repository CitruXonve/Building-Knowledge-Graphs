import React from 'react';
import ReactDOM from 'react-dom';
import Main from './Main';
import Search from './Search';
import View from './View';
import { BrowserRouter as Router, Switch, Route, Link, Redirect, useParams } from 'react-router-dom';
import { Container } from '@material-ui/core';
import $ from 'jquery';
// import history from './history';

import { createBrowserHistory } from "history";

const customHistory = createBrowserHistory({ forceRefresh: true });

const Viewer = () => {
    let { params } = useParams();
    return (<View params={params} />)
}
class App extends React.Component {

    handleResultClick = (id) => {
        customHistory.push('/view/' + id);
    }

    render = () => (
        <Switch>
            <Route path="/search">
                <Search onResultClick={this.handleResultClick} />
            </Route>
            <Route path="/test">
                <Main />
            </Route>
            <Route exact path="/">
                <Redirect to="/search" />
            </Route>
            <Route path="/view/:params">
                <Viewer />
            </Route>
        </Switch>
    )
}

ReactDOM.render(<Router history={customHistory}>
    <App />
</Router>
    , document.getElementById('root'));