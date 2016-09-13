import React, { PropTypes } from 'react';
import CurateDisplayButton from './curate_display_button';

const CurateTableRow = props => (
  <tr style={{ backgroundColor: props.sms.matched_colour }}>
    <td>{props.sms.content}</td>
    <td className="collapsing">{props.sms.time_received}</td>
    <td className="collapsing">
      <CurateDisplayButton
        sms={props.sms}
        toggleSms={props.toggleSms}
      />
    </td>
  </tr>
);

CurateTableRow.propTypes = {
  sms: PropTypes.object.isRequired,
  toggleSms: PropTypes.func.isRequired,
};

export default CurateTableRow;
