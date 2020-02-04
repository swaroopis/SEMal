import React from 'react';
import { CustomInput, FormGroup, Label } from 'reactstrap';


const FileUploader = ({
  id,
  placeholder,
  modal,
  toggleModal,
  label,
  handleChange,
}) => (
  <FormGroup>
    <Label for="exampleCustomFileBrowser">
      {placeholder}
      (<span onClick={() => toggleModal(modal)} className="like-anchor">Example</span>)
    </Label>
    <CustomInput type="file" id={id} name="customFile" label={label} onChange={() => handleChange(id)} />
  </FormGroup>
)

export default FileUploader;