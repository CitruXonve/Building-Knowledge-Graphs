import React, { useRef, useEffect, useScript } from 'react';
import postScribe from 'postscribe';
import { CssBaseline, Typography, Container, makeStyles, Grid, Paper, TextareaAutosize, Button } from '@material-ui/core';

const diagramStyles = {
    width: "200px",
    height: "200px",
    backgroundColor: "#DAE4E4",
  };  

export default class MinGojsSample extends React.Component{
    componentDidMount = () => {
        postScribe("#myminDiv", "<script src=\"/minGojsSample.script.js\"></script>");
    }
    render = () => {
        return (
            <Container>
                <div id="myminDiv" style={{ ...diagramStyles, backgroundColor: "#333" }}></div>
            </Container>
        )
    }
}