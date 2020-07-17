import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

const PublicationsModal = ({
  open,
  toggle,
}) => (
  <Modal isOpen={open} toggle={() => toggle('publicationsModal')}>
    <ModalHeader toggle={() => toggle('publicationsModal')}>Publications</ModalHeader>
    <ModalBody>
      S. R. Dipta, G. Taherzadeh, Md. W. Ahmad, Md. E. Arafat, S. Shatabda, A. Dehzangi. "SEMal: Accurate Protein Malonylation Site Predictor Using Structural and Evolutionary Information" - <i>Submitted to Computers in Biology and Medicine</i>
    </ModalBody>
    <ModalFooter>
      <Button color="secondary" onClick={() => toggle('publicationsModal')}>Close</Button>
    </ModalFooter>
  </Modal>
);

export default PublicationsModal;
