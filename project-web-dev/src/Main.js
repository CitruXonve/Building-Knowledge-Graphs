import React, { useRef, useEffect, useScript } from 'react';
import postScribe from 'postscribe';
import { CssBaseline, Typography, Container, makeStyles, Grid, Paper, TextareaAutosize, Button } from '@material-ui/core';
import FullWidthGrid from './FullWidthGrid';
import ContainedButtons from './ContainedButtons';
import * as go from "gojs";
import regroupingController from './regrouping'
// import Dashboard from './Dashboard';

const diagramStyles = {
  width: "800px",
  height: "600px",
  backgroundColor: "#DAE4E4",
};

const gridStyles = {
  root: {
    flexGrow: 1,
    padding: '24px',
    backgroundColor: '#333',
  },
  paper: {
    border: 0,
    borderRadius: 3,
    color: 'white',
    padding: '10px 10px',
    textAlign: 'center',
    backgroundColor: '#424242',
  },
};

const buttonStyles = {
    root: {
      color: "#fff",
      padding: "6px 16px",
      fontSize: "0.875rem",
      minWidth: "64px",
      boxSizing: "border-box",
      transition: "background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,border 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms",
      fontFamily: "\Roboto\", \"Helvetica\", \"Arial\", sans-serif",
      fontWeight: "500",
      lineHeight: "1.75",
      borderRadius: "4px",
      letterSpacing: "0.02857em",
      textTransform: "uppercase",
    },
    primary: {
      color: "rgba(0, 0, 0, 0.87)",
      backgroundColor: "#90caf9",
    },
    secondary: {
      color: "rgba(0, 0, 0, 0.87)",
      backgroundColor: "#f48fb1",
    },
    contained: {
      color: "rgba(0, 0, 0, 0.87)",
      boxShadow: "0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12)",
      backgroundColor: "#e0e0e0",
    },
    outlined: {
      border: "1px solid rgba(255, 255, 255, 0.23)",
      padding: "5px 15px",
    }
}

export default class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      regroupingText: ""
    }
    this.handleRegroupingDataChange = this.handleRegroupingDataChange.bind(this);
    this.loadRegroupingContent = this.loadRegroupingContent.bind(this)
  }

  scriptLoaded() {
  }

  loadScriptAsync = (src) => {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = () => this.scriptLoaded();
    document.body.appendChild(script);
  }

  loadScriptSync = (src) => {
    const script = document.createElement("script");
    script.src = src;
    script.async = false;
    script.onload = () => this.scriptLoaded();
    document.body.appendChild(script);
  }

  componentDidMount = () => {
    // this.loadScriptSync("https://unpkg.com/gojs/release/go-debug.js");
    // this.loadScriptSync("/myDiagramDiv.script.js");
    postScribe("#myDiagramDiv", "<script src=\"/myDiagramDiv.script.js\"></script>")
    postScribe("#myminDiv", "<script src=\"/minGojsSample.script.js\"></script>")
    // postScribe('#myRegroupingDiagram', "<script src=\"/regrouping.script.js\"></script>", {
    //   done: function () {
    //     console.info('Regrouping diagram loaded.');
    //   }
    // })
    this.loadRegroupingContent();
  }

  loadRegroupingContent = () => {
    fetch('/initRegroupingData.js').then(
      response => response.text()
    ).then(
      text => {
        console.log(text);
        this.setState({regroupingText: text})
      }
    ).then(
      () => {
        regroupingController.init();
        console.info("Regrouping data loaded")
      }
    )
  }

  handleRegroupingDataChange(event) {
    this.setState({regroupingText: event.target.value});
    console.log(event.target.value, this.state);
  }

  FormRow = () => {
    return (
      <React.Fragment>
        <Grid item style={{visibility: "hidden"}}>
          <Paper style={gridStyles.paper}>
            <div id="myPaletteDiv" style={{ width: "100%", height: '300px', marginRight: "2px", backgroundColor: "whitesmoke", border: "solid 1px black" }}></div>
          </Paper>
        </Grid>
        <Grid item md={12}>
          <Paper style={gridStyles.paper}>
            <div id="myRegroupingDiagram" style={{ width: '100%', height: '300px' }}></div>
          </Paper>
        </Grid>
        <Grid item md={4}>
          <Paper style={gridStyles.paper}>
            <TextareaAutosize id="mySavedModel" style={{ width: '100%', height: '300px'}} onChange={this.handleRegroupingDataChange} value={this.state.regroupingText}/>
            <Button style={{...buttonStyles.contained, ...buttonStyles.primary}} onClick={regroupingController.load}>
              Load
            </Button>
            <Button variant="outlined" color="secondary" onClick={regroupingController.save}>
              Extract
            </Button>
          </Paper>
        </Grid>
      </React.Fragment>
    )
  }

  render() {
    return (
      <React.Fragment>


        <CssBaseline />
        <Container maxWidth="lg">
          <Typography component="div" style={{ backgroundColor: '#cfe8fc', height: '100vh' }}>
            <Container>
              <ContainedButtons />
            </Container>
            <Container style={{...buttonStyles.root, ...gridStyles.root}}>
              <Grid container spacing={1}>
                <Grid container item xs={12} spacing={3}>
                  <this.FormRow />
                </Grid>
              </Grid>
            </Container>
            <Container>
              <div id="myminDiv" style={{ ...diagramStyles, backgroundColor: "#333" }}></div>
            </Container>
            <div className="container">
              <h1>Helloworld React!</h1>
              Loading script
              <div id="myDiagramDiv" style={diagramStyles}></div>
            </div>
            <FullWidthGrid />
          </Typography>>
        </Container>

      </React.Fragment>
    );
  }
}