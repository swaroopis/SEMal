import React, { Component } from 'react';
import './App.scss';
import TextareaAutosize from '@material-ui/core/TextareaAutosize';
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import LoadingOverlay from 'react-loading-overlay';
import { pssm, spd3 } from './placeholder';
import axios from 'axios';

export default class App extends Component {
  state = {
    species: 'human',
    pssm: pssm,
    spd3: spd3,
    loading: false,
    protein: '',
    res: '',
  }

  changeSpecies = ({ target: { value } }) => {
    this.setState({ species: value });
  }

  changeFasta = ({ target: { value } }) => {
    this.setState({ fasta: value });
  }

  submit = async () => {
    this.setState({ loading: true, protein: '', res: '' });
    const { species, pssm, spd3 } = this.state;
    const { data } = await axios.post('http://13.58.188.133:5000/get_malonylation', {
      pssm,
      spd3,
      species,
    });
    const ret = data.split('\n');
    const protein = ret[0];
    const res = ret[1];
    
    this.setState({ loading: false, protein, res });
  }

  render() {
    const { species, loading, pssm, spd3, protein, res } = this.state

    const result = protein.split('').map((p, i) => {
      if (p === 'K') {
        if (res[i] === '1') return `<span class="red">${p}</span>`
        else return `<span class="green">${p}</span>`
      }
      else return `${p}`
    }).join("");

    const indices = res.split('').map((p, i) => {
      if (res[i] === '1') return i;
    }).filter(p => p).join(' , ');

    return (
      <LoadingOverlay
        active={loading}
        spinner
        text='Fetching Result, It will take some time. Do not close or press back'
      >
        <div className="container">
          <div className="title">
            SEMal: Predict Malonylation Sites from a protein sequence using structural and evolutionary information
          </div>
          <hr />
          <div className="body">
            {/* <p>Enter or copy/paste query protein in
            <a href="http://prodata.swmed.edu/promals/info/fasta_format_file_example.htm"> Fasta </a>
              format</p> */}

            <div className="input-area">
              <TextareaAutosize
                onChange={(e) => this.setState({ pssm: e.target.value })}
                value={pssm}
                aria-label="PSSM"
                placeholder={pssm}
                rowsMin={20}
                rowsMax={20}
                className="input-box-pssm"
              />

              <TextareaAutosize
                onChange={(e) => this.setState({ spd3: e.target.value })}
                value={spd3}
                aria-label="maximum height"
                placeholder={spd3}
                rowsMin={20}
                rowsMax={20}
                className="input-box-fasta"
              />
            </div>

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
                  label="Mice"
                  labelPlacement="end"
                />
              </RadioGroup>
            </FormControl>

            <Button variant="contained" color="primary" className="margin-top-20" onClick={this.submit}>
              Submit
            </Button>

            {!!protein.length && (
              <>
                <div className="result-container" dangerouslySetInnerHTML={{ __html: result }} />
                <div>
                  <h4>Malonylation Site Indexes (0-based indexing)</h4>
                  <p>{indices}</p>
                </div>
              </>
            )}

          </div>
        </div>
      </LoadingOverlay>
    )
  }
}
