import React, { useRef, useEffect } from 'react';
export default class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      content: null,
      diagram: {
        style: {
          width: "400px",
          height: "150px",
          backgroundColor: "#DAE4E4",
        }
      }
    };
  }

  scriptLoaded() {
  }

  loadScript(src) {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    // script.onload = () => this.scriptLoaded();

    document.body.appendChild(script);
  }

  componentDidMount() {
    this.loadScript("https://unpkg.com/gojs/release/go-debug.js");
  }

  render() {
    // const localHtml = require('./regrouping.html')

    return (
      <div className="root">
        <h1>Helloworld React!</h1>
        Loading script
        <div id="myDiagramDiv" style={this.state.diagram.style}></div>
      </div>
    );
  }
}