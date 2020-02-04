import React, { Component } from 'react';
import './App.scss';
import Index from './components/Index';
import 'bootstrap/dist/css/bootstrap.min.css';

export default class App extends Component {
  render() {
    return <Index />
  }
  //   return (
  //     <LoadingOverlay
  //       active={loading}
  //       spinner
  //       text='Fetching Result, It will take some time. Do not close or press back'
  //     >
  //       <div className="container">
  //         <div className="title">
  //           SEMal: Predict Malonylation Sites from a protein sequence using structural and evolutionary information
  //         </div>
  //         <hr />
  //         <div className="body">
  //           {/* <p>Enter or copy/paste query protein in
  //           <a href="http://prodata.swmed.edu/promals/info/fasta_format_file_example.htm"> Fasta </a>
  //             format</p> */}

  //           <div className="input-area">
  //             <TextareaAutosize
  //               onChange={(e) => this.setState({ pssm: e.target.value })}
  //               value={pssm}
  //               aria-label="PSSM"
  //               placeholder={pssm}
  //               rowsMin={20}
  //               rowsMax={20}
  //               className="input-box-pssm"
  //             />

  //             <TextareaAutosize
  //               onChange={(e) => this.setState({ spd3: e.target.value })}
  //               value={spd3}
  //               aria-label="maximum height"
  //               placeholder={spd3}
  //               rowsMin={20}
  //               rowsMax={20}
  //               className="input-box-fasta"
  //             />
  //           </div>

  //           <FormControl component="fieldset" className="margin-top-20">
  //             <FormLabel component="legend">Select Species</FormLabel>
  //             <RadioGroup aria-label="position" name="position" value={species} onChange={this.changeSpecies} row>
  //               <FormControlLabel
  //                 value="human"
  //                 control={<Radio color="primary" />}
  //                 label="Human"
  //                 labelPlacement="end"
  //               />
  //               <FormControlLabel
  //                 value="mice"
  //                 control={<Radio color="primary" />}
  //                 label="Mice"
  //                 labelPlacement="end"
  //               />
  //             </RadioGroup>
  //           </FormControl>

  //           <Button variant="contained" color="primary" className="margin-top-20" onClick={this.submit}>
  //             Submit
  //           </Button>

  //           {!!protein.length && (
  //             <>
  //               <div className="result-container" dangerouslySetInnerHTML={{ __html: result }} />
  //               <div>
  //                 <h4>Malonylation Site Indexes (0-based indexing)</h4>
  //                 <p>{indices}</p>
  //               </div>
  //             </>
  //           )}

  //         </div>
  //       </div>
  //     </LoadingOverlay>
  //   )
  // }
}
