import React, {  } from 'react';
import { WebView } from 'react-native';

export default class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      content: null
    };
  }

  render() {
    const localHtml = require('./regrouping.html')

    return (
        <div>
            <WebView source={localHtml} />
        </div>
    );
  }
}