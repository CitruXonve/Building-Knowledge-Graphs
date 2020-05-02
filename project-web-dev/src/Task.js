import React, { Component, Fragment } from 'react';
import { CssBaseline, Typography, Container, Grid, Paper } from '@material-ui/core';
import regroupingController from './regrouping';
import { gridStyles, buttonStyles, innerStyles } from './styles';

class Task extends Component {
    constructor(props) {
        super(props);
        this.state = {

        }
        this.loadRegroupingContent = this.loadRegroupingContent.bind(this)
        this.handleDiagramChange = this.handleDiagramChange.bind(this)
    }

    exportDiagram2DisplayText(data) {
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
        // console.log(JSON.stringify(key2id), JSON.stringify(children), output)
        // this.setState({ plannerText: output })
        return output;
    }

    handleDiagramChange(event) {
        if (event.isTransactionFinished) {
            this.setState({ regroupingText: event.model.toJson() });
            // console.log(event.model.toJson());
            const new_displayText = this.exportDiagram2DisplayText(event.model)
            this.setState({ displayText: new_displayText });
        }
    }

    loadRegroupingContent = (text) => {
        if (text !== undefined && text !== null) {
            // const diagram = regroupingController.init("myRegroupingDiagram", text, this.handleDiagramChange, false);
            this.setState({ regroupingDiagram: regroupingController.init("myRegroupingDiagram", text, this.handleDiagramChange, false) })
            console.log("Regrouping data loaded")
        }
        else {
            console.log("error loading regrouping" + text)
        }
        // return null
    }


    componentDidMount = () => {
        this.loadRegroupingContent(this.props.regroupingText);
        console.info("mount" + this.props.regroupingText)
    }

    componentDidUpdate = () => {
        if (!this.state.regroupingDiagram) {
            this.loadRegroupingContent(this.props.regroupingText)
            // console.info("first update" + this.props.regroupingText)
        }
    }

    render = () => {
        // console.log(JSON.stringify(this.props))
        return (
            <Fragment>
                {/* <p>{JSON.stringify(this.props)}</p> */}
                <CssBaseline />
                <Container maxWidth="lg">
                    <Typography component="div" style={{ backgroundColor: '#cfe8fc', height: '100vh', fontSize: "initial" }}>
                        <Container style={{ ...buttonStyles.root, ...gridStyles.root }}>
                            <Grid container spacing={3}>
                                <Grid item md={12}>
                                    <h2> Click & drag to make your plan: </h2>
                                    <Paper style={gridStyles.paper}>
                                        <div id="myRegroupingDiagram" style={{ width: '100%', height: '300px' }}></div>
                                    </Paper>
                                    <div>
                                        <span>{this.state.displayText ?
                                            this.state.displayText.split('\n').map(
                                                (text, index) => {
                                                    var formatted = text.replace('\t', '\u00a0\u00a0')
                                                    var matched = formatted.match(/^\s*([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g)
                                                    return (<React.Fragment key={`${text}-${index}`}>
                                                        {/* {text.match(/\t/g) ? text.match(/\t/g).map(() => '&nbsp;') : null} */}
                                                        {
                                                            matched ? (<a href={"/view/" + matched[0]} target="_blank">{formatted}</a>) : formatted
                                                        }
                                                        <br />
                                                    </React.Fragment>)
                                                }
                                            )
                                            : null}</span>
                                    </div>

                                    <Paper style={{ ...buttonStyles.root, ...innerStyles.paper, ...innerStyles.coolPaper }} onClick={() => print()}>
                                        <h2>
                                            Download your plan
                                        </h2>
                                    </Paper>
                                </Grid>
                            </Grid>
                        </Container>
                    </Typography>
                </Container>
            </Fragment>)
    }
}
export default Task;