import React from 'react';
import { Container, Grid, Paper } from '@material-ui/core';
import regroupingController from './regrouping';

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
        backgroundColor: '#F1F1F1',
    },
};

const buttonStyles = {
    root: {
        color: "#fff",
        padding: "6px 16px",
        // fontSize: "0.875rem",
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

const innerStyles = {
    root: {
        flexGrow: 1,
        padding: '24px',
        backgroundColor: '#333',
    },
    paper: {
        border: 0,
        borderRadius: 3,
        color: 'white',
        height: 48,
        padding: '0 30px',
        textAlign: 'center',
        backgroundColor: '#424242',
    },
    warmPaper: {
        background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
        boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
    },
    coolPaper: {
        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
        boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
    }
}

const loadRegroupingContentFromTest = () => {
    fetch('/initRegroupingData.js').then(
        response => response.text()
    ).then(
        text => {
            // console.log(text);
            this.setState({ regroupingText: text })
            // this.state.regroupingText = text
        }
    ).then(
        () => {
            this.setState({ regroupingDiagram: regroupingController.init("myRegroupingDiagram", this.state.regroupingText, this.handleDiagramChange, false) });
            console.info("Regrouping data loaded")
            this.exportDiagram2Text(regroupingController.extract(this.state.regroupingDiagram))
        }
    )
}

var regroupingDiagram = null;
var regroupingText = null;
var plannerText = null;

const loadRegroupingContent = (data, onChange) => {
    regroupingDiagram = regroupingController.init("myRegroupingDiagram", data, onChange, false);
    console.info("Regrouping data loaded")
    // return exportDiagram2Text(regroupingController.extract(regroupingDiagram))
}

const exportDiagram2Text = (data) => {
    // const result = data["nodeDataArray"].map(item => item.text);
    // data["nodeDataArray"].forEach(item => console.log(item.key, item.text, item.group, item.key, item.isGroup, item.category));
    var key2id = Object()
    var cnt = 0;
    var children = Object()
    var dict_text = Object()
    for (var key in data["nodeDataArray"]) {
        const item = data["nodeDataArray"][key]
        key2id[item.key] = cnt;
        dict_text[cnt] = item.text
        // console.log(key, item.key, item.text, item.group, item.key, item.isGroup, item.category);
        cnt++;
    }
    for (var key in data["nodeDataArray"]) {
        const item = data["nodeDataArray"][key]
        if ("group" in item) {
            const parent = key2id[item.group]
            var child_list = parent in children ? children[parent] : Array();
            child_list.push(key2id[item.key]);
            children[parent] = child_list;
        }
    }
    function traverse(id) {
        if (id in children) {
            var result = [];
            result = result.concat(children[id].map(traverse))
            return dict_text[id] + '\n' + result.map(str => '\t' + str).join('\n')
        }
        else
            return dict_text[id]
    }
    /*
    for (var key in data["linkDataArray"]){
        const from = key2id[data["linkDataArray"][key].from]
        const to = key2id[data["linkDataArray"][key].to]
        
    }*/
    // this.state.plannerText = result
    var output = traverse(0);
    console.log(JSON.stringify(key2id), JSON.stringify(children), output)
    return output;
}

const FormRow = () => {
    return (
        <React.Fragment>
            <Grid item md={12}>
                <Paper style={gridStyles.paper}>
                    <div id="myRegroupingDiagram" style={{ width: '100%', height: '300px' }}></div>
                </Paper>
            </Grid>
        </React.Fragment>
    )
}

const methods = {
    componentDidMount(props) {
      console.log('I mounted! Here are my props: ', props);
      
    }
  };

const ProgramView = props => {

    const regrouping = props.regroupingText;
    const handleChange = props.onChange;

    const displayText = loadRegroupingContent(regrouping, handleChange);
    // const displayText = null;

    // console.log("draw program graph by+"+JSON.stringify(handleChange))

    return (
        <React.Fragment>
            <Grid container spacing={1}>
                <Grid container item xs={12} spacing={3}>
                    <FormRow />
                </Grid>
            </Grid>
            <Grid container spacing={1}>
                <Grid container item xs={12} spacing={3} id="planner">
                    {displayText ? displayText.split('\n').map(
                        (text, index) => (<React.Fragment key={`${text}-${index}`}>
                            {/* {text.match(/\t/g) ? text.match(/\t/g).map(() => '&nbsp;') : null} */}
                            {text.replace('\t', '\u00a0\u00a0')}
                            <br />
                        </React.Fragment>)
                    ) : null}
                </Grid>
            </Grid>
        </React.Fragment>
    )
}

export default ProgramView;