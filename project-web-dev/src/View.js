import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { CssBaseline, Typography, Container, Grid, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import Task from './Task';
// import FullWidthGrid from './FullWidthGrid';
import { gridStyles, buttonStyles, innerStyles } from './styles';
import { makeStyles } from '@material-ui/core';

function createData(name, calories, fat, carbs, protein) {
    return { name, calories, fat, carbs, protein };
}

const rows = [
    createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
    createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
    createData('Eclair', 262, 16.0, 24, 6.0),
    createData('Cupcake', 305, 3.7, 67, 4.3),
    createData('Gingerbread', 356, 16.0, 49, 3.9),
];

export default class View extends React.Component {

    constructor(props) {
        super(props)
        this.constructDiagram = this.constructDiagram.bind(this)
    }

    state = {
        plannerText: null,
        plannerObj: null,
        regroupingText: null,
        fetched: {
            description: null,
        },
        dataList: require('../public/USC_catalogue_KG.json').concat(require('../public/USC_catalogue_KG_2.json')),
    }

    constructDiagram = (data) => {

        // var cnt = -1
        let nodeArray = []

        function parseNode(data, parent) {
            // console.log("parse", data, parent, typeof (data), Array.isArray(data))
            // cnt += 1
            if (typeof (data) === 'string') {
                try {
                    data = JSON.parse(data)
                } catch (error) {
                    // console.log("Error: ", error, data)
                } finally {
                    try {

                        if (typeof (data) === 'string' && (data.match(/([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g))) {
                            // cnt += 1
                            nodeArray.push(parent >= 0 ? {
                                key: nodeArray.length, text: data,
                                group: parent
                            } : {
                                    key: nodeArray.length, text: data,
                                }
                            )
                            return
                        }
                    } catch (error) {
                        console.log("Error: ", error, data)
                    } finally {

                    }
                }
            }
            // console.log("continue parse")
            if (Array.isArray(data)) {
                // console.log("parse array")
                var group = nodeArray.length
                var arr = data.map((item) => parseNode(item, group - 1))
                // console.log("parse array",data, parent, data.map(item => parseNode(item, cnt)))
                return
            }
            else if (typeof (data) === 'object') {
                // cnt += 1
                var group = nodeArray.length
                var desc = ""
                // console.log("parse object", data)
                nodeArray.push(parent >= 0 ? {
                    key: nodeArray.length, text: desc, isGroup: true, group: parent,
                    category: "OfNodes"
                } : {
                        key: nodeArray.length, text: desc, isGroup: true,
                        category: "OfGroups"
                    })
                for (const key in data) {
                    desc += key
                    // console.log("parse object", key, typeof(key), data[key], cnt )
                    parseNode(data[key], group - 1)
                }
                nodeArray[group].text = desc
                // console.log("parse object", data, parent, arr.concat({
                // key: cnt, text: data, isGroup: true, group: parent >=0 ? parent : null,
                // category: parent >= 0 ? "OfNodes" : "OfGroups"
                // }))
                // console.log(arr, {
                //     key: cnt, text: data, isGroup: true, group: parent >=0 ? parent : null,
                //     category: parent >= 0 ? "OfNodes" : "OfGroups"
                // })
                return
            }
            else {
                try {
                    if (data.match(/([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g)) {
                        // cnt += 1
                        nodeArray.push(parent >= 0 ? {
                            key: nodeArray.length, text: data,
                            group: parent
                        } : {
                                key: nodeArray.length, text: data,
                            })
                        return
                    }
                } catch (error) {
                    console.log("Error: ", error, data)
                } finally {

                }
            }
        }

        let root = data.course.raw
        // console.log("construct+", root)

        parseNode(root, -1)

        let children_cnt = {}
        for (var i = 0; i < nodeArray.length; i++) {
            const parent = nodeArray[i].group
            if (parent !== undefined && parent !== null) {
                if (parent in children_cnt) {
                    children_cnt[parent] = children_cnt[parent] + 1
                }
                else {
                    children_cnt[parent] = 1
                }
            }
        }

        let num_to_remove = 0
        while (!(nodeArray[num_to_remove].key in children_cnt) || children_cnt[num_to_remove] < 1) {
            num_to_remove += 1
        }
        nodeArray = nodeArray.slice(num_to_remove)

        const diagramObj = {
            "class": "go.GraphLinksModel",
            "nodeDataArray": nodeArray,
            "linkDataArray": []
        }
        console.log("constructed ", diagramObj, children_cnt)
        // nodeArray.forEach(line => console.log(line))
        this.setState({ regroupingText: JSON.stringify(diagramObj) })
        /*
        fetch('/initRegroupingData.js').then(
            response => response.text()
        ).then(
            text => {
                this.setState({ regroupingText: text })
                // this.state.regroupingText = text;
                // console.log("fetched"+this.state.regroupingText);
                // this.state.regroupingText = text
            }
        );*/
    }

    componentDidMount() {
        const keyword = this.props.params
        if (keyword.match(/^doc\-/g)) {
            const id = keyword; // query search engine
            fetch("http://localhost:3002/api/as/v1/engines/inf558/search.json", {
                headers: { "authorization": "Bearer search-weg5x9xous972kvpsjr7ncbc", 'Content-Type': 'application/json' },
                method: 'POST',
                body: '{"id": {"type": "value"}, "page": {"size": 1, "current": 1}, "query": "' + id + '"}'
            }).then(response => response.json())
                .then(
                    response => {
                        // console.log(response.results)
                        if (response.results && response.results[0]) {
                            // console.log(JSON.stringify(response.results[0]));
                            this.setState({ plannerText: JSON.stringify(response.results[0]) })
                            this.setState({ plannerObj: response.results[0] })
                            return response.results[0]
                        }
                        else {
                            console.log("Null response " + id + '\n' + JSON.stringify(response))
                        }
                    }
                ).then(result => {
                    this.constructDiagram(result)
                    // console.log("Constructed diagram+" + JSON.stringify(result) + '\n' + JSON.stringify(this.state.regroupingText))
                })
                .catch(
                    (response) => {
                        console.log("Fail to retrieve ID " + id + '\n' + response)
                    }
                );
        }
        if (keyword.match(/([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g)) {
            const abbr1 = keyword.match(/([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g)[0].match(/[A-Z]{2,4}/g)[0]
            const abbr2 = keyword.match(/([A-Z]{2,4}\s*[0-9]{3}[A-Za-z]{0,2})/g)[0].match(/[0-9]+[A-Za-z]{0,2}/g)[0]
            // alert("receive course query + "+abbr1+abbr2)
            var query = "query=PREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0Aprefix+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0APREFIX+cs%3A+%3Chttp%3A%2F%2Finf558.org%2Fcourse%23%3E%0A%0Aselect+DISTINCT+%3Fdesc+%3Ftitle+%3Funit%0Awhere+%7B+%0A++%3Fs+%3Fp+%3Fdesc+%3B%0A+++++foaf%3Aname+%3Ftitle+%3B%0A+++++cs%3Ahas_unit+%3Funit+.%0A++FILTER+regex(%3Fdesc%2C+'%5E%5C%5Cs*" + abbr1 + "." + abbr2 + "'%2C+'i')%0A%7D%0ALIMIT+10"

            fetch("http://localhost:3030/usc/sparql", {
                headers: { "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" },
                method: "POST",
                body: query,
            }).then(
                response => response.json()
            ).then(
                data => {
                    const obj = data.results.bindings[0]
                    this.state.fetched = {
                        description: obj.desc.value,
                        title: obj.title.value,
                        unit: obj.unit.value,
                        type: "course",
                    }
                    console.log(this.state.fetched)
                    this.forceUpdate()
                }
                ).catch(
                    data => {
                        console.log("query failed: "+ data)
                        for (const key in this.state.dataList){
                            const item = this.state.dataList[key];
                            if (item.type === 'course' && item.title.match(abbr1+" "+abbr2)){
                                this.state.fetched = {
                                    description: item.description,
                                    title: item.title,
                                    unit: item.description.match(/Unit:\s*[0-9]{1,2}/g) ? item.description.match(/Unit:\s*[0-9]{1,2}/g)[0]: null,
                                    type: 'course',
                                }
                            }
                        }
                        this.forceUpdate()
                }
            )

            query = "query=PREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0Aprefix+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0Aprefix+dbpprop%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0APREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0APREFIX+lmdb%3A+%3Chttp%3A%2F%2Fdata.linkedmdb.org%2Fmovie%2F%3E%0APREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E+%0APREFIX+cs%3A+%3Chttp%3A%2F%2Finf558.org%2Fcourse%23%3E%0A%0Aselect+DISTINCT+%3Fobject+%3Furl+%3Flevel%0Awhere+%7B+%0A++%3Fs+%3Fp+%3Fdesc+%3B%0A+++++cs%3Asimilar_to+%5B+foaf%3Aname+%3Fobject%3B+cs%3Aprovenance_url+%3Furl%3B+cs%3Alevel+%3Flevel%5D+%3B%0A+++++foaf%3Aname+%3Fname+.%0A++FILTER+regex(%3Fdesc%2C+'%5E%5C%5Cs*" + abbr1 + "." + abbr2 + "'%2C+'i')%0A%7D%0ALIMIT+10"

            fetch("http://localhost:3030/usc/sparql", {
                headers: { "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" },
                method: "POST",
                body: query,
            }).then(
                response => response.json()
            ).then(
                data => {
                    const obj = data.results.bindings.map(item => ({ "level": item.level.value, "title": item.object.value, "url": item.url.value }));
                    this.setState({ remote: obj })
                    console.log(this.state.remote)
                    this.forceUpdate()
                }
                ).catch(
                    data => {
                        console.log("query failed: "+ data)
                        this.forceUpdate()
                }
            )
        }
    }

    render = () => {

        // const useStyles = makeStyles({
        //     text: {
        //         fontSize: 'initial',
        //     }
        // })

        // const classes = useStyles();

        return (

            <React.Fragment>
                {/* <AsyncComponent id="main"/> */}
                {this.state.plannerObj && this.state.plannerObj.type && this.state.plannerObj.type.raw == "program" ?
                    (
                        <React.Fragment>
                            <Container>
                                {/* <FullWidthGrid /> */}
                                <Typography component="div" style={{ fontSize: "initial" }}>
                                    <Container style={{ ...gridStyles.root }}>
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} >
                                                <Paper style={{ ...buttonStyles.root, ...innerStyles.paper, ...innerStyles.warmPaper }}>
                                                    <h2>
                                                        Program Overview
                                                    </h2>
                                                </Paper>
                                                <Paper style={{ ...innerStyles.paper }}>
                                                    {this.state.plannerObj.description && this.state.plannerObj.description.raw ? (<p>{this.state.plannerObj.description.raw}</p>) : (<h3><a href={this.state.plannerObj.url.raw} target="_blank">{this.state.plannerObj.title.raw}</a>
                                                        {this.state.fetched.description}
                                                    </h3>)}
                                                </Paper>
                                            </Grid>
                                        </Grid>
                                    </Container>
                                </Typography>
                                <Task regroupingText={this.state.regroupingText} />

                            </Container>
                        </React.Fragment>
                    ) : null
                }
                {this.state.fetched && this.state.fetched.type && this.state.fetched.type === 'course' ?
                    (
                        <React.Fragment>
                            <Container>
                                {/* <FullWidthGrid /> */}
                                <Typography component="div" style={{ fontSize: "initial" }}>
                                    <Container style={{ ...gridStyles.root }}>
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} >
                                                <Paper style={{ ...buttonStyles.root, ...innerStyles.paper, ...innerStyles.warmPaper }}>
                                                    <h2>
                                                        {this.state.fetched.title}
                                                    </h2>
                                                </Paper>
                                                <Paper style={{ ...innerStyles.paper }}>
                                                    <span>
                                                        {this.state.fetched.description}<br />
                                                    </span>
                                                </Paper>
                                            </Grid>
                                        </Grid>
                                    </Container>
                                </Typography>

                                {this.state.remote && this.state.remote.length>0 ? (
                                    <Typography component="div" style={{ fontSize: "initial" }}>
                                        <Container style={{ ...buttonStyles.root, ...gridStyles.root }}>
                                            <Grid container spacing={3}>
                                                <Grid item md={12}>
                                                    <Paper style={{ ...buttonStyles.root, ...innerStyles.paper, ...innerStyles.coolPaper }}>
                                                        <h2>Similar online courses of {this.state.fetched.title} (top 10)</h2>
                                                    </Paper>
                                                    <TableContainer component={Paper}>
                                                        <Table aria-label="simple table" style={{ minWidth: "650", fontSize: "initial" }} >
                                                            <TableHead>
                                                                <TableRow>
                                                                    {
                                                                        ["Title", "URL", "Difficulty Level"].map(
                                                                            caption => (
                                                                                <TableCell style={{ fontSize: "initial" }}>{caption}</TableCell>
                                                                            )
                                                                        )
                                                                    }
                                                                </TableRow>
                                                            </TableHead>
                                                            <TableBody>
                                                                {
                                                                    this.state.remote.map(
                                                                        item => (
                                                                            <TableRow>
                                                                                <TableCell style={{ fontSize: "initial" }}>{item.title}</TableCell>
                                                                                <TableCell>
                                                                                    <a href={item.url} target="_blank">{item.url}</a>
                                                                                </TableCell>
                                                                                <TableCell style={{ fontSize: "initial" }}>{item.level.split('_').slice(-1)}</TableCell>
                                                                            </TableRow>
                                                                        )
                                                                    )
                                                                }
                                                            </TableBody>
                                                        </Table>
                                                    </TableContainer>
                                                    
                                                </Grid>
                                            </Grid>
                                        </Container>
                                    </Typography>
                                ) : null
                                }
                            </Container>
                        </React.Fragment>
                    ) : null
                }
            </React.Fragment>
        )
    }
};
// console.log("loading " + JSON.stringify(params));