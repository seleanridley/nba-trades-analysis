import React, { useEffect } from "react";
import { Streamlit, withStreamlitConnection }  from "streamlit-component-lib";
import data from './data/data.json';
import { ForceGraph } from "./components/forceGraph";
import './app.css';

/**
 * Called by <CustomSlider />, renders the return value on screen.
 *
 * (props) => {code} is an arrow function, a shorter syntax for JS functions
 * equivalent to : function (props) { code; return <h1>Hello world</h1>};
 * or in Python, lambda props : return <h1>Hello world</h1>.
 *
 * When called, it will run then render on the browser the returned JSX block
 */
const NBAD3Component = () => {
  // This React component returns (and renders) this <h1> block
  useEffect(() => Streamlit.setFrameHeight(1000));

  const nodeHoverTooltip = React.useCallback((node) => {
    return `<div>     
      <b>${node.name}</b>
    </div>`;
  }, []);

  
  return (
    <div className="App">
      <header className="App-header">
        Force Graph Example
      </header>
      <section className="Main">
      <ForceGraph linksData={data.links} nodesData={data.nodes} nodeHoverTooltip={nodeHoverTooltip} />
      </section>
    </div>
  );

};

/* class NBAD3Component extends React.Component {
  constructor(props) {
    super(props);
    this.state = {graph: ''}
  }

  componentDidMount() {
    this.setState({graph: svg});
  }

  render() {
    return (
      <div>
        <RD3Component data={this.state.graph} />
      </div>
    )
  }
}; */

// Make the function publicly available. If you forget this, index.tsx won't find it.
export default withStreamlitConnection(NBAD3Component);