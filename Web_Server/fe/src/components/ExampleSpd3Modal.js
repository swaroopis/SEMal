import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

const ExampleSpd3Modal = ({
  open,
  toggle,
  file,
  download,
}) => (
  <Modal isOpen={open} toggle={() => toggle('exampleSpd3Modal')} className="example" >
    <ModalHeader toggle={() => toggle('exampleSpd3Modal')}>Example SPD3</ModalHeader>
    <ModalBody className="body">
      <div className="dont-break-out" dangerouslySetInnerHTML={{ __html: file }} />
    </ModalBody>
    <ModalFooter>
      <Button color="primary" onClick={() => download()}>Download</Button>
      <Button color="secondary" onClick={() => toggle('exampleSpd3Modal')}>Close</Button>
    </ModalFooter>
  </Modal>
);

export default ExampleSpd3Modal;
