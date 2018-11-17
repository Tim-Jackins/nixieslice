import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import Number from './clock.jsx'
import * as serviceWorker from './serviceWorker'

ReactDOM.render(<Number name="num-0" digit="0" />, document.getElementById('digit-0'))
ReactDOM.render(<Number name="num-1" digit="1" />, document.getElementById('digit-1'))

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister()
