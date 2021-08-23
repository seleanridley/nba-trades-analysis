import React, { useEffect } from "react";
import { Streamlit, withStreamlitConnection }  from "streamlit-component-lib";
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
  useEffect(() => Streamlit.setFrameHeight());
  return <h1>D3 goes here :)</h1>;
};

// Make the function publicly available. If you forget this, index.tsx won't find it.
export default withStreamlitConnection(NBAD3Component);