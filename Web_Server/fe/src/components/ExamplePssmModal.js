import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

const ExamplePssmModal = ({
  open,
  toggle,
  file,
  download,
}) => (
  <Modal isOpen={open} toggle={() => toggle('examplePssmModal')} className="example" >
    <ModalHeader toggle={() => toggle('examplePssmModal')}>Example PSSM</ModalHeader>
    <ModalBody className="body">
      <div className="dont-break-out" dangerouslySetInnerHTML={{ __html: file }} />
    </ModalBody>
    <ModalFooter>
      <Button color="primary" onClick={() => download()}>Download</Button>
      <Button color="secondary" onClick={() => toggle('examplePssmModal')}>Close</Button>
    </ModalFooter>
  </Modal>
);

export default ExamplePssmModal;
