import React, { Component } from 'react'
import ReactModal from 'react-modal'

//const API = 'localhost:8000/'

const ModalForm = (props) => {
  var form = []
  var config = props.config
  for (var num = 0; num < config.length; num++) {
    form.push(
      <div>
        <label>{num}:</label>
        <ul>
          <li>Brightness:<input type="number" name={`bright-slice-${num}`} max="255" min="0" defaultValue={config[num].brightness} /></li>
          <li>Color:<input type="color" name={`color-slice-${num}`} defaultValue={config[num].color} /></li>
        </ul>
      </div>
    )
  }

  return form
}


class Number extends Component {
  constructor() {
    super()
    this.state = {
      showModal: false,
      config: null,
      error: false,
      isLoaded: false
    }

    this.handleOpenModal = this.handleOpenModal.bind(this)
    this.handleCloseModal = this.handleCloseModal.bind(this)
    this.componentDidMount = this.componentDidMount.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  componentDidMount() {
    fetch('/api/config')
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            config: result
          })
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error: error,
          })
        }
      )
  }

  handleOpenModal() {
    this.setState({ showModal: true })
  }

  handleCloseModal() {
    this.setState({ showModal: false })
  }

  handleSubmit(event) {
    event.preventDefault()
    const data = new FormData(event.target);

    fetch('/api/config/', {
      method: 'POST',
      body: data,
    })
    
  }

  render() {
    const { showModal, config, error, isLoaded } = this.state;

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    }
    else {
      return (
        <div>
          <button onClick={this.handleOpenModal}>{this.props.name}</button>
          <ReactModal
            isOpen={showModal}
            contentLabel="Minimal Modal Example"
          >
            <button onClick={this.handleCloseModal}>Close Modal</button>
            <br></br>
            <form action="/api/config/" method="POST">
              <ModalForm config={config.Lights[`num-${this.props.digit}`]} />
              <input type="hidden" name="num" value={this.props.name} />
              <button onClick="this.submit">Make Changes</button>
            </form>
          </ReactModal>
        </div>
      )
    }
  }
}

export default Number;
