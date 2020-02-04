import React, { Component, useState } from 'react';
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import LoadingOverlay from 'react-loading-overlay';
import { pssm, spd3 } from './placeholder';
import axios from 'axios';
import Header from './Header';
import AboutModal from './AboutModal';
import PublicationsModal from './PublicationsModal';
import ContactModal from './ContactModal';
import ExamplePssmModal from './ExamplePssmModal';
import ExampleSpd3Modal from './ExampleSpd3Modal';
import Footer from './Footer';
import FileUploader from './FileUploader';

export default class Index extends Component {
  state = {
    species: 'human',
    pssm: '',
    spd3: '',
    loading: false,
    protein: '',
    res: '',
    aboutModal: false,
    publicationsModal: false,
    contactModal: false,
    examplePssmModal: false,
    exampleSpd3Modal: false,
  }

  changeSpecies = ({ target: { value } }) => {
    this.setState({ species: value });
  }

  submit = async () => {
    this.setState({ loading: true, protein: '', res: '' });
    const { species, pssm, spd3 } = this.state;
    const { data } = await axios.post('http://13.58.188.133:7447/get_malonylation', {
      pssm,
      spd3,
      species,
    });
    const ret = data.split('\n');
    const protein = ret[0];
    const res = ret[1];
    
    this.setState({ loading: false, protein, res });
  }

  toggleModal = (type) => {
    const now = this.state[type];
    this.setState({
      [type]: !now,
    });
  }

  getFileContent = (id) => {
    var file = document.getElementById(id).files[0];
    if (file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = (evt) => {
          this.setState({
            [id]: evt.target.result,
          });
          console.log("TCL: reader.onload -> evt.target.result", evt.target.result)
        }
        reader.onerror = function (evt) {
          console.log("TCL: reader.onerror -> evt", evt)
        }
    }
  }

  download = (filename, text) => {
    const element = document.createElement('a');
    element.setAttribute('href', `data:text/plain;charset=utf-8,${encodeURIComponent(text)}`);
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
  };

  fileChange = (id) => {
    this.getFileContent(id);
  }

  render() {
    const { species, loading, protein, res, aboutModal, publicationsModal, contactModal, examplePssmModal, exampleSpd3Modal } = this.state

    let result = protein.split('').map((p, i) => {
      if (p === 'K') {
        if (res[i] === '1') return `<span class="red">${p}</span>`
        else return `<span class="green">${p}</span>`
      }
      else return `${p}`
    }).join("");
    result = `<h6>${result}</h6>`;

    let indices = res.split('').map((p, i) => {
      if (res[i] === '1') return i;
    }).filter(p => p).join(' , ');
    if (!res.length) {
      indices = "No Malonylation site";
    }

    const pssmExample = `<pre>${pssm.split('\n').map(ele => `${ele}<br/>`).join("")}</pre>`;
    const spd3Example = `<pre>${spd3.split('\n').map(ele => `${ele}<br/>`).join("")}</pre>`;

    return (
      <>
        <LoadingOverlay
          active={loading}
          spinner
          text='Fetching Result, It will take some time. Do not close or press back'
        >
          <Header toggle={this.toggleModal} />
          <div className="container-me">
            <div className="flex">
              <div>
                <h1>SEMal:</h1>
                <h3>Predict Malonylation Sites from a protein sequence using structural and evolutionary information.</h3>
                <br />
                <br />
                <div style={{ textAlign: 'left', width: '100%', marginTop: '20px' }}>
                  <h4>References:</h4>
                  <ul>
                    <li>Scientific Reports (Submitted)</li>
                  </ul>
                </div>
              </div>
              <div className="body">
                <FileUploader
                  id="pssm"
                  placeholder="Input your PSSM file"
                  modal="examplePssmModal"
                  toggleModal={this.toggleModal}
                  label="PSSM"
                  handleChange={this.fileChange}
                />
                <FileUploader
                  id="spd3"
                  placeholder="Input your SPD3 file"
                  modal="exampleSpd3Modal"
                  toggleModal={this.toggleModal}
                  label="SPD3"
                  handleChange={this.fileChange}
                />

                <FormControl component="fieldset" className="margin-top-20">
                  <FormLabel component="legend">Select Species</FormLabel>
                  <RadioGroup aria-label="position" name="position" value={species} onChange={this.changeSpecies} row>
                  <FormControlLabel
                    value="human"
                    control={<Radio color="primary" />}
                    label="Human"
                    labelPlacement="end"
                  />
                  <FormControlLabel
                    value="mice"
                    control={<Radio color="primary" />}
                    label="Mouse"
                    labelPlacement="end"
                  />
                  </RadioGroup>
                </FormControl>

                <Button variant="contained" color="primary" className="margin-top-20" onClick={this.submit}>
                  Submit
                </Button>
              </div>
            </div>

            {!!protein.length && (
              <>
                <div className="result-container" dangerouslySetInnerHTML={{ __html: result }} />
                <div>
                  <br />
                  <br />
                  <h4>Malonylation Site Indexes (0-based indexing)</h4>
                  <p>{indices}</p>
                </div>
              </>
            )}
          </div>
          <Footer />
        </LoadingOverlay>
        <AboutModal open={aboutModal} toggle={this.toggleModal} />
        <PublicationsModal open={publicationsModal} toggle={this.toggleModal} />
        <ContactModal open={contactModal} toggle={this.toggleModal} />
        <ExamplePssmModal open={examplePssmModal} toggle={this.toggleModal} download={() => this.download('pssm.txt', pssm)} file={pssmExample} />
        <ExampleSpd3Modal open={exampleSpd3Modal} toggle={this.toggleModal} download={() => this.download('spd3.txt', spd3)} file={spd3Example} />
      </>
    )
  }
}
